# =============================================================================
# motor_inferencia.py
# Sistema Basado en Conocimiento — Diagnóstico de Fallas en Motocicletas
# Autores: Manuel Bermudez - Wilson Sarmiento
# Asignatura: Inteligencia Artificial II — Proyecto Final
# =============================================================================

import logging
from datetime import datetime
from base_conocimiento import (
    crear_base_conocimiento,
    SINTOMAS_ETIQUETAS,
    TIPO_FALLA_ETIQUETAS,
    DESCRIPCIONES_ACCION,
    DESCRIPCIONES_APTITUD,
    APTITUD_POR_URGENCIA,
    NIVEL_URGENCIA,
)

# -----------------------------------------------------------------------------
# Configuración del logger — registra cada paso de inferencia
# -----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
)
logger = logging.getLogger("motor_inferencia")


# =============================================================================
# MOTOR PRINCIPAL
# =============================================================================

def encadenamiento_adelante(hechos_iniciales: dict) -> tuple[dict, list]:
    """
    Aplica encadenamiento hacia adelante sobre los hechos iniciales.

    Soporta múltiples fallas simultáneas. La urgencia final es la más alta
    entre todas las fallas detectadas.

    Parámetros
    ----------
    hechos_iniciales : dict
        Diccionario {predicado: valor} con los síntomas observados.
        Ejemplo: {"bateria_descargada": True, "llanta_baja": True}

    Retorna
    -------
    hechos_finales : dict
        Hechos iniciales más todos los predicados derivados por el motor.
    traza : list[dict]
        Lista ordenada de cada paso de inferencia con regla, condiciones
        y conclusión.
    """
    base    = dict(hechos_iniciales)
    reglas  = crear_base_conocimiento()
    traza   = []

    tipos_detectados    = []
    urgencias_detectadas = []

    logger.info("=== INICIO DE INFERENCIA ===")
    logger.info("Hechos iniciales: %s", {k: v for k, v in base.items() if v is True})

    # -------------------------------------------------------------------------
    # FASE 1 — Detectar todos los tipos de falla (prioridad 0)
    # Recorre todas las reglas de clasificación; puede activar varias.
    # Detección de ciclos: si un tipo ya fue derivado, no se repite.
    # -------------------------------------------------------------------------
    reglas_p0 = [r for r in reglas if r["prioridad"] == 0]

    for r in reglas_p0:
        if _condiciones_satisfechas(base, r["condiciones"]):
            tipo = r["conclusion"][1]
            if tipo not in tipos_detectados:
                tipos_detectados.append(tipo)
                traza.append(_paso(r))
                logger.info("Regla %s activada → tipo_falla = %s", r["nombre"], tipo)

    base["tipo_fallas"] = tipos_detectados

    if not tipos_detectados:
        logger.info("Ninguna regla de clasificación activada.")
        return base, traza

    # -------------------------------------------------------------------------
    # FASE 2 — Determinar urgencia para cada tipo detectado (prioridad 1)
    # -------------------------------------------------------------------------
    reglas_p1 = [r for r in reglas if r["prioridad"] == 1]

    for tipo in tipos_detectados:
        base["tipo_falla"] = tipo
        for r in reglas_p1:
            if _condiciones_satisfechas(base, r["condiciones"]):
                urgencia = r["conclusion"][1]
                traza.append(_paso(r))
                logger.info("Regla %s activada → urgencia = %s (para %s)", r["nombre"], urgencia, tipo)
                if urgencia not in urgencias_detectadas:
                    urgencias_detectadas.append(urgencia)
                break  # una urgencia por tipo de falla es suficiente

    base.pop("tipo_falla", None)

    # -------------------------------------------------------------------------
    # FASE 3 — Acción y aptitud según la urgencia máxima (prioridad 2)
    # -------------------------------------------------------------------------
    if not urgencias_detectadas:
        logger.info("No se determinó urgencia.")
        return base, traza

    urgencia_max = max(urgencias_detectadas, key=lambda u: NIVEL_URGENCIA[u])
    base["urgencia"] = urgencia_max
    logger.info("Urgencia máxima seleccionada: %s", urgencia_max)

    reglas_p2 = [r for r in reglas if r["prioridad"] == 2]
    base["tipo_falla"] = urgencia_max  # reutiliza el campo para match

    for r in reglas_p2:
        if _condiciones_satisfechas(base, r["condiciones"]):
            clave, valor = r["conclusion"]
            base[clave] = valor
            traza.append(_paso(r))
            logger.info("Regla %s activada → %s = %s", r["nombre"], clave, valor)
            break

    base.pop("tipo_falla", None)

    # Aptitud de uso derivada de la urgencia máxima
    base["aptitud"] = APTITUD_POR_URGENCIA[urgencia_max]

    logger.info("=== FIN DE INFERENCIA ===")
    return base, traza


# =============================================================================
# FUNCIONES DE EXPLICACIÓN
# =============================================================================

def explicar_razonamiento(hechos: dict, traza: list) -> str:
    """
    Genera un reporte completo en texto plano del proceso de inferencia.

    Parámetros
    ----------
    hechos : dict   — hechos finales devueltos por encadenamiento_adelante
    traza  : list   — traza de pasos devuelta por encadenamiento_adelante

    Retorna
    -------
    str — reporte formateado listo para imprimir o mostrar en la interfaz
    """
    sep   = "=" * 62
    lines = []

    lines.append(sep)
    lines.append("  REPORTE DE DIAGNÓSTICO — SISTEMA BASADO EN CONOCIMIENTO")
    lines.append(f"  Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(sep)

    # Síntomas registrados
    lines.append("\nSÍNTOMAS REGISTRADOS:")
    sintomas_activos = [
        etiqueta
        for clave, etiqueta in SINTOMAS_ETIQUETAS.items()
        if hechos.get(clave) is True
    ]
    if sintomas_activos:
        for s in sintomas_activos:
            lines.append(f"  • {s}")
    else:
        lines.append("  (ninguno)")

    # Cadena de inferencia
    lines.append("\nCADENA DE INFERENCIA:")
    for i, paso in enumerate(traza, 1):
        conds = " Y ".join(f"{c[0]}={c[1]}" for c in paso["condiciones"])
        ck, cv = paso["conclusion"]
        lines.append(f"  Paso {i:02d} [{paso['regla']}]:")
        lines.append(f"    SI   {conds}")
        lines.append(f"    → ENTONCES {ck} = {cv}")

    # Fallas detectadas
    lines.append("\nFALLAS DETECTADAS:")
    for falla in hechos.get("tipo_fallas", []):
        etiqueta = TIPO_FALLA_ETIQUETAS.get(falla, falla)
        lines.append(f"  • {etiqueta}")

    # Urgencia
    urgencia = hechos.get("urgencia", "N/A")
    lines.append(f"\nURGENCIA MÁXIMA: {urgencia.upper()}")

    # Diagnóstico final
    lines.append("\nDIAGNÓSTICO FINAL:")
    accion  = hechos.get("accion_recomendada")
    aptitud = hechos.get("aptitud")
    if accion:
        lines.append(f"  Acción:  {DESCRIPCIONES_ACCION.get(accion, accion)}")
    if aptitud:
        lines.append(f"  Aptitud: {DESCRIPCIONES_APTITUD.get(aptitud, aptitud)}")

    lines.append(f"\n{sep}")
    return "\n".join(lines)


def porque(hecho_clave: str, valor_buscado, hechos: dict, traza: list) -> str:
    """
    Explica por qué se llegó a una conclusión específica.

    Parámetros
    ----------
    hecho_clave   : str   — predicado a explicar (ej. "urgencia")
    valor_buscado : any   — valor del predicado (ej. "alta")
    hechos        : dict  — hechos finales
    traza         : list  — traza de pasos

    Retorna
    -------
    str — explicación en lenguaje natural
    """
    valor_actual = hechos.get(hecho_clave)

    if valor_actual is None:
        return f"El predicado '{hecho_clave}' no fue derivado en esta inferencia."

    if valor_buscado is not None and valor_actual != valor_buscado:
        return (
            f"'{hecho_clave}' fue derivado con valor '{valor_actual}', "
            f"no '{valor_buscado}'."
        )

    lines = [f"¿Por qué {hecho_clave} = '{valor_actual}'?"]

    for paso in traza:
        ck, cv = paso["conclusion"]
        if ck == hecho_clave and cv == valor_actual:
            lines.append(f"  Regla [{paso['regla']}] — {paso.get('descripcion', '')}")
            lines.append("  porque se cumplieron las condiciones:")
            for cond in paso["condiciones"]:
                lines.append(f"    • {cond[0]} = {cond[1]}")
            return "\n".join(lines)

    # Si no está en traza es un hecho inicial
    return f"'{hecho_clave} = {valor_actual}' es un hecho inicial (no derivado)."


def sin_conclusion(hechos: dict) -> bool:
    """
    Retorna True si el motor no pudo derivar ninguna conclusión.
    Útil para mostrar un mensaje adecuado en la interfaz.
    """
    return not hechos.get("tipo_fallas")


# =============================================================================
# UTILIDADES INTERNAS
# =============================================================================

def _condiciones_satisfechas(base: dict, condiciones: list) -> bool:
    """Verifica si todas las condiciones de una regla se cumplen en base."""
    return all(base.get(clave) == valor for clave, valor in condiciones)


def _paso(regla: dict) -> dict:
    """Construye un registro de traza a partir de una regla activada."""
    return {
        "regla":       regla["nombre"],
        "descripcion": regla.get("descripcion", ""),
        "condiciones": regla["condiciones"],
        "conclusion":  regla["conclusion"],
        "prioridad":   regla["prioridad"],
        "certeza":     regla.get("certeza", 1.0),
    }
