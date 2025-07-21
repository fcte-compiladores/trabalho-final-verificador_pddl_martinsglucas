(define (problem encontrar-na-escuridao)
  (:domain casa-simples)
  (:objects
    joao - pessoa
    sala1 sala2 - sala
  )

  (:init
    (na-sala joao sala1)
    (not (luz-acesa sala1))
    (not (luz-acesa sala2))
    (tem-lanterna joao)
  )

  (:goal
    (item-encontrado joao sala1)
  )
)