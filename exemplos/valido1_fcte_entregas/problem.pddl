(define (problem simples2)
    (:domain dom)
    (:objects
        d1 d2 - delivery-man
        a1 a2 a3 a4 a5 a6 a7 - point
        o1 o2 - order
    )

    (:init
        ;; Estado geral
        (visited origin)
        (max-capacity n2)

        (sequence n0 n1)
        (sequence n1 n2)

        ;;Entregadores
        (at d1 origin)
        (capacity d1 n0)

        (at d2 origin)
        (capacity d2 n0)

        ;;Pedidos
        (pickup o1 a1)
        (destination o1 a2)
        (pending o1)

        (pickup o2 a5)
        (destination o2 a4)
        (pending o2)

    )

    (:goal
        (and
            (not (pending o1))
            (not (pending o2))

            (visited a1)
            (visited a2)
            (visited a3)
            (visited a4)
            (visited a5)
            (visited a6)
            (visited a7)

            (at d1 origin)
            (at d2 origin)
        )
    )
)

; expect: ✅ Domínio declarado corretamente!
; expect: ✅ Problema declarado corretamente!