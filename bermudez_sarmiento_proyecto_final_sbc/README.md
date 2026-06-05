# 🏍️ DiagMoto — Sistema Experto de Diagnóstico de Fallas en Motocicletas

**Asignatura:** Inteligencia Artificial II — Proyecto Final  
**Autores:** Manuel Bermudez · Wilson Sarmiento  
**Institución:** Fundación Universitaria Los Libertadores  
**Fecha:** 2026  

---

## Descripción

DiagMoto es un sistema basado en conocimiento (SBC) que diagnostica fallas en motocicletas mediante **encadenamiento hacia adelante**. El propietario selecciona los síntomas observados y el sistema aplica 27 reglas de producción formalizadas en lógica de predicados para determinar:

- **Tipo(s) de falla** detectados
- **Urgencia** de atención (alta / media / baja)
- **Acción recomendada** (ir al taller / programar mantenimiento / revisión básica)
- **Aptitud de uso** de la moto (no apta / precaución / apta)
- **Cadena de inferencia** completa con explicación de cada paso

El sistema soporta **múltiples fallas simultáneas** y selecciona la urgencia máxima entre todas las detectadas.

---

## Estructura del proyecto

```
bermudez_sarmiento_proyecto_final_sbc/
│
├── README.md                        # Este archivo
├── requirements.txt                 # Dependencias Python
│
├── src/
│   ├── base_conocimiento.py         # 27 reglas + 18 predicados del dominio
│   ├── motor_inferencia.py          # Motor: encadenamiento adelante, porque(), explicar()
│   └── app.py                       # Interfaz web Streamlit
│
├── docs/
│   ├── documentacion_tecnica.pdf    # Documentación técnica completa
│   └── manual_usuario.pdf           # Manual de usuario con capturas
│
└── tests/
    └── casos_prueba.md              # Tabla de validación con 8 casos de prueba
```

---

## Requisitos del sistema

- Python 3.8 o superior
- pip
- Conexión a internet (solo para cargar fuentes Google en la interfaz)

---

## Instalación

### 1. Clonar o descomprimir el proyecto

```bash
# Si descargaste el ZIP:
unzip bermudez_sarmiento_proyecto_final_sbc.zip
cd bermudez_sarmiento_proyecto_final_sbc
```

### 2. (Opcional) Crear entorno virtual

```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac / Linux:
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Cómo ejecutar la aplicación

```bash
cd src
streamlit run app.py
```

La aplicación abrirá automáticamente en el navegador en `http://localhost:8501`.

> **Nota:** si el navegador no abre automáticamente, copia y pega la URL en la barra de direcciones.

---

## Uso rápido

1. En el panel izquierdo, selecciona un **caso precargado** o marca síntomas manualmente.
2. Haz clic en **"Ejecutar diagnóstico"**.
3. El panel derecho muestra:
   - Fallas detectadas con sus badges de tipo
   - Urgencia máxima derivada
   - Diagnóstico final con aptitud de uso
   - Cadena de inferencia paso a paso
4. Expande **"¿Por qué?"** para ver la explicación detallada de cada conclusión.
5. Descarga el reporte completo con el botón al final.

---

## Base de conocimiento — resumen

| Grupo | Reglas | Descripción |
|-------|--------|-------------|
| Clasificación | R01 – R13 | Determinan el tipo de falla según síntomas |
| Urgencia | R14 – R24 | Asignan nivel de urgencia a cada tipo de falla |
| Acción | R25 – R27 | Definen acción recomendada y aptitud de uso |

**Síntomas soportados (12):** batería descargada, sin combustible, nivel de aceite bajo, humo azul, pastillas desgastadas, llanta baja, humo negro, cadena suelta, motor sobrecalentado, luces no encienden, aceite en el suelo, vibración excesiva.

---

## Tecnologías utilizadas

| Componente | Tecnología |
|---|---|
| Lenguaje | Python 3.8+ |
| Interfaz web | Streamlit |
| Motor de inferencia | Python puro (sin librerías externas) |
| Estilos | CSS personalizado dentro de Streamlit |

---

## Autores

| Nombre | Rol |
|---|---|
| Manuel Bermudez | Desarrollo del motor de inferencia, base de conocimiento e interfaz |
| Wilson Sarmiento | Diseño de reglas, validación de casos de prueba y documentación |

---

*Fundación Universitaria Los Libertadores · Inteligencia Artificial II · 2026*
