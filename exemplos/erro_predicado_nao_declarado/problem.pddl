(define (problem my_problem)
  (:domain my_domain)
  (:objects
    box - item
    warehouse - location
    store - location
  )
  (:init
    (at box warehouse)
    (unknown_predicate box warehouse) ; Este predicado não foi declarado no domínio
  )
  (:goal
    (at box store)
  )
)
; expect runtime error: File "exemplos/erro_predicado_nao_declarado/problem.pddl", line 10, column 6: predicado unknown_predicate não declarado