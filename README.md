# MediCare Pro — Sistema de Gestión Clínica y Facturación Médica

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2.13.4-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![Ruff](https://img.shields.io/badge/Linter-Ruff-D7FF64?style=for-the-badge&logo=ruff&logoColor=black)
![POO](https://img.shields.io/badge/Paradigma-POO_Avanzado-1B365D?style=for-the-badge)
![Blackboard](https://img.shields.io/badge/Evaluaci%C3%B3n-Examen_P1-green?style=for-the-badge)

---

## 📌 Datos de la Evaluación y Estudiante

* **Estudiante:** Luis Alberto Villegas Merchan
* **Materia:** Programación Orientada a Objetos / Programación Estructurada
* **Evaluación:** Examen Parcial P1 — Presentación y Explicación del Proyecto
* **Lenguaje:** Python 3.14
* **Repositorio GitHub:** [https://github.com/luisvillegas190/examen-de-programacion-estructurada](https://github.com/luisvillegas190/examen-de-programacion-estructurada)

---

## 📑 Tabla de Contenidos

1. [Descripción del Proyecto](#-descripción-del-proyecto)
2. [Objetivos del Proyecto](#-objetivos-del-proyecto)
3. [Principios de POO Integrados (Semanas 1, 2 y 3)](#-principios-de-poo-integrados)
4. [Diagrama de Clases UML](#-diagrama-de-clases-uml)
5. [Estructura del Código Fuente](#-estructura-del-código-fuente)
6. [Instalación y Ejecución](#-instalación-y-ejecución)
7. [Demostración de Resultados](#-demostración-de-resultados)
8. [🎬 Guión para la Grabación del Video (Máx. 10 Minutos)](#-guión-para-la-grabación-del-video-máx-10-minutos)

---

## 🏥 Descripción del Proyecto

**MediCare Pro** es una solución de software orientada a objetos diseñada para la administración hospitalaria, gestión de historias clínicas, farmacia interna y liquidación automatizada de consultas médicas con cálculo de coberturas y copagos según el seguro de salud del paciente.

El sistema modela el flujo completo de una clínica:
1. Registro y control seguro de **Pacientes** y **Medicamentos**.
2. Administración del personal médico (**Médicos Generales** y **Cirujanos Especialistas**).
3. Agrupación y gestión institucional a través de la clase central **Clínica**.
4. Liquidación polimórfica de **Consultas Médicas** mediante una interfaz abstracta de **Planes de Salud** (Particular, Seguro Privado y Convenio Seguro Social).

---

## 🎯 Objetivos del Proyecto

* **Consolidar los aprendizajes de las Semanas 1, 2 y 3** en una arquitectura de software robusta, desacoplada y escalable.
* Demostrar la **encapsulación estricta** mediante atributos privados (`__`) y validaciones de negocio en tiempo real.
* Reutilizar código y modelar especializaciones mediante **herencia simple**.
* Implementar **composición** para representar relaciones "todo-parte" entre la clínica, médicos, medicamentos y consultas.
* Aplicar **polimorfismo dinámico** y **clases abstractas (`ABC`)** para liquidar pagos y seguros sin condicionales `if/isinstance`.

---

## 🧩 Principios de POO Integrados

### 1. Semana 1: Clases, Objetos, Encapsulación y Validación
* **Atributos Privados (`__`):** Ocultamiento de la información sensible del paciente (`__cedula`, `__nombre`, `__edad`, `__telefono`) y del medicamento (`__precio`, `__stock`).
* **Getters y Setters:** Métodos públicos de consulta y mutación que garantizan la integridad del estado interno del objeto.
* **Validación con Pydantic:** Se utilizan modelos `BaseModel` (`DatosPaciente`, `DatosMedicamento`, `DatosMedico`) para asegurar:
  * Cédulas y teléfonos válidos con expresiones regulares (`r"^\d{10}$"`).
  * Longitudes mínimas de nombres.
  * Precios y honorarios estrictamente positivos (`gt=0`).
  * Edades lógicas (`0 <= edad <= 125`).

### 2. Semana 2: Herencia y Composición
* **Herencia (`is-a`):**
  * Clase Padre: `Medico` (define `salario_base`, `cedula`, `especialidad` y honorarios base).
  * Subclases Hijas:
    * `MedicoGeneral`: Especializado en atención ambulatoria en consultorio.
    * `CirujanoEspecialista`: Especializado en intervenciones de quirófano con bono quirúrgico y honorarios especializados.
* **Composición (`has-a`):**
  * `Clinica`: Administra colecciones dinámicas de médicos, pacientes y medicamentos.
  * `ConsultaMedica`: Compone un paciente, un médico tratante, un plan de salud y una lista de medicamentos recetados con sus cantidades.

### 3. Semana 3: Clases Abstractas, Interfaces y Polimorfismo
* **Clase Abstracta / Interfaz (`PlanSalud` con `abc.ABC`):**
  * Declara los métodos abstractos `@abstractmethod def calcular_cobertura(...)` y `@abstractmethod def calcular_copago(...)`.
  * Impide la instanciación de planes genéricos no definidos.
* **Sobrescritura de Métodos (`Method Overriding`):**
  * `PlanParticular`: Aplica tarifa completa (con 5% de descuento por pronto pago en montos superiores a \$150).
  * `PlanSeguroPrivado`: Cobertura del 80% sobre el total (el paciente cancela el 20% de copago).
  * `PlanConvenioSeguroPublico`: Cobertura total de la atención con deducible administrativo fijo de \$10.00.
* **Polimorfismo Dinámico en `ConsultaMedica`:**
  * La consulta delega el cálculo financiero invocando `self.__plan_salud.calcular_copago(costo_bruto)`.
  * **Sin condicionales:** El sistema no necesita saber el tipo concreto de seguro; la llamada se resuelve dinámicamente en tiempo de ejecución.

---

## 📊 Diagrama de Clases UML

```mermaid
classDiagram
    class Paciente {
        -str __cedula
        -str __nombre
        -int __edad
        -str __telefono
        +get_cedula() str
        +get_nombre() str
        +set_edad(edad) void
        +mostrar_informacion() str
    }

    class Medicamento {
        -str __codigo
        -str __nombre
        -float __precio
        -int __stock
        +aumentar_stock(cantidad) void
        +disminuir_stock(cantidad) void
        +mostrar_informacion() str
    }

    class Medico {
        -str __cedula
        -str __nombre
        -float __salario_base
        -str __especialidad
        +calcular_honorarios_consulta() float
        +mostrar_informacion() str
    }

    class MedicoGeneral {
        -str __consultorio
        +atender_paciente(paciente) str
    }

    class CirujanoEspecialista {
        -str __quirofano
        -float __bono_cirugia
        +realizar_intervencion(paciente) str
    }

    Medico <|-- MedicoGeneral : hereda
    Medico <|-- CirujanoEspecialista : hereda

    class PlanSalud {
        <<abstract>>
        -str __titular
        -str __numero_poliza
        +calcular_cobertura(costo_total)* float
        +calcular_copago(costo_total)* float
        +get_tipo_plan()* str
    }

    class PlanParticular {
        +calcular_cobertura(costo_total) float
        +calcular_copago(costo_total) float
    }

    class PlanSeguroPrivado {
        -float __porcentaje_cobertura
        +calcular_cobertura(costo_total) float
        +calcular_copago(costo_total) float
    }

    class PlanConvenioSeguroPublico {
        -float __deducible_fijo
        +calcular_cobertura(costo_total) float
        +calcular_copago(costo_total) float
    }

    PlanSalud <|-- PlanParticular : implementa
    PlanSalud <|-- PlanSeguroPrivado : implementa
    PlanSalud <|-- PlanConvenioSeguroPublico : implementa

    class Clinica {
        -str __nombre
        -str __direccion
        -List~Medico~ __medicos
        -List~Paciente~ __pacientes
        -List~Medicamento~ __medicamentos
        +registrar_medico(medico) void
        +registrar_paciente(paciente) void
        +agregar_medicamento(medicamento) void
    }

    class ConsultaMedica {
        -str __numero_atencion
        -Paciente __paciente
        -Medico __medico
        -PlanSalud __plan_salud
        -List __medicamentos_recetados
        +prescribir_medicamento(med, cant) void
        +calcular_costo_bruto() float
        +calcular_cobertura_aplicada() float
        +calcular_total_copago() float
        +confirmar_atencion() str
    }

    Clinica *-- Medico : administra
    Clinica *-- Paciente : registra
    Clinica *-- Medicamento : almacena
    ConsultaMedica o-- Paciente : atiende
    ConsultaMedica o-- Medico : atendido por
    ConsultaMedica o-- PlanSalud : liquida polimórficamente
    ConsultaMedica *-- Medicamento : prescribe
```

---

## 📁 Estructura del Código Fuente

```text
examen-de-programacion-estructurada/
│
├── modelo.py              # Definición de clases del dominio (POO Semanas 1, 2 y 3)
├── main.py                # Suite de ejecución, pruebas y demostración automatizada
├── requirements.txt       # Dependencias del proyecto (Pydantic, Ruff)
├── .gitignore             # Exclusión de archivos de compilación, caché y temporales
├── README.md              # Documentación técnica y guía de sustentación del examen
└── diagramas/
    └── uml_examen.puml    # Diagrama de clases editable en formato PlantUML
```

---

## 🚀 Instalación y Ejecución

### 1. Clonar el repositorio
```bash
git clone https://github.com/luisvillegas190/examen-de-programacion-estructurada.git
cd examen-de-programacion-estructurada
```

### 2. Instalar dependencias
```bash
python -m pip install -r requirements.txt
```

### 3. Ejecutar la suite del proyecto
```bash
python main.py
```

### 4. Verificar calidad de código con Ruff
```bash
python -m ruff check .
```

---

## 📈 Demostración de Resultados

Al ejecutar `python main.py`, el sistema valida automáticamente:
1. **Semana 1:** Crea paciente y medicamento con atributos privados, ejecuta getters/setters y rechaza datos anómalos mediante Pydantic (`[OK]`).
2. **Semana 2:** Crea instancias de `MedicoGeneral` y `CirujanoEspecialista` invocando sus métodos heredados y propios, y genera el resumen institucional de la `Clinica` (`[OK]`).
3. **Semana 3:** Comprueba que `PlanSalud` no puede instanciarse directamente (lanza `TypeError`), procesa tres consultas con distintos planes de salud liquidando los copagos polimórficamente y descuenta el stock de medicamentos (`[OK]`).

---

## 🎬 Guión para la Grabación del Video (Máx. 10 Minutos)

Utiliza este guión estructurado mientras grabas tu pantalla mostrando el `README.md` y el código en VS Code:

### ⏱ Minuto 0:00 - 1:30 | Presentación y Objetivos
* *"Hola con todos, mi nombre es **Luis Alberto Villegas Merchan** y a continuación presento mi proyecto para el Examen Parcial P1 de Programación Orientada a Objetos."*
* *(Muestra el README.md en modo Preview en VS Code)*.
* *"El proyecto se titula **MediCare Pro**, un sistema de gestión hospitalaria y facturación médica desarrollado en Python 3.14 que integra de forma completa los temas estudiados en las Semanas 1, 2 y 3: encapsulación y validación de datos, herencia y composición, y clases abstractas con polimorfismo."*

### ⏱ Minuto 1:30 - 3:30 | Explicación del Código: Semana 1 (Encapsulación y Pydantic)
* *(Abre `modelo.py` y muestra las clases `Paciente` y `Medicamento`)*.
* *"En la Semana 1 aplicamos **encapsulación estricta**. Todos los atributos como cédula, nombre, precio o stock tienen el prefijo privado `__`. Esto evita modificaciones indebidas desde el exterior y obliga al uso de métodos controlados `get_` y `set_`."*
* *"Adicionalmente, integramos **Pydantic** (`DatosPaciente`, `DatosMedicamento`) en los constructores y setters para validar que las cédulas y teléfonos tengan exactamente 10 dígitos y que los precios y edades sean positivos."*

### ⏱ Minuto 3:30 - 5:30 | Explicación del Código: Semana 2 (Herencia y Composición)
* *(Muestra en `modelo.py` la jerarquía de `Medico`, `MedicoGeneral`, `CirujanoEspecialista` y la clase `Clinica`)*.
* *"Para la Semana 2 implementamos **Herencia**: la clase base `Medico` define atributos comunes como salario y especialidad, mientras que `MedicoGeneral` y `CirujanoEspecialista` extienden de ella con `super().__init__()` y añaden comportamientos propios como el quirófano y bonos quirúrgicos."*
* *"También aplicamos **Composición** en la clase `Clinica`, la cual administra colecciones dinámicas de médicos, pacientes y medicamentos para consolidar la operación hospitalaria."*

### ⏱ Minuto 5:30 - 7:30 | Explicación del Código: Semana 3 (Clases Abstractas y Polimorfismo)
* *(Muestra la clase `PlanSalud` y sus hijas en `modelo.py`, y la clase `ConsultaMedica`)*.
* *"En la Semana 3 definimos la clase abstracta `PlanSalud` utilizando el módulo `abc.ABC` con métodos abstractos obligatorios `@abstractmethod def calcular_cobertura()` y `calcular_copago()`."*
* *"Las clases `PlanParticular`, `PlanSeguroPrivado` (80%) y `PlanConvenioSeguroPublico` (\$10 deducible) sobrescriben estos métodos."*
* *"El **Polimorfismo** se evidencia en la clase `ConsultaMedica`: al liquidar la cuenta, simplemente ejecuta `self.__plan_salud.calcular_copago(costo_bruto)`. **No existe ningún condicional `if/isinstance`**; Python resuelve la regla en tiempo de ejecución según el tipo real del plan asignado."*

### ⏱ Minuto 7:30 - 9:30 | Ejecución y Demostración en Vivo
* *(Abre la terminal de VS Code y ejecuta `python main.py`)*.
* *"Ahora ejecutamos el proyecto con `python main.py`. Como podemos observar en la salida:"*
  * *"Semana 1 pasa todas las pruebas y captura los datos inválidos con Pydantic."*
  * *"Semana 2 demuestra el funcionamiento de médicos y la clínica."*
  * *"Semana 3 bloquea la instanciación de la clase abstracta y genera los 3 comprobantes médicos calculando los descuentos de seguro de forma polimórfica y descontando el stock farmacéutico."*

### ⏱ Minuto 9:30 - 10:00 | Conclusión y Repositorio en GitHub
* *(Muestra el repositorio en el navegador o en Git)*.
* *"El código se encuentra subido en mi repositorio público de GitHub en la rama `main`, validado sin errores con el linter Ruff."*
* *"Muchas gracias por su atención."*

---

## 👨‍💻 Autor

**Luis Alberto Villegas Merchan**  
Estudiante de Ingeniería de Software / Sistemas
