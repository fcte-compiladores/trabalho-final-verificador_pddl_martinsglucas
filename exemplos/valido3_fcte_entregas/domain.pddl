(define (domain dom)

  ;remove requirements that are not needed
  (:requirements :strips :typing :negative-preconditions)

  (:types
    delivery-man point order num
  )

  (:constants
    origin - point
    n0 n1 n2 - num
  )

  (:predicates ;todo: define predicates here
    (at ?d - delivery-man ?p - point)
    (pending ?o - order)
    (pickup ?o - order ?p - point)
    (destination ?o - order ?p - point)
    (carrying ?d - delivery-man ?o - order)
    (visited ?p - point)

    (sequence ?n1 ?n2 - num)
    (capacity ?d - delivery-man ?n - num)
    (max-capacity ?n - num)
  )

  (:action move
    :parameters (?d - delivery-man ?p1 ?p2 - point)
    :precondition (and
      (at ?d ?p1)
      (not (visited ?p2))
    )
    :effect (and
      (not (at ?d ?p1))
      (at ?d ?p2)
      (visited ?p2)
    )
  )

  (:action move-to-origin
    :parameters (?d - delivery-man ?p - point)
    :precondition (and
      (at ?d ?p)
      (not (at ?d origin))
      (forall
        (?p - point)
        (visited ?p))
    )
    :effect (and
      (not(at ?d ?p))
      (at ?d origin)
    )
  )

  (:action take
    :parameters (?d - delivery-man ?o - order ?p - point ?cur ?next - num)
    :precondition (and
      (at ?d ?p)
      (pending ?o)
      (pickup ?o ?p)
      (not (carrying ?d ?o))
      (sequence ?cur ?next)
      (capacity ?d ?cur)
      (not (max-capacity ?cur))
    )
    :effect (and
      (carrying ?d ?o)
      (not (capacity ?d ?cur))
      (capacity ?d ?next)
    )
  )

  (:action deliver
    :parameters (?d - delivery-man ?o - order ?p - point ?cur ?next - num)
    :precondition (and
      (at ?d ?p)
      (pending ?o)
      (destination ?o ?p)
      (carrying ?d ?o)
      (sequence ?next ?cur)
      (capacity ?d ?cur)
    )
    :effect (and
      (not (pending ?o))
      (not (carrying ?d ?o))
      (not (capacity ?d ?cur))
      (capacity ?d ?next)
    )
  )
)