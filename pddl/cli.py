"""
ATENÇÃO: EVITE MODIFICAR ESTE ARQUIVO!

Este módulo usa a biblioteca `argparse` para criar uma interface de linha de comando
(CLI) para o verificador de PDDL.

Ele permite que o usuário execute o verificador com diferentes opções, como especificar
os arquivos de domínio e problema, ativar o modo para imprimir as árvores
sintáticas, lexer, etc.

Argparse talvez não seja a melhor opção para criar uma CLI, mas é uma biblioteca
padrão do Python e não requer instalação de dependências externas.
"""

import argparse

from lark import Token

from . import eval as pddl_eval
from .ctx import Ctx
from .parser import lex, parse, parse_cst, parse_expr


def make_argparser():
    parser = argparse.ArgumentParser(description="Verificador PDDL")
    parser.add_argument(
        "domain_file",
        help="Arquivo de domínio",
    )
    parser.add_argument(
        "problem_file",
        help="Arquivo de problema",
    )
    parser.add_argument(
        "-t",
        "--ast",
        action="store_true",
        help="Imprime a árvore sintática.",
    )
    parser.add_argument(
        "-l",
        "--lex",
        action="store_true",
        help="Imprime o lexer.",
    )
    parser.add_argument(
        "-c",
        "--cst",
        action="store_true",
        help="Imprime a árvore sintática concreta produzida pelo Lark.",
    )
    parser.add_argument(
        "-p",
        "--pm",
        action="store_true",
        help="Habilita o post-mortem debugger em caso de falha.",
    )
    parser.add_argument(
        "-s",
        "--show",
        action="store_true",
        help="Mostra o código fonte do arquivo de entrada.",
    )
    return parser


def main():
    """
    Função principal que cria a interface de linha de comando (CLI) para o verificador de PDDL.
    """
    parser = make_argparser()
    args = parser.parse_args()

    # Inicia o repl, se requisitado
    if args.domain_file == "repl":
        return repl()

    # Lê arquivos de domínio e problema
    try:
        with open(args.domain_file, "r") as d:
            domain_source = d.read()
        with open(args.problem_file, "r") as p:
            problem_source = p.read()
        # source = domain_source + "\n" + problem_source
        # source = domain_source
    except FileNotFoundError:
        print(f"Arquivo {args.domain_file} ou {args.problem_file} não encontrado.")
        exit(1)

    if args.show:
        line_len = 60
        head = f"=== {args.domain_file} ="
        head += "=" * (line_len - len(head))
        print_color(head, "blue")
        print()
        # print_color(source, "yellow")
        print_color(domain_source, "yellow")
        head = f"=== {args.problem_file} ="
        head += "=" * (line_len - len(head))
        print_color(head, "blue")
        print_color(problem_source, "yellow")
        print_color("=" * line_len, "blue")
        print()

    if not args.ast and not args.cst and not args.lex:
        try:
            # pddl_eval(source)
            from .ast import Predicate, Identifier
            # pddl_eval(domain_source)
            _, ctx = pddl_eval(domain_source, 
                               Ctx({
                                   "and": Predicate(Identifier("and", 0, 0), None, "strips"), 
                                   "not": Predicate(Identifier("not", 0, 0), None, "negative-preconditions"),
                                   "or": Predicate(Identifier("or", 0, 0), None, "disjunctive-preconditions"),
                                   }), 
                                   file_path=args.domain_file)
            pddl_eval(problem_source, ctx, file_path=args.problem_file)
        except Exception as e:
            on_error(e, args.pm)

    else:
        # debug_source(source, args)
        debug_source(domain_source, args)
        debug_source(problem_source, args)


def debug_source(source: str, args):
    """
    Mostra informações de depuração sobre o código PDDL passado como argumento.
    """

    if args.ast:
        ast = parse(source)
        for node in ast.lark_descendents():
            if isinstance(node, Token):
                descr = repr(node)
                tail = f"Implemente o método {node.type} no PDDLTransformer para lidar com estes terminais."
            else:
                descr = node.data
                tail = f"Implemente o método {node.data} no PDDLTransformer para lidar com regras do tipo {node.data}."
            msg = f"Atenção: A árvore sintática contém nós Lark ({descr}).\n"
            msg += tail
            print(msg)

        print(ast.pretty())

    if args.cst:
        cst = parse_cst(source)
        print(cst.pretty())

    if args.lex:
        for token in lex(source):
            print(f"{token.type}: {token.value}")


def repl():
    """
    Função que inicia o REPL (Read-Eval-Print Loop) para PDDL.
    Permite que o usuário execute código PDDL interativamente (experimental).
    """
    try:
        from rich import print, prompt

        class PDDLPrompt(prompt.Prompt):
            prompt_suffix = ""

        ask = lambda: PDDLPrompt.ask("[red]>[yellow]>[blue]> ")  # noqa: E731

    except ImportError:
        import builtins

        ask = lambda: input("pddl> ")  # noqa: E731
        print = builtins.print

    def parse_any(src: str):
        try:
            return parse_expr(src)
        except Exception:
            return parse(src)

    print("Iniciando REPL do PDDL. Digite 'exit' para sair.")
    ctx = Ctx.from_dict({})
    while True:
        source = ask()
        if source.strip().lower() == "exit":
            break
        try:
            ast = parse_any(source)
        except Exception as e:
            print(f"Erro de sintaxe: {e}")
            continue

        try:
            value = pddl_eval(ast, ctx)
        except Exception as e:
            print(f"Erro de execução: {e}")
            continue

        if value is not None:
            print(value)


def on_error(exception: Exception, pm: bool):
    if not pm:
        raise exception

    from ipdb import post_mortem  # type: ignore[import-untyped]

    post_mortem(exception.__traceback__)


def print_color(str: str, color: str):
    try:
        from rich import print

        print(f"[{color}]{str}[/{color}]")
    except ImportError:
        print(str)
