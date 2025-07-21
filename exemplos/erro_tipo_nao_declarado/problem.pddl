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
; expect runtime error: File "exemplos/erro_tipo_nao_declarado/domain.pddl", line 9, column 24: tipo location não declarado