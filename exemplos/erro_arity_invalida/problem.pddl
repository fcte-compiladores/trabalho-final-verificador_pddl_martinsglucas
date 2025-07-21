(define (problem my_problem)
  (:domain my_domain)
  (:objects
    box - item
    warehouse - location
    store - location
  )
  (:init
    (at box)
  )
  (:goal
    (at box store)
  )
)
; expect runtime error: File "exemplos/erro_arity_invalida/problem.pddl", line 9, column 6: at esperava 2 argumentos, mas recebeu 1