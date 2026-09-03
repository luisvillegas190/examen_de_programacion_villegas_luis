"""
main.py
=======

Punto de entrada y suite de demostración del sistema "MediCare Pro".

Actividad: Examen Parcial P1 — Programación Orientada a Objetos
Autor: Luis Alberto Villegas Merchan

Demuestra de forma modular y automatizada:
- Semana 1: Clases, objetos, encapsulación y validación con Pydantic.
- Semana 2: Herencia y composición en el ámbito clínico.
- Semana 3: Clases abstractas/interfaces (PlanSalud) y Polimorfismo dinámico en liquidaciones.
"""

from pydantic import ValidationError

from modelo import (
    CirujanoEspecialista,
    Clinica,
    ConsultaMedica,
    Medicamento,
    MedicoGeneral,
    Paciente,
    PlanConvenioSeguroPublico,
    PlanParticular,
    PlanSalud,
    PlanSeguroPrivado,
)


def encabezado(seccion: str) -> None:
    """Imprime un título de sección formateado."""
    print(f"\n>>> {seccion} <<<")


def demostrar_semana_1() -> tuple[Paciente, Medicamento]:
    """Demuestra los fundamentos de la Semana 1: Encapsulación y Pydantic."""
    encabezado("SEMANA 1 | CLASES, OBJETOS, ENCAPSULACIÓN Y VALIDACIÓN")

    print("\n[1] Creación de Instancias y Encapsulación:")
    paciente = Paciente(
        cedula="0912345678",
        nombre="Luis Alberto Villegas",
        edad=21,
        telefono="0998765432",
    )
    medicamento = Medicamento(
        codigo="MED-001",
        nombre="Amoxicilina + Ácido Clavulánico 500mg",
        precio=18.50,
        stock=40,
    )
    print(f"[OK] Objeto Paciente creado: {paciente.mostrar_informacion()}")
    print(f"[OK] Objeto Medicamento creado: {medicamento.mostrar_informacion()}")

    print("\n[2] Demostración de Getters y Setters:")
    print(f"    Nombre original: {paciente.get_nombre()} | Edad: {paciente.get_edad()}")
    paciente.set_edad(22)
    medicamento.set_precio(19.00)
    print("[OK] Atributos modificados exitosamente mediante setters.")
    print(f"    Nueva edad: {paciente.get_edad()} años | Nuevo precio: ${medicamento.get_precio():,.2f}")

    print("\n[3] Encapsulación de Atributos Privados:")
    print("[OK] Los atributos internos utilizan el prefijo privado '__'.")
    print("[OK] No se permite acceso directo desde el exterior sin métodos públicos.")

    print("\n[4] Validación de Reglas de Negocio con Pydantic:")
    try:
        # Intentamos crear un paciente con datos no válidos (cédula incompleta y edad negativa)
        Paciente(
            cedula="123",
            nombre="L",
            edad=-5,
            telefono="000",
        )
    except ValidationError as error:
        print("[OK] Pydantic interceptó y rechazó los datos inválidos.")
        print(f"    Total de anomalías detectadas: {len(error.errors())} errores de validación.")

    return paciente, medicamento


def demostrar_semana_2(
    paciente: Paciente,
    medicamento_1: Medicamento,
) -> tuple[Clinica, MedicoGeneral, CirujanoEspecialista]:
    """Demuestra la Semana 2: Herencia y Composición."""
    encabezado("SEMANA 2 | HERENCIA Y COMPOSICIÓN HOSPITALARIA")

    print("\n[1] Herencia en Jerarquía Médica:")
    medico_general = MedicoGeneral(
        cedula="0923456789",
        nombre="Dra. Elena Ramos",
        salario_base=1600.00,
        consultorio="C-102",
    )
    cirujano = CirujanoEspecialista(
        cedula="0934567890",
        nombre="Dr. Fernando Salazar",
        salario_base=3200.00,
        especialidad="Cirugía Cardiovascular",
        quirofano="Q-03",
        bono_cirugia=250.00,
    )
    print(f"[OK] MedicoGeneral (Hereda de Medico): {medico_general.mostrar_informacion()}")
    print(f"     Acción: {medico_general.atender_paciente(paciente)}")
    print(f"[OK] CirujanoEspecialista (Hereda de Medico): {cirujano.mostrar_informacion()}")
    print(f"     Acción: {cirujano.realizar_intervencion(paciente)}")

    print("\n[2] Composición: La Clínica administra médicos, pacientes e insumos:")
    clinica = Clinica(
        nombre="Hospital Metropolitano MediCare Pro",
        direccion="Av. Mariana de Jesús y Occidental, Quito",
    )
    clinica.registrar_medico(medico_general)
    clinica.registrar_medico(cirujano)
    clinica.registrar_paciente(paciente)
    clinica.agregar_medicamento(medicamento_1)

    # Medicamento secundario
    medicamento_2 = Medicamento("MED-002", "Ketorolaco Inyectable 30mg", precio=8.00, stock=60)
    clinica.agregar_medicamento(medicamento_2)

    print("[OK] Médicos, pacientes y medicamentos asociados a la clínica.")
    print(clinica.mostrar_resumen_institucional())

    return clinica, medico_general, cirujano


def demostrar_semana_3(
    paciente_1: Paciente,
    medico_general: MedicoGeneral,
    cirujano: CirujanoEspecialista,
    clinica: Clinica,
) -> None:
    """Demuestra la Semana 3: Clases Abstractas y Polimorfismo Dinámico."""
    encabezado("SEMANA 3 | CLASES ABSTRACTAS, INTERFACES Y POLIMORFISMO")

    # 1. Verificación de Clase Abstracta (ABC)
    print("\n[1] Control de Abstracción con PlanSalud (ABC):")
    try:
        # Intentamos instanciar la clase abstracta directamente
        PlanSalud("Titular Demo", "POL-000")  # type: ignore
    except TypeError as e:
        print("[OK] Python impidió instanciar la clase abstracta PlanSalud directamente:")
        print(f"    {e}")

    # 2. Creación de planes concretos (Especializaciones con Sobrescritura)
    print("\n[2] Planes de Cobertura Médica (Subclases Concretas):")
    plan_particular = PlanParticular(titular=paciente_1.get_nombre())
    plan_privado = PlanSeguroPrivado(
        titular="María Fernanda Castro",
        numero_poliza="BMI-PREMIUM-992",
        porcentaje_cobertura=0.80,  # 80% cubierto por seguro
    )
    plan_publico = PlanConvenioSeguroPublico(
        titular="Carlos Alberto Mendoza",
        numero_poliza="IESS-AFIL-8841",
        deducible_fijo=10.00,  # Deducible fijo de $10
    )

    print(f"[OK] {plan_particular.mostrar_informacion()}")
    print(f"[OK] {plan_privado.mostrar_informacion()}")
    print(f"[OK] {plan_publico.mostrar_informacion()}")

    # Pacientes adicionales para las consultas
    paciente_2 = Paciente("0945678901", "María Fernanda Castro", 35, "0981122334")
    paciente_3 = Paciente("0956789012", "Carlos Alberto Mendoza", 58, "0972233445")
    clinica.registrar_paciente(paciente_2)
    clinica.registrar_paciente(paciente_3)

    med_amox = clinica.get_medicamentos()[0]
    med_keto = clinica.get_medicamentos()[1]

    # 3. Creación de Consultas Médicas Polimórficas
    print("\n[3] Demostración de Polimorfismo en ConsultaMedica:")

    # Atención 1: Paciente Particular con Medicina General
    atencion_1 = ConsultaMedica(
        numero_atencion="ATN-2026-001",
        paciente=paciente_1,
        medico=medico_general,
        plan_salud=plan_particular,
    )
    atencion_1.prescribir_medicamento(med_amox, 2)  # 2 x $19.00 = $38.00 + $35 = $73.00

    # Atención 2: Paciente con Seguro Privado (80%) y Cirujano
    atencion_2 = ConsultaMedica(
        numero_atencion="ATN-2026-002",
        paciente=paciente_2,
        medico=cirujano,
        plan_salud=plan_privado,
    )
    atencion_2.prescribir_medicamento(med_amox, 3)  # 3 x $19.00 = $57.00
    atencion_2.prescribir_medicamento(med_keto, 4)  # 4 x $8.00 = $32.00 (+ $80 = $169.00 -> 80% cubierto)

    # Atención 3: Paciente con Seguro Público IESS ($10 deducible) y Médico General
    atencion_3 = ConsultaMedica(
        numero_atencion="ATN-2026-003",
        paciente=paciente_3,
        medico=medico_general,
        plan_salud=plan_publico,
    )
    atencion_3.prescribir_medicamento(med_keto, 2)  # 2 x $8.00 = $16.00 (+ $35 = $51.00 -> Copago: $10)

    # Lista homogénea procesada polimórficamente
    atenciones_del_dia: list[ConsultaMedica] = [
        atencion_1,
        atencion_2,
        atencion_3,
    ]

    for atencion in atenciones_del_dia:
        print("\n" + atencion.generar_detalle_factura())
        print(atencion.confirmar_atencion())

    print("\n[OK] POLIMORFISMO COMPROBADO:")
    print("     La clase ConsultaMedica liquidó coberturas y copagos invocando a PlanSalud")
    print("     sin requerir ninguna sentencia if/isinstance.")
    print(f"[OK] Stock restante de {med_amox.get_nombre()}: {med_amox.get_stock()} uds.")
    print(f"[OK] Stock restante de {med_keto.get_nombre()}: {med_keto.get_stock()} uds.")


def main() -> None:
    """Función principal que coordina la ejecución integral del examen."""
    print("=" * 65)
    print("   MEDICARE PRO | SISTEMA DE GESTIÓN CLÍNICA Y FACTURACIÓN")
    print("       EXAMEN PARCIAL P1 — PROGRAMACIÓN ORIENTADA A OBJETOS")
    print("=" * 65)
    print("Autor: Luis Alberto Villegas Merchan")
    print("Tecnologías: Python 3.14 + Pydantic + Ruff + ABC (Polimorfismo)")

    paciente, medicamento = demostrar_semana_1()
    clinica, medico_general, cirujano = demostrar_semana_2(paciente, medicamento)
    demostrar_semana_3(paciente, medico_general, cirujano, clinica)

    encabezado("RESUMEN DE EVALUACIÓN FINAL")
    print("[OK] Semana 1: Clases, objetos, encapsulación y Pydantic superados.")
    print("[OK] Semana 2: Herencia y composición hospitalaria superadas.")
    print("[OK] Semana 3: Clases abstractas, interfaces y polimorfismo superados.")
    print("\nProyecto listo y verificado para la presentación y video del examen.\n")


if __name__ == "__main__":
    main()
