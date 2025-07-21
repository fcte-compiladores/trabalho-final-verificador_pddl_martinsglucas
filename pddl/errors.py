"""
ATENÇÃO: EVITE MODIFICAR ESTE ARQUIVO!

Execeções usadas no verificador PDDL.
"""

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .ast import Value

class PDDLError(Exception):
    """Exceção base para erros no PDDL.
    """

    def __init__(self, msg, line, column, file_path = None):
        super().__init__(f"{file_path}: linha {line}, coluna {column}: {msg}")
        self.msg = msg
        self.line = line
        self.column = column

class TypeError(PDDLError):
    """Exceção levantada quando um tipo é inválido ou não declarado."""

    def __init__(self, msg, line, column, file_path=None):
        super().__init__(msg, line, column, file_path)

class MissingRequirementError(PDDLError):
    """Exceção levantada quando um requisito necessário não é encontrado."""

    def __init__(self, msg, line, column, file_path=None):
        super().__init__(msg, line, column, file_path)

class PredicateArityError(PDDLError):
    """Exceção levantada quando um predicado é usado com o número incorreto de argumentos."""

    def __init__(self, msg, line, column, file_path=None):
        super().__init__(msg, line, column, file_path)

class UndeclaredNameError(PDDLError):
    """Exceção levantada quando um predicado ou objeto não foi declarado."""

    def __init__(self, msg, line, column, file_path=None):
        super().__init__(msg, line, column, file_path)