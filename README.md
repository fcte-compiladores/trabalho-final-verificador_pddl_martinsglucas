# Título: Verificador PDDL - Lucas Martins

## Integrantes

- [Lucas Martins Gabriel](github.com/martinsglucas), matrícula 221022088, turma 3 (18h)

## Introdução

Este projeto implementa um verificador (validator) para a Planning Domain Definition Language (PDDL). PDDL é uma linguagem padronizada utilizada para descrever problemas de planejamento automático, dividindo-os em um domínio (que define o universo do problema, incluindo tipos, predicados e ações) e um problema (que define o estado inicial e o objetivo específico dentro daquele domínio).

O objetivo principal deste verificador é realizar a análise semântica estática de arquivos PDDL (domínio e problema) para garantir sua validade e consistência antes que sejam passados para um planejador. Isso significa que o verificador não gera planos, mas sim reporta erros como:

- Entidades não declaradas: Predicados, objetos ou tipos que são utilizados, mas não foram previamente definidos.

- Aridade incorreta de predicados: Predicados usados com um número de argumentos diferente do que foi declarado.

- Incompatibilidade de tipos: Argumentos passados para predicados que não correspondem aos tipos esperados.

- Requisitos PDDL não atendidos: Verificação se as funcionalidades avançadas da linguagem utilizadas no domínio foram explicitamente declaradas (``:typing``).

A ferramenta utiliza a biblioteca Lark para as etapas de análise léxica e sintática, e implementa uma Árvore de Sintaxe Abstrata (AST) personalizada para a análise semântica e validação.

**A linguagem PDDL suportada foca em um subconjunto** relevante para problemas de satisfação de planos, incluindo:

- Declarações de ``domain`` e ``problem``.

- Seção ``:requirements`` com suporte a ``:strips``, ``:typing``, e ``:negative-preconditions``.

- Definição de ``:types``, ``:constants``, ``:predicates`` e ``:actions``.

- Estruturas lógicas básicas como ``and``, ``not`` e ``forall`` (em precondições e efeitos).

- Seções ``:objects``, ``:init`` e ``:goal`` para o problema.

### Exemplo

```pddl
(define (domain my_domain)
  (:requirements :strips :typing :negative-preconditions)
  
  (:types
    item location - object
  )
  (:predicates
    (at ?x - item ?l - location)
  )
  (:action move
    :parameters (?x - item ?from - location ?to - location)
    :precondition (and (at ?x ?from))
    :effect (and (not (at ?x ?from)) (at ?x ?to))
  )
)
```

```pddl
(define (problem my_problem)
  (:domain my_domain)
  (:objects
    box - item
    warehouse - location
    store - location
  )
  (:init
    (at box warehouse)
  )
  (:goal
    (at box store)
  )
)
```

## Instalação

A única dependência externa é a biblioteca Lark. Use o método preferido de instalação do seu sistema para instalá-la. De modo geral, recomendo usar a ferramenta [uv](https://docs.astral.sh/uv/). Siga as instruções de instalação por lá e use o verificador com o comando

```bash
$ uv run pddl
```

## Uso

O verificador pode ser executado diretamente no terminal, passando os caminhos dos arquivos de domínio e problema PDDL como argumentos. Por exemplo:

```bash
$ uv run pddl domain.pddl problem.pddl
```

## Exemplos

O projeto contém uma pasta ``exemplos/`` com diversos arquivos PDDL organizados em subdiretórios, demonstrando tanto casos válidos quanto diferentes tipos de erros que o verificador é capaz de identificar. Cada subdiretório representa um caso de teste completo, contendo um ``domain.pddl`` e um ``problem.pddl``. As expectativas para cada teste (saídas esperadas ou mensagens de erro de runtime) estão definidas como comentários no arquivo ``problem.pddl``.

### Exemplos válidos

- ``valido1_simples/``: Um domínio e problema PDDL básico para demonstração.

- ``valido2_visit_all_sequential/``: Um domínio de "visitar todos" (grid).

- ``valido3_fcte_entregas/``: Um exemplo mais complexo de entregas.

Estes exemplos representam domínios e problemas PDDL bem-formados e semanticamente corretos. O verificador deve ser executado sem lançar exceções, imprimindo as mensagens de sucesso ``✅ Domínio declarado corretamente!`` e ``✅ Problema declarado corretamente!``.

### Exemplos inválidos

- ``erro_arity_invalida/``: Tenta usar um predicado com o número incorreto de argumentos.

- ``erro_objeto_nao_declarado/``: Faz referência a um objeto que não foi declarado.

- ``erro_predicado_nao_declarado/``: Tenta usar um predicado que não foi definido no domínio.

- ``erro_requirement_nao_importado/``: Demonstra o uso de uma funcionalidade PDDL (como uso de ``not``) sem declarar o requisito correspondente (``:negative-preconditions``).

- ``erro_tipo_de_argumento_invalido/``: Passa um argumento com um tipo incompatível para um predicado.

- ``erro_tipo_nao_declarado/``: Tenta usar um tipo que não foi declarado no domínio.

## Referências

- Lark (``lark-parser``): Biblioteca utilizada para a análise léxica e sintática do PDDL. Responsável por gerar a CST (Concrete Syntax Tree) a partir da gramática e auxiliar na transformação para a AST.

- Padrão PDDL: A sintaxe e semântica da linguagem PDDL foram implementadas com base nas especificações do PDDL, que evoluíram através de várias International Planning Competitions (IPC). A implementação cobre os requisitos essenciais como :strips, :typing e :negative-preconditions.

- Código Base (Referência): Este projeto foi desenvolvido sobre uma estrutura base de um interpretador da linguagem Lox, usado na disciplina. As contribuições originais para este projeto incluem:

    - A gramática PDDL (``grammar.lark``).
    - A totalidade dos nós da Árvore de Sintaxe Abstrata (AST) específica para PDDL (``ast.py``).
    - A lógica de validação semântica (método ``eval`` nos nós da AST) e modificação do método ``eval`` para lidar com a análise semântica de ambos os arquivos, garantindo que o problema esteja validado em relação ao domínio
    - As classes de erro personalizadas para PDDL (``errors.py``) e seu tratamento.
    - A atualização da interface de linha de comando (CLI), permitindo que o verificador aceite dois arquivos como argumentos: um arquivo de domínio e um arquivo de problema PDDL..
    - A integração da análise de requisitos.

## Estrutura

O código do projeto está organizado no diretório ``pddl`` nos seguintes módulos principais:

- ``cli.py``: Define a interface de linha de comando (CLI) para o verificador

- ``grammar.lark``: O arquivo que define a gramática PDDL na sintaxe do Lark.

- ``parser.py``: Realiza a análise léxica (transformando o código PDDL em tokens) e a análise sintática (construindo a CST e, posteriormente, a AST) 

- ``transformer.py``: Converte a CST (Concrete Syntax Tree) gerada pelo Lark em uma AST (Abstract Syntax Tree) 

- ``ast.py``: Define os nós da Árvore de Sintaxe Abstrata (AST) e implementa a lógica de validação semântica.

- ``ctx.py``: Gerencia o ambiente de execução e o escopo de variáveis

- ``errors.py``: Contém as definições das classes de exceção personalizadas do verificador PDDL (PDDLError e suas subclasses específicas).

- ``node.py``: Define a classe base Node para todos os nós da AST

## Bugs/Limitações/Problemas Conhecidos

Embora suporte os requisitos e recursos básicos e alguns avançados, o verificador não implementa a totalidade das funcionalidades do PDDL (``derived-predicates``, ``preferences``, ``numeric-fluents`` com operações complexas, certas formas de efeitos condicionais ou quantificadores como ``conditional-effects`` e ``adl``, etc.).

Futuras melhorias podem incluir:
- Suporte a mais requisitos PDDL, como ``:conditional-effects`` e ``:adl``.