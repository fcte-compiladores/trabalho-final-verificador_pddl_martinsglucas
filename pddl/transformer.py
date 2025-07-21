"""
Implementa o transformador da árvore sintática que converte entre as representações

    lark.Tree -> pddl.ast.Node.

A resolução de vários exercícios requer a modificação ou implementação de vários
métodos desta classe.
"""

from lark import Transformer, Token, v_args

from .ast import *

@v_args(inline=True)
class PDDLTransformer(Transformer):

    def program(self, source):
        return Program(source)
    
    def domain(self, *args):
        arguments = fix_list(args)

        define = arguments[0]
        requirements = [arg for arg in arguments if isinstance(arg, Requirement)]
        types = [arg for arg in arguments if isinstance(arg, Type)]
        constants = [arg for arg in arguments if isinstance(arg, Constant)]
        predicates = [arg for arg in arguments if isinstance(arg, Predicate)]
        actions = [arg for arg in arguments if isinstance(arg, Action)]

        return Domain(define, requirements, types, constants, predicates, actions)
    
    def define_domain(self, domain_name: Identifier):
        return domain_name
    
    def requirements(self, *reqs: Identifier):
        return list(Requirement(req) for req in reqs)
    
    def types(self, *types: Type):
        return list(types)
    
    def type(self, name: Identifier):
        return Type(name)
    
    def constants_def(self, *consts: Constant) -> list[Constant]:
        return list(obj for const in consts for obj in const)

    def constants(self, consts: list[Identifier] = [], type: Identifier = None) -> list[Object]:
        return list(Constant(const, type) for const in consts)

    def objects_def(self, *objs: Identifier):
        return list(objs)
    
    def predicates(self, *predicates: Predicate):
        return list(predicates)
    
    def predicate_def(self, name: Identifier, *args: Object):
        return Predicate(name, list(obj for arg in args for obj in arg))

    def predicate_arg(self, objs: list[Identifier], type: Identifier):
        return list(Object(obj, type) for obj in objs)
    
    def argument(self, objects: list[Identifier], type: Type):
        return list(Object(obj, type) for obj in objects)
    
    def action(self, name: Identifier, parameters: list[Object], precondition: list[Call], effect: list[Call]):
        return Action(name, parameters, precondition, effect)
    
    def forall(self, objs: list, call: Call):
        return Forall(objs, call)
    
    def parameters(self, *args):
        return list(obj for arg in args for obj in arg)

    def precondition(self, *args):
        return list(args)
    
    def effect(self, *args):
        return list(args)

    def call(self, name: Identifier, *args):
        return Call(name, args[0] if isinstance(args[0], list) else list(args))
    
    def problem(self, define_problem: Identifier, domain_ref: Identifier, objects: list[Object], init: list[Call], goal: list[Call]):
        return Problem(define_problem, domain_ref, objects, init, goal)

    def define_problem(self, name: Identifier):
        return name
    
    def domain_ref(self, domain_name):
        return domain_name
    
    def objects(self, *args):
        return list(obj for arg in args for obj in arg)
    
    def init(self, *args):
        return list(args)
    
    def goal(self, *args):
        return list(args)
    
    # TERMINAIS

    def IDENTIFIER(self, token: Token) -> Identifier:
        name = str(token)
        return Identifier(name, token.line, token.column)

def fix_list(elements: list):
    aux = []
    for elem in elements:
        if isinstance(elem, list):
            aux.extend(elem)
        else:
            aux.append(elem)
    return aux
