"""
modelo.py
=========

Modelo de dominio del Sistema de Gestión Hospitalaria y Consultas "MediCare Pro".

Actividad: Examen Parcial P1 — 
Autor: Luis Alberto Villegas Merchan

Este archivo reúne e integra los conceptos clave de las Semanas 1, 2 y 3:
- Semana 1: Clases, objetos, encapsulación estricta (__), getters/setters y validación Pydantic.
- Semana 2: Herencia (Medico -> MedicoGeneral, CirujanoEspecialista) y Composición (Clinica, ConsultaMedica).
- Semana 3: Clases abstractas / Interfaces (PlanSalud) y Polimorfismo dinámico en liquidación de consultas.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from pydantic import BaseModel, Field


# MODELOS DE VALIDACIÓN PYDANTIC


class DatosPaciente(BaseModel):
    """Valida la integridad de los datos de un paciente."""

    cedula: str = Field(pattern=r"^\d{10}$")
    nombre: str = Field(min_length=3, max_length=100)
    edad: int = Field(ge=0, le=125)
    telefono: str = Field(pattern=r"^\d{10}$")


class DatosMedicamento(BaseModel):
    """Valida los datos de medicamentos e insumos médicos."""

    codigo: str = Field(min_length=2, max_length=20)
    nombre: str = Field(min_length=2, max_length=100)
    precio: float = Field(gt=0)
    stock: int = Field(ge=0)


class DatosMedico(BaseModel):
    """Valida los datos del personal médico."""

    cedula: str = Field(pattern=r"^\d{10}$")
    nombre: str = Field(min_length=3, max_length=100)
    salario_base: float = Field(gt=0)
    especialidad: str = Field(min_length=3, max_length=60)



# SEMANA 1: CLASES, OBJETOS, ENCAPSULACIÓN Y VALIDACIÓN


class Paciente:
    """
    Representa a un paciente de la clínica.
    Aplica encapsulación estricta mediante atributos privados (__).
    """

    def __init__(
        self,
        cedula: str,
        nombre: str,
        edad: int,
        telefono: str,
    ) -> None:
        datos = DatosPaciente(
            cedula=cedula,
            nombre=nombre,
            edad=edad,
            telefono=telefono,
        )
        self.__cedula = datos.cedula
        self.__nombre = datos.nombre
        self.__edad = datos.edad
        self.__telefono = datos.telefono

    # Getters
    def get_cedula(self) -> str:
        """Retorna la cédula del paciente."""
        return self.__cedula

    def get_nombre(self) -> str:
        """Retorna el nombre completo del paciente."""
        return self.__nombre

    def get_edad(self) -> int:
        """Retorna la edad del paciente."""
        return self.__edad

    def get_telefono(self) -> str:
        """Retorna el teléfono de contacto."""
        return self.__telefono

    # Setters
    def set_nombre(self, nombre: str) -> None:
        """Actualiza y valida el nombre del paciente."""
        datos = DatosPaciente(
            cedula=self.__cedula,
            nombre=nombre,
            edad=self.__edad,
            telefono=self.__telefono,
        )
        self.__nombre = datos.nombre

    def set_edad(self, edad: int) -> None:
        """Actualiza y valida la edad del paciente."""
        datos = DatosPaciente(
            cedula=self.__cedula,
            nombre=self.__nombre,
            edad=edad,
            telefono=self.__telefono,
        )
        self.__edad = datos.edad

    def set_telefono(self, telefono: str) -> None:
        """Actualiza y valida el teléfono del paciente."""
        datos = DatosPaciente(
            cedula=self.__cedula,
            nombre=self.__nombre,
            edad=self.__edad,
            telefono=telefono,
        )
        self.__telefono = datos.telefono

    def mostrar_informacion(self) -> str:
        """Devuelve la información formateada del paciente."""
        return (
            f"Paciente: {self.__nombre} | CI: {self.__cedula} | "
            f"Edad: {self.__edad} años | Tel: {self.__telefono}"
        )


class Medicamento:
    """
    Representa un medicamento o insumo médico de la farmacia hospitalaria.
    """

    def __init__(
        self,
        codigo: str,
        nombre: str,
        precio: float,
        stock: int,
    ) -> None:
        datos = DatosMedicamento(
            codigo=codigo,
            nombre=nombre,
            precio=precio,
            stock=stock,
        )
        self.__codigo = datos.codigo
        self.__nombre = datos.nombre
        self.__precio = datos.precio
        self.__stock = datos.stock

    def get_codigo(self) -> str:
        """Retorna el código de inventario."""
        return self.__codigo

    def get_nombre(self) -> str:
        """Retorna el nombre del medicamento."""
        return self.__nombre

    def get_precio(self) -> float:
        """Retorna el precio unitario del medicamento."""
        return self.__precio

    def get_stock(self) -> int:
        """Retorna las unidades disponibles."""
        return self.__stock

    def set_precio(self, precio: float) -> None:
        """Actualiza y valida el precio."""
        datos = DatosMedicamento(
            codigo=self.__codigo,
            nombre=self.__nombre,
            precio=precio,
            stock=self.__stock,
        )
        self.__precio = datos.precio

    def set_stock(self, stock: int) -> None:
        """Actualiza y valida el stock disponible."""
        datos = DatosMedicamento(
            codigo=self.__codigo,
            nombre=self.__nombre,
            precio=self.__precio,
            stock=stock,
        )
        self.__stock = datos.stock

    def aumentar_stock(self, cantidad: int) -> None:
        """Incrementa el stock con valores positivos."""
        if cantidad <= 0:
            raise ValueError("La cantidad a reabastecer debe ser positiva.")
        self.set_stock(self.__stock + cantidad)

    def disminuir_stock(self, cantidad: int) -> None:
        """Disminuye el stock verificando disponibilidad."""
        if cantidad <= 0:
            raise ValueError("La cantidad a dispensar debe ser positiva.")
        if cantidad > self.__stock:
            raise ValueError(
                f"Stock insuficiente para el medicamento {self.__nombre}."
            )
        self.set_stock(self.__stock - cantidad)

    def mostrar_informacion(self) -> str:
        """Devuelve un resumen del medicamento."""
        return (
            f"[{self.__codigo}] {self.__nombre} | "
            f"Precio: ${self.__precio:,.2f} | Stock: {self.__stock} uds."
        )



# SEMANA 2: HERENCIA Y COMPOSICIÓN


class Medico:
    """
    Clase padre de los profesionales de la salud.
    """

    def __init__(
        self,
        cedula: str,
        nombre: str,
        salario_base: float,
        especialidad: str,
    ) -> None:
        datos = DatosMedico(
            cedula=cedula,
            nombre=nombre,
            salario_base=salario_base,
            especialidad=especialidad,
        )
        self.__cedula = datos.cedula
        self.__nombre = datos.nombre
        self.__salario_base = datos.salario_base
        self.__especialidad = datos.especialidad

    def get_cedula(self) -> str:
        return self.__cedula

    def get_nombre(self) -> str:
        return self.__nombre

    def get_salario_base(self) -> float:
        return self.__salario_base

    def get_especialidad(self) -> str:
        return self.__especialidad

    def set_salario_base(self, salario: float) -> None:
        datos = DatosMedico(
            cedula=self.__cedula,
            nombre=self.__nombre,
            salario_base=salario,
            especialidad=self.__especialidad,
        )
        self.__salario_base = datos.salario_base

    def calcular_honorarios_consulta(self) -> float:
        """Retorna el costo base de la consulta médica."""
        return 40.00

    def mostrar_informacion(self) -> str:
        return (
            f"Dr(a). {self.__nombre} | Esp: {self.__especialidad} | "
            f"CI: {self.__cedula} | Salario Base: ${self.__salario_base:,.2f}"
        )


class MedicoGeneral(Medico):
    """
    Médico general de atención primaria en consultorio.
    Hereda de Medico y añade consultorio asignado.
    """

    def __init__(
        self,
        cedula: str,
        nombre: str,
        salario_base: float,
        consultorio: str,
    ) -> None:
        super().__init__(
            cedula=cedula,
            nombre=nombre,
            salario_base=salario_base,
            especialidad="Medicina General",
        )
        self.__consultorio = consultorio

    def get_consultorio(self) -> str:
        return self.__consultorio

    def set_consultorio(self, consultorio: str) -> None:
        self.__consultorio = consultorio

    def calcular_honorarios_consulta(self) -> float:
        """Honorario de consulta de medicina general."""
        return 35.00

    def atender_paciente(self, paciente: Paciente) -> str:
        return (
            f"El Dr. {self.get_nombre()} atiende al paciente {paciente.get_nombre()} "
            f"en el Consultorio {self.__consultorio}."
        )


class CirujanoEspecialista(Medico):
    """
    Cirujano especialista de alta complejidad.
    Hereda de Medico y añade quirófano asignado y bono quirúrgico.
    """

    def __init__(
        self,
        cedula: str,
        nombre: str,
        salario_base: float,
        especialidad: str,
        quirofano: str,
        bono_cirugia: float = 120.00,
    ) -> None:
        super().__init__(
            cedula=cedula,
            nombre=nombre,
            salario_base=salario_base,
            especialidad=especialidad,
        )
        self.__quirofano = quirofano
        self.__bono_cirugia = bono_cirugia

    def get_quirofano(self) -> str:
        return self.__quirofano

    def set_quirofano(self, quirofano: str) -> None:
        self.__quirofano = quirofano

    def get_bono_cirugia(self) -> float:
        return self.__bono_cirugia

    def calcular_honorarios_consulta(self) -> float:
        """Honorario de consulta de alta especialidad quirúrgica."""
        return 80.00

    def realizar_intervencion(self, paciente: Paciente) -> str:
        return (
            f"El especialista Dr. {self.get_nombre()} ({self.get_especialidad()}) "
            f"programa intervención quirúrgica para {paciente.get_nombre()} "
            f"en el Quirófano {self.__quirofano} (Bono adicional: ${self.__bono_cirugia:,.2f})."
        )


class Clinica:
    """
    Representa el centro de salud que administra recursos médicos.
    Demuestra Composición al gestionar listas de médicos, pacientes y medicamentos.
    """

    def __init__(self, nombre: str, direccion: str) -> None:
        self.__nombre = nombre
        self.__direccion = direccion
        self.__medicos: list[Medico] = []
        self.__pacientes: list[Paciente] = []
        self.__medicamentos: list[Medicamento] = []

    def get_nombre(self) -> str:
        return self.__nombre

    def get_direccion(self) -> str:
        return self.__direccion

    def registrar_medico(self, medico: Medico) -> None:
        if medico not in self.__medicos:
            self.__medicos.append(medico)

    def registrar_paciente(self, paciente: Paciente) -> None:
        if paciente not in self.__pacientes:
            self.__pacientes.append(paciente)

    def agregar_medicamento(self, medicamento: Medicamento) -> None:
        if medicamento not in self.__medicamentos:
            self.__medicamentos.append(medicamento)

    def get_medicos(self) -> tuple[Medico, ...]:
        return tuple(self.__medicos)

    def get_pacientes(self) -> tuple[Paciente, ...]:
        return tuple(self.__pacientes)

    def get_medicamentos(self) -> tuple[Medicamento, ...]:
        return tuple(self.__medicamentos)

    def mostrar_resumen_institucional(self) -> str:
        return (
            f"--- RESUMEN CLÍNICO: {self.__nombre} ---\n"
            f"Ubicación: {self.__direccion}\n"
            f"Médicos en plantilla: {len(self.__medicos)}\n"
            f"Pacientes registrados: {len(self.__pacientes)}\n"
            f"Medicamentos en stock: {len(self.__medicamentos)}"
        )



# SEMANA 3: CLASES ABSTRACTAS, INTERFACES Y POLIMORFISMO


class PlanSalud(ABC):
    """
    Clase abstracta (Interfaz de seguro/cobertura médica).
    Define los métodos abstractos para calcular coberturas y copagos.
    No permite instanciación directa.
    """

    def __init__(self, titular: str, numero_poliza: str) -> None:
        self.__titular = titular
        self.__numero_poliza = numero_poliza

    def get_titular(self) -> str:
        return self.__titular

    def get_numero_poliza(self) -> str:
        return self.__numero_poliza

    @abstractmethod
    def calcular_cobertura(self, costo_total: float) -> float:
        """
        Método abstracto: Calcula el monto total que cubre el plan de salud.
        """

    @abstractmethod
    def calcular_copago(self, costo_total: float) -> float:
        """
        Método abstracto: Calcula el valor neto a pagar por el paciente.
        """

    @abstractmethod
    def get_tipo_plan(self) -> str:
        """Retorna la denominación del plan de salud."""

    def mostrar_informacion(self) -> str:
        return (
            f"Plan: {self.get_tipo_plan()} | Póliza: {self.__numero_poliza} | "
            f"Titular: {self.__titular}"
        )


class PlanParticular(PlanSalud):
    """
    Atención médica privada sin seguro.
    El paciente asume el costo. Si el monto supera $150, aplica un 5% de descuento.
    """

    def __init__(self, titular: str, numero_poliza: str = "PART-000") -> None:
        super().__init__(titular, numero_poliza)

    def calcular_cobertura(self, costo_total: float) -> float:
        """Aplica 5% de descuento por pronto pago si supera $150; de lo contrario 0."""
        if costo_total >= 150.00:
            return costo_total * 0.05
        return 0.0

    def calcular_copago(self, costo_total: float) -> float:
        """El paciente asume el costo total menos el descuento si aplica."""
        return costo_total - self.calcular_cobertura(costo_total)

    def get_tipo_plan(self) -> str:
        return "Particular (Sin Seguro)"


class PlanSeguroPrivado(PlanSalud):
    """
    Plan de Medicina Prepagada / Seguro Privado Internacional.
    Cubre el 80% fijo de honorarios y medicinas (copago del 20%).
    """

    def __init__(
        self,
        titular: str,
        numero_poliza: str,
        porcentaje_cobertura: float = 0.80,
    ) -> None:
        super().__init__(titular, numero_poliza)
        if not (0.0 <= porcentaje_cobertura <= 1.0):
            raise ValueError("La cobertura debe estar entre 0.0 y 1.0.")
        self.__porcentaje_cobertura = porcentaje_cobertura

    def calcular_cobertura(self, costo_total: float) -> float:
        """Cubre el 80% del valor total de la consulta y medicinas."""
        return costo_total * self.__porcentaje_cobertura

    def calcular_copago(self, costo_total: float) -> float:
        """El paciente solo abona el 20% de copago."""
        return costo_total - self.calcular_cobertura(costo_total)

    def get_tipo_plan(self) -> str:
        return f"Seguro Privado ({int(self.__porcentaje_cobertura * 100)}% Cobertura)"


class PlanConvenioSeguroPublico(PlanSalud):
    """
    Plan de Convenio Público / Seguro Social (IESS / Estudiantil).
    Cubre el 100% de la atención médica con un deducible administrativo fijo de $10.00.
    """

    def __init__(
        self,
        titular: str,
        numero_poliza: str,
        deducible_fijo: float = 10.00,
    ) -> None:
        super().__init__(titular, numero_poliza)
        self.__deducible_fijo = deducible_fijo

    def calcular_cobertura(self, costo_total: float) -> float:
        """Cubre el total menos el deducible administrativo fijo."""
        if costo_total > self.__deducible_fijo:
            return costo_total - self.__deducible_fijo
        return 0.0

    def calcular_copago(self, costo_total: float) -> float:
        """El paciente abona únicamente el deducible administrativo."""
        return min(self.__deducible_fijo, costo_total)

    def get_tipo_plan(self) -> str:
        return "Convenio Seguro Social (Cobertura Total con Deducible $10)"



# COMPOSICIÓN Y POLIMORFISMO: CONSULTA MÉDICA


class ConsultaMedica:
    """
    Representa un acto médico integral.

    Demuestra:
    - Composición: Integra un Paciente, un Medico, un PlanSalud y Medicamentos.
    - Polimorfismo: Resuelve los montos de cobertura y copago llamando polimórficamente
      a self.__plan_salud.calcular_cobertura() y self.__plan_salud.calcular_copago()
      sin usar ninguna sentencia if/elif de verificación de tipos.
    """

    def __init__(
        self,
        numero_atencion: str,
        paciente: Paciente,
        medico: Medico,
        plan_salud: PlanSalud,
    ) -> None:
        self.__numero_atencion = numero_atencion
        self.__paciente = paciente
        self.__medico = medico
        self.__plan_salud = plan_salud
        self.__medicamentos_recetados: list[tuple[Medicamento, int]] = []

    def get_numero_atencion(self) -> str:
        return self.__numero_atencion

    def get_paciente(self) -> Paciente:
        return self.__paciente

    def get_medico(self) -> Medico:
        return self.__medico

    def get_plan_salud(self) -> PlanSalud:
        return self.__plan_salud

    def prescribir_medicamento(self, medicamento: Medicamento, cantidad: int) -> None:
        """Agrega medicamentos recetados verificando stock disponible."""
        if cantidad <= 0:
            raise ValueError("La cantidad recetada debe ser mayor que cero.")
        if cantidad > medicamento.get_stock():
            raise ValueError(
                f"No hay stock suficiente de {medicamento.get_nombre()} "
                f"(disponible: {medicamento.get_stock()})."
            )
        self.__medicamentos_recetados.append((medicamento, cantidad))

    def calcular_subtotal_medicinas(self) -> float:
        """Suma el costo total de los medicamentos recetados."""
        return sum(
            med.get_precio() * cant
            for med, cant in self.__medicamentos_recetados
        )

    def calcular_costo_bruto(self) -> float:
        """Calcula el costo bruto total (honorarios médicos + medicinas)."""
        honorarios = self.__medico.calcular_honorarios_consulta()
        medicinas = self.calcular_subtotal_medicinas()
        return honorarios + medicinas

    def calcular_cobertura_aplicada(self) -> float:
        """
        POLIMORFISMO:
        Invoca calcular_cobertura() sobre la referencia abstracta PlanSalud.
        """
        costo_bruto = self.calcular_costo_bruto()
        return self.__plan_salud.calcular_cobertura(costo_bruto)

    def calcular_total_copago(self) -> float:
        """
        POLIMORFISMO:
        Invoca calcular_copago() sobre la referencia abstracta PlanSalud.
        """
        costo_bruto = self.calcular_costo_bruto()
        return self.__plan_salud.calcular_copago(costo_bruto)

    def confirmar_atencion(self) -> str:
        """Confirma la atención y descuenta los medicamentos del stock hospitalario."""
        for med, cant in self.__medicamentos_recetados:
            med.disminuir_stock(cant)

        bruto = self.calcular_costo_bruto()
        cobertura = self.calcular_cobertura_aplicada()
        copago = self.calcular_total_copago()

        return (
            f"Atención {self.__numero_atencion} finalizada con éxito.\n"
            f"    Paciente: {self.__paciente.get_nombre()} | "
            f"Plan: {self.__plan_salud.get_tipo_plan()}\n"
            f"    Costo Bruto: ${bruto:,.2f} | "
            f"Cobertura Seguros: -${cobertura:,.2f} | "
            f"Total a Pagar (Copago): ${copago:,.2f}"
        )

    def generar_detalle_factura(self) -> str:
        """Genera el comprobante desglosado de la atención médica."""
        honorarios = self.__medico.calcular_honorarios_consulta()
        sub_med = self.calcular_subtotal_medicinas()
        bruto = self.calcular_costo_bruto()
        cobertura = self.calcular_cobertura_aplicada()
        copago = self.calcular_total_copago()

        lineas = [
            "=" * 55,
            f"COMPROBANTE MÉDICO: {self.__numero_atencion}",
            "=" * 55,
            f"Paciente: {self.__paciente.get_nombre()} (CI: {self.__paciente.get_cedula()})",
            f"Médico Tratante: Dr(a). {self.__medico.get_nombre()} ({self.__medico.get_especialidad()})",
            f"Cobertura de Salud: {self.__plan_salud.get_tipo_plan()}",
            f"Póliza: {self.__plan_salud.get_numero_poliza()}",
            "-" * 55,
            f"Honorarios Médicos: ${honorarios:,.2f}",
            "Medicamentos / Insumos Recetados:",
        ]

        if not self.__medicamentos_recetados:
            lineas.append("  (Sin prescripción farmacéutica)")
        else:
            for med, cant in self.__medicamentos_recetados:
                sub = med.get_precio() * cant
                lineas.append(f"  • {med.get_nombre()} x{cant} unid. = ${sub:,.2f}")

        lineas.extend([
            "-" * 55,
            f"Subtotal Medicamentos: ${sub_med:,.2f}",
            f"TOTAL BRUTO DE ATENCIÓN: ${bruto:,.2f}",
            f"COBERTURA / DESCUENTO SEGURO: -${cobertura:,.2f}",
            f"VALOR NETO A CANCELAR (COPAGO): ${copago:,.2f}",
            "=" * 55,
        ])
        return "\n".join(lineas)
