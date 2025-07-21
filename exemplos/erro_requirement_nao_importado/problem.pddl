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
; expect runtime error: File "exemplos/erro_tipo_de_argumento_invalido/domain.pddl", line 13, column 19: not não encontrado, necessário :negative-preconditions