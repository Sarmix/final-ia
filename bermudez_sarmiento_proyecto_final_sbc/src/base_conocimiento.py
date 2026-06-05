# =============================================================================
# base_conocimiento.py
# Sistema Basado en Conocimiento — Diagnóstico de Fallas en Motocicletas
# Autores: Manuel Bermudez - Wilson Sarmiento
# Asignatura: Inteligencia Artificial II — Proyecto Final
# =============================================================================

# -----------------------------------------------------------------------------
# PREDICADOS DEL DOMINIO
# 18 predicados que representan los conceptos fundamentales del sistema
# -----------------------------------------------------------------------------

PREDICADOS = {
    # --- Síntomas observables (predicados de entrada) ---
    "bateria_descargada":    "La moto no arranca por batería sin carga",
    "sin_combustible":       "La moto no arranca por falta de combustible",
    "nivel_aceite_bajo":     "Nivel de aceite por debajo del mínimo recomendado",
    "humo_azul":             "Emite humo azul por el escape (aceite quemado)",
    "pastillas_desgastadas": "Pastillas de freno al límite de desgaste",
    "llanta_baja":           "Presión de llanta por debajo de lo recomendado",
    "humo_negro":            "Emite humo negro (mezcla rica en combustible)",
    "cadena_suelta":         "Cadena de transmisión con holgura excesiva",
    "motor_sobrecalentado":  "Motor alcanza temperatura anormalmente alta",
    "luz_no_enciende":       "Faro o luz de stop no funcionan",
    "aceite_en_suelo":       "Manchas de aceite visibles bajo la moto",
    "vibracion_excesiva":    "Vibración inusual en manillar o chasis",

    # --- Predicados derivados (conclusiones del motor) ---
    "tipo_falla":           "Categoría de falla detectada",
    "urgencia":             "Nivel de urgencia de atención requerida",
    "accion_recomendada":   "Acción concreta que debe tomar el propietario",
    "aptitud":              "Estado de aptitud de la moto para circular",
    "tipo_fallas":          "Lista de todas las fallas detectadas simultáneamente",
}

# Etiquetas legibles para mostrar en la interfaz
SINTOMAS_ETIQUETAS = {
    "bateria_descargada":    "Batería descargada / no enciende",
    "sin_combustible":       "Sin combustible",
    "nivel_aceite_bajo":     "Nivel de aceite bajo",
    "humo_azul":             "Humo azul por el escape",
    "pastillas_desgastadas": "Pastillas de freno desgastadas",
    "llanta_baja":           "Presión de llanta baja",
    "humo_negro":            "Humo negro por el escape",
    "cadena_suelta":         "Cadena de transmisión suelta",
    "motor_sobrecalentado":  "Motor sobrecalentado",
    "luz_no_enciende":       "Luces no encienden",
    "aceite_en_suelo":       "Manchas de aceite en el suelo",
    "vibracion_excesiva":    "Vibración excesiva en manillar",
}

# Etiquetas para tipos de falla
TIPO_FALLA_ETIQUETAS = {
    "electrica":        "Eléctrica (batería)",
    "combustible":      "Combustible",
    "mecanica":         "Mecánica (motor / anillos)",
    "frenos":           "Frenos",
    "neumaticos":       "Neumáticos",
    "carburacion":      "Carburación / inyección",
    "transmision":      "Transmisión (cadena)",
    "refrigeracion":    "Refrigeración (sobrecalentamiento)",
    "electrica_luces":  "Eléctrica (sistema de luces)",
    "fuga_aceite":      "Fuga de aceite",
    "desbalance":       "Desbalance / vibración",
}

# Descripciones de acciones recomendadas
DESCRIPCIONES_ACCION = {
    "ir_taller_inmediato":     "Llevar al taller de inmediato. NO usar la moto.",
    "programar_mantenimiento": "Programar mantenimiento pronto. Usar con precaución.",
    "revision_basica":         "Revisión básica suficiente. Puede seguir usando la moto.",
}

# Descripciones de aptitud de uso
DESCRIPCIONES_APTITUD = {
    "no_apta_para_uso":    "NO APTA — No debe circular hasta ser reparada.",
    "usar_con_precaucion": "PRECAUCIÓN — Solo trayectos cortos y baja velocidad.",
    "apta_para_uso":       "APTA — Puede circular con normalidad.",
}

# Nivel numérico de urgencia para comparación
NIVEL_URGENCIA = {"alta": 2, "media": 1, "baja": 0}

# Aptitud resultante según urgencia máxima
APTITUD_POR_URGENCIA = {
    "alta":  "no_apta_para_uso",
    "media": "usar_con_precaucion",
    "baja":  "apta_para_uso",
}


# -----------------------------------------------------------------------------
# REGLAS DE PRODUCCIÓN
# 25 reglas organizadas en 3 grupos por prioridad de ejecución:
#   Prioridad 0 → Clasificación del tipo de falla
#   Prioridad 1 → Determinación de urgencia
#   Prioridad 2 → Acción recomendada y aptitud de uso
# -----------------------------------------------------------------------------

def crear_base_conocimiento():
    """
    Retorna las 25 reglas del dominio ordenadas por prioridad de ejecución.

    Cada regla es un diccionario con:
        nombre      : identificador único (R01 … R25)
        descripcion : texto explicativo de la regla
        condiciones : lista de tuplas (predicado, valor_esperado)
        conclusion  : tupla (predicado, valor_derivado)
        prioridad   : entero 0|1|2 — orden de ejecución del motor
        certeza     : factor de certeza (1.0 = determinista)
    """

    def regla(nombre, descripcion, condiciones, conclusion, prioridad, certeza=1.0):
        return {
            "nombre":      nombre,
            "descripcion": descripcion,
            "condiciones": condiciones,
            "conclusion":  conclusion,
            "prioridad":   prioridad,
            "certeza":     certeza,
        }

    reglas = []

    # =========================================================================
    # GRUPO 1 — Clasificación del tipo de falla (prioridad 0)
    # =========================================================================

    reglas.append(regla(
        "R01",
        "Falla eléctrica por batería descargada",
        [("bateria_descargada", True)],
        ("tipo_falla", "electrica"),
        prioridad=0,
    ))

    reglas.append(regla(
        "R02",
        "Falla de combustible por depósito vacío",
        [("sin_combustible", True)],
        ("tipo_falla", "combustible"),
        prioridad=0,
    ))

    reglas.append(regla(
        "R03",
        "Falla mecánica por aceite bajo y humo azul (desgaste de anillos)",
        [("nivel_aceite_bajo", True), ("humo_azul", True)],
        ("tipo_falla", "mecanica"),
        prioridad=0,
    ))

    reglas.append(regla(
        "R04",
        "Falla de frenos por pastillas al límite de desgaste",
        [("pastillas_desgastadas", True)],
        ("tipo_falla", "frenos"),
        prioridad=0,
    ))

    reglas.append(regla(
        "R05",
        "Falla de neumáticos por presión insuficiente",
        [("llanta_baja", True)],
        ("tipo_falla", "neumaticos"),
        prioridad=0,
    ))

    reglas.append(regla(
        "R06",
        "Falla de carburación por mezcla rica (humo negro)",
        [("humo_negro", True)],
        ("tipo_falla", "carburacion"),
        prioridad=0,
    ))

    reglas.append(regla(
        "R07",
        "Falla mecánica grave: aceite bajo sin humo azul (riesgo de gripado)",
        [("nivel_aceite_bajo", True), ("humo_azul", False)],
        ("tipo_falla", "mecanica"),
        prioridad=0,
        certeza=0.85,
    ))

    reglas.append(regla(
        "R08",
        "Falla de transmisión por cadena de transmisión suelta",
        [("cadena_suelta", True)],
        ("tipo_falla", "transmision"),
        prioridad=0,
    ))

    reglas.append(regla(
        "R09",
        "Falla de refrigeración por motor sobrecalentado",
        [("motor_sobrecalentado", True)],
        ("tipo_falla", "refrigeracion"),
        prioridad=0,
    ))

    reglas.append(regla(
        "R10",
        "Falla eléctrica en sistema de luces",
        [("luz_no_enciende", True)],
        ("tipo_falla", "electrica_luces"),
        prioridad=0,
    ))

    reglas.append(regla(
        "R11",
        "Fuga de aceite detectada por manchas en el suelo",
        [("aceite_en_suelo", True)],
        ("tipo_falla", "fuga_aceite"),
        prioridad=0,
    ))

    reglas.append(regla(
        "R12",
        "Desbalance o vibración excesiva en manillar o chasis",
        [("vibracion_excesiva", True)],
        ("tipo_falla", "desbalance"),
        prioridad=0,
    ))

    reglas.append(regla(
        "R13",
        "Fuga crítica de aceite: aceite en suelo y nivel bajo (fuga activa grave)",
        [("aceite_en_suelo", True), ("nivel_aceite_bajo", True)],
        ("tipo_falla", "mecanica"),
        prioridad=0,
        certeza=0.95,
    ))

    # =========================================================================
    # GRUPO 2 — Determinación de urgencia (prioridad 1)
    # =========================================================================

    reglas.append(regla(
        "R14",
        "Urgencia alta para falla mecánica (riesgo de daño catastrófico al motor)",
        [("tipo_falla", "mecanica")],
        ("urgencia", "alta"),
        prioridad=1,
    ))

    reglas.append(regla(
        "R15",
        "Urgencia alta para falla de frenos (riesgo directo de accidente)",
        [("tipo_falla", "frenos")],
        ("urgencia", "alta"),
        prioridad=1,
    ))

    reglas.append(regla(
        "R16",
        "Urgencia alta para falla de refrigeración (riesgo de gripado)",
        [("tipo_falla", "refrigeracion")],
        ("urgencia", "alta"),
        prioridad=1,
    ))

    reglas.append(regla(
        "R17",
        "Urgencia alta para fuga de aceite (pérdida de lubricación)",
        [("tipo_falla", "fuga_aceite")],
        ("urgencia", "alta"),
        prioridad=1,
    ))

    reglas.append(regla(
        "R18",
        "Urgencia media para falla eléctrica de batería",
        [("tipo_falla", "electrica")],
        ("urgencia", "media"),
        prioridad=1,
    ))

    reglas.append(regla(
        "R19",
        "Urgencia media para falla de neumáticos",
        [("tipo_falla", "neumaticos")],
        ("urgencia", "media"),
        prioridad=1,
    ))

    reglas.append(regla(
        "R20",
        "Urgencia media para falla de transmisión (cadena)",
        [("tipo_falla", "transmision")],
        ("urgencia", "media"),
        prioridad=1,
    ))

    reglas.append(regla(
        "R21",
        "Urgencia media para falla eléctrica del sistema de luces",
        [("tipo_falla", "electrica_luces")],
        ("urgencia", "media"),
        prioridad=1,
    ))

    reglas.append(regla(
        "R22",
        "Urgencia baja para falla de combustible (no implica daño mecánico)",
        [("tipo_falla", "combustible")],
        ("urgencia", "baja"),
        prioridad=1,
    ))

    reglas.append(regla(
        "R23",
        "Urgencia baja para falla de carburación",
        [("tipo_falla", "carburacion")],
        ("urgencia", "baja"),
        prioridad=1,
    ))

    reglas.append(regla(
        "R24",
        "Urgencia baja para desbalance o vibración leve",
        [("tipo_falla", "desbalance")],
        ("urgencia", "baja"),
        prioridad=1,
    ))

    # =========================================================================
    # GRUPO 3 — Acción recomendada (prioridad 2)
    # =========================================================================

    reglas.append(regla(
        "R25",
        "Acción inmediata para urgencia alta: taller y no circulación",
        [("urgencia", "alta")],
        ("accion_recomendada", "ir_taller_inmediato"),
        prioridad=2,
    ))

    reglas.append(regla(
        "R26",
        "Acción programada para urgencia media: mantenimiento próximo",
        [("urgencia", "media")],
        ("accion_recomendada", "programar_mantenimiento"),
        prioridad=2,
    ))

    reglas.append(regla(
        "R27",
        "Revisión básica suficiente para urgencia baja",
        [("urgencia", "baja")],
        ("accion_recomendada", "revision_basica"),
        prioridad=2,
    ))

    return sorted(reglas, key=lambda r: r["prioridad"])
