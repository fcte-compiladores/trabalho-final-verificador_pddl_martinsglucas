(define (domain my_domain)
  (:requirements :strips :typing :negative-preconditions)
  
  (:types
    item
    ;;location
  )
  (:predicates
    (at ?x - item ?l - location)
  )
  (:action move
    :parameters (?x - item ?from - location ?to - location)
    :precondition (and (at ?x ?from))
    :effect (and (not (at ?x ?from)) (at ?x ?to))
  )
)