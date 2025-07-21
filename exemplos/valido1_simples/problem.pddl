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
; expect: ✅ Domínio declarado corretamente!
; expect: ✅ Problema declarado corretamente!