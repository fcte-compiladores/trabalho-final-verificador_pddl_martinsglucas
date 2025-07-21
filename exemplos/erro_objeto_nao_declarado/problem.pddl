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
    (at box home)
  )
)
; expect runtime error: File "exemplos/erro_objeto_nao_declarado/problem.pddl", line 12, column 13: objeto home não declarado