from abc import ABC
from dataclasses import dataclass
from typing import Callable
from .errors import PDDLError, MissingRequirementError, PredicateArityError , TypeError, UndeclaredNameError
from .ctx import Ctx

# Declaramos nossa classe base num módulo separado para esconder um pouco de
# Python relativamente avançado de quem não se interessar pelo assunto.
#
# A classe Node implementa um método `pretty` que imprime as árvores de forma
# legível. Também possui funcionalidades para navegar na árvore usando cursores
# e métodos de visitação.
from .node import Node


#
# TIPOS BÁSICOS
#

# Tipos de valores que podem aparecer durante a execução do programa
Value = str | None

class Expr(Node, ABC):
    """
    Classe base para expressões.

    Expressões são nós que podem ser avaliados para produzir um valor.
    Também podem ser atribuídos a variáveis, passados como argumentos para
    funções, etc.
    """

@dataclass
class Program(Node):
    """
    Representa um programa.

    Um programa é uma lista de comandos.
    """

    source: Expr

    def eval(self, ctx: Ctx, file_path: str | None = None):
        return self.source.eval(ctx, file_path)


#
# EXPRESSÕES
#

@dataclass
class Domain(Expr):
    define: "Identifier"
    requirements: list["Requirement"]
    types: list["Type"]
    constants: list["Constant"]
    predicates: list["Predicate"]
    actions: list["Action"]
    
    def eval(self, ctx: Ctx, file_path: str | None = None):
        try:
            self.define.eval(ctx)
            for requirement in self.requirements:
                requirement.eval(ctx)
            for type in self.types:
                type.eval(ctx)
            for constant in self.constants:
                constant.eval(ctx)
            for predicate in self.predicates:
                predicate.eval(ctx)
            for action in self.actions:
                action.eval(ctx)
            print("✅ Domínio declarado corretamente!")
            return ctx
        except PDDLError as p:
            raise p.__class__(msg=p.msg, line=p.line, column=p.column, file_path=file_path)

@dataclass
class Problem(Expr):
    define_problem: "Identifier" 
    domain_ref: "Identifier" 
    objects: list["Object"] 
    init: list["Call"] 
    goal: list["Call"]

    def eval(self, ctx: Ctx, file_path: str | None = None):
        try:
            self.define_problem.eval(ctx)
            self.domain_ref.eval(ctx)
            for obj in self.objects:
                ctx.var_def(obj.name.name, obj)
                obj.eval(ctx)
            for init_call in self.init:
                init_call.eval(ctx)
            for goal_call in self.goal:
                goal_call.eval(ctx)
            print("✅ Problema declarado corretamente!")
        except PDDLError as p:
            raise p.__class__(msg=p.msg, line=p.line, column=p.column, file_path=file_path)

@dataclass
class Identifier(Expr):
    """
    Uma variável no código

    Ex.: x, y, z
    """

    name: str
    line: int
    column: int

    def eval(self, ctx: Ctx):
        ...

    def __repr__(self):
        return f"ident {self.name}"
        
@dataclass
class Requirement(Expr):
    name: Identifier

    def eval(self, ctx: Ctx):
        ctx.var_def(self.name.name, self)

@dataclass
class Type(Expr):
    name: Identifier

    def eval(self, ctx: Ctx):
        ctx.var_def(self.name.name, self)
        try:
            if ctx["typing"]:
                pass
        except KeyError:
            raise MissingRequirementError (
                        f"erro ao declarar {self.name.name}, necessário :typing",
                        line=self.name.line,
                        column=self.name.column
                        )

    
    def __repr__(self):
        return f"type {self.name.name}"
    
@dataclass
class Object(Expr):
    name: Identifier
    type: Identifier
    
    def eval(self, ctx: Ctx):
        try:
            if ctx[self.type.name]:
                # print(f"tipo {self.type.name} existe")
                # ctx.var_def(self.name.name, self)
                ...
        except Exception:
            raise TypeError(f"tipo {self.type.name} não declarado", line=self.type.line, column=self.type.column)
    
@dataclass
class Constant(Expr):
    name: Identifier
    type: Identifier

    def eval(self, ctx: Ctx):
        try:
            if ctx[self.type.name]:
                ctx.var_def(self.name.name, self)
                # print(ctx)
                ...
        except Exception:
            raise TypeError(f"{self.type.name} não declarado", line=self.type.line, column=self.type.column)
    def __repr__(self):
        return f"const {self.name.name}"
@dataclass
class Predicate(Expr):
    name: Identifier
    args: list[Object]
    requirement: str | None = None

    def eval(self, ctx: Ctx):

        ctx.var_def(self.name.name, self)

        for arg in self.args:
            arg.eval(ctx)

    def __repr__(self):
        return f"pred {self.name.name}"

@dataclass
class Call(Expr):
    """
    Representa o uso de um predicado
    """
    name: Identifier
    args: list[Identifier | Expr]

    def eval(self, ctx: Ctx):
        # 1. Verificar se o predicado (self.name.name) foi declarado
        try:
            predicate: Predicate = ctx[self.name.name]
        except KeyError:
            raise UndeclaredNameError(f"predicado {self.name.name} não declarado", 
                                      line=self.name.line, column=self.name.column)
        
        # 2. Verificar o requisito associado ao predicado (se houver)
        if predicate.requirement is not None:
            try:
                if ctx[predicate.requirement]:
                    pass
            except KeyError:
                raise MissingRequirementError (
                    f"{predicate.name.name} não encontrado, necessário :{predicate.requirement}",
                    line=self.name.line,
                    column=self.name.column
                    )
        # 3. Verificar a aridade (número de argumentos) do predicado
        if predicate.args is not None:
            if len(self.args) != len(predicate.args):
                raise PredicateArityError(
                    f"{self.name.name} esperava {
                        len(predicate.args)} {
                            "argumento" if len(predicate.args) == 1 
                            else "argumentos"}, mas recebeu {len(self.args)}", 
                    line=self.name.line, column=self.name.column)
            
            # 4. Verificar o tipo dos argumentos passados
            for arg_1, arg_2 in zip(self.args, predicate.args):
                expected_type = arg_2.type.name
                try:
                    real_type = ctx[arg_1.name].type.name
                except KeyError:
                    raise UndeclaredNameError(f"objeto {arg_1.name} não declarado", 
                                              line=arg_1.line, column=arg_1.column)
                
                if real_type != expected_type:
                    raise TypeError(
                        f"({self.name.name} {" ".join(
                            [f"**?{obj.name.name} - {obj.type.name}**" if obj.name.name == arg_2.name.name 
                                else f"?{obj.name.name} - {obj.type.name}"
                                for obj in predicate.args]
                            )}) esperava argumento do tipo '{expected_type}', mas recebeu '{real_type}'", 
                        line=arg_1.line, 
                        column=arg_1.column)
                
        for arg in self.args:
            arg.eval(ctx)

@dataclass
class Forall(Expr):
    objs: list[Object]
    call: Call

    def eval(self, ctx: Ctx):
        scope = ctx.push({})
        for obj in self.objs:
            scope.var_def(obj.name.name, obj)
            obj.eval(scope)
        self.call.eval(scope)
        scope.pop()

@dataclass
class When(Expr):
    when: Identifier
    condition: Call
    effect: Call

    def eval(self, ctx: Ctx):
        try:
            if ctx["conditional-effects"]:
                pass
        except KeyError:
            raise MissingRequirementError(
                "erro ao declarar when, necessário :conditional-effects",
                line=self.when.line,
                column=self.when.column
            )
        self.condition.eval(ctx)
        self.effect.eval(ctx)

@dataclass
class Action(Expr):
    name: Identifier
    parameters: list[Object]
    precondition: list[Call]
    effect: list[Call]
    
    def eval(self, ctx: Ctx):
        env = ctx.push({})
        for parameter in self.parameters:
            env.var_def(parameter.name.name, parameter)
            parameter.eval(env)
        for precon in self.precondition:
            precon.eval(env)
        for eff in self.effect:
            eff.eval(env)
        env.pop()
    
    def __repr__(self):
        return f"act {self.name.name}"
