(define (domain casa-simples)
  (:requirements :strips :typing :conditional-effects :negative-preconditions :disjunctive-preconditions)
  (:types
    pessoa sala
  )

  (:predicates
    (na-sala ?p - pessoa ?s - sala)
    (luz-acesa ?s - sala) 
    (tem-lanterna ?p - pessoa)
    (item-encontrado ?p - pessoa ?s - sala)
  )

  (:action mover
    :parameters (?p - pessoa ?de - sala ?para - sala)
    :precondition (and (na-sala ?p ?de)
      (not (na-sala ?p ?para)))
    :effect (and (not (na-sala ?p ?de))
      (na-sala ?p ?para))
  )

  (:action acender-luz
    :parameters (?p - pessoa ?s - sala)
    :precondition (and (na-sala ?p ?s)
      (not (luz-acesa ?s))) 
    :effect (luz-acesa ?s)
  )

  (:action apagar-luz
    :parameters (?p - pessoa ?s - sala)
    :precondition (and (na-sala ?p ?s)
      (luz-acesa ?s))
    :effect (not (luz-acesa ?s))
  )

  (:action procurar-item
    :parameters (?p - pessoa ?s - sala)
    :precondition (na-sala ?p ?s)
    :effect (when
      (or (luz-acesa ?s) (tem-lanterna ?p))
      (item-encontrado ?p ?s))
  )

)