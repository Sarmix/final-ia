# =============================================================================
# app.py
# Sistema Basado en Conocimiento — Diagnóstico de Fallas en Motocicletas
# Interfaz web con Streamlit
# Autores: Manuel Bermudez - Wilson Sarmiento
# Asignatura: Inteligencia Artificial II — Proyecto Final
# =============================================================================

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from motor_inferencia import (
    encadenamiento_adelante,
    explicar_razonamiento,
    porque,
    sin_conclusion,
)
from base_conocimiento import (
    SINTOMAS_ETIQUETAS,
    TIPO_FALLA_ETIQUETAS,
    DESCRIPCIONES_ACCION,
    DESCRIPCIONES_APTITUD,
)

# =============================================================================
# CONFIGURACIÓN DE PÁGINA
# =============================================================================
st.set_page_config(
    page_title="DiagMoto — Sistema Experto",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =============================================================================
# ESTILOS CSS
# =============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Fondo general */
.stApp {
    background: #0f1117;
    color: #e8eaf0;
}

/* Header principal */
.header-block {
    background: linear-gradient(135deg, #1a1f2e 0%, #0f1117 60%, #1a1220 100%);
    border: 1px solid #2a2f40;
    border-radius: 16px;
    padding: 36px 40px 28px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.header-block::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(255,140,0,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.header-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 6px;
    letter-spacing: -0.5px;
}
.header-title span { color: #ff8c00; }
.header-sub {
    font-size: 0.95rem;
    color: #8891a8;
    margin: 0;
    font-weight: 300;
}
.header-badge {
    display: inline-block;
    background: rgba(255,140,0,0.15);
    border: 1px solid rgba(255,140,0,0.35);
    color: #ff8c00;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 14px;
    text-transform: uppercase;
}

/* Secciones */
.section-card {
    background: #161b27;
    border: 1px solid #232840;
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 20px;
}
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #c8cdd8;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    margin: 0 0 18px;
    padding-bottom: 10px;
    border-bottom: 1px solid #232840;
}

/* Checkboxes */
.stCheckbox label {
    color: #c8cdd8 !important;
    font-size: 0.9rem !important;
}
.stCheckbox label:hover { color: #ffffff !important; }

/* Botón principal */
.stButton > button {
    background: linear-gradient(135deg, #ff8c00, #e07000) !important;
    color: #ffffff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.5px !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 32px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(255,140,0,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 28px rgba(255,140,0,0.45) !important;
}

/* Botón secundario */
.stButton.secondary > button {
    background: transparent !important;
    border: 1px solid #2a2f40 !important;
    color: #8891a8 !important;
    box-shadow: none !important;
}

/* Tarjetas de resultado */
.result-card {
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 14px;
    border: 1px solid;
}
.result-alta {
    background: rgba(220,38,38,0.08);
    border-color: rgba(220,38,38,0.3);
}
.result-media {
    background: rgba(245,158,11,0.08);
    border-color: rgba(245,158,11,0.3);
}
.result-baja {
    background: rgba(16,185,129,0.08);
    border-color: rgba(16,185,129,0.3);
}

/* Badges de urgencia */
.badge-alta  { background:#7f1d1d; color:#fca5a5; padding:4px 14px; border-radius:20px; font-size:0.8rem; font-weight:600; }
.badge-media { background:#78350f; color:#fcd34d; padding:4px 14px; border-radius:20px; font-size:0.8rem; font-weight:600; }
.badge-baja  { background:#064e3b; color:#6ee7b7; padding:4px 14px; border-radius:20px; font-size:0.8rem; font-weight:600; }

/* Badges de tipo falla */
.badge-tipo {
    display: inline-block;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.3);
    color: #a5b4fc;
    font-size: 0.78rem;
    padding: 3px 12px;
    border-radius: 20px;
    margin: 3px 3px 3px 0;
}

/* Pasos de inferencia */
.paso-item {
    background: #1a1f2e;
    border-left: 3px solid #ff8c00;
    border-radius: 0 8px 8px 0;
    padding: 10px 16px;
    margin-bottom: 8px;
    font-size: 0.85rem;
    font-family: 'DM Mono', monospace;
    color: #c8cdd8;
}
.paso-regla { color: #ff8c00; font-weight: 700; }
.paso-cond  { color: #8891a8; }
.paso-conc  { color: #6ee7b7; }

/* Aptitud final */
.aptitud-box {
    border-radius: 12px;
    padding: 22px 26px;
    text-align: center;
    margin-top: 6px;
}
.aptitud-no_apta {
    background: rgba(220,38,38,0.12);
    border: 2px solid rgba(220,38,38,0.4);
}
.aptitud-precaucion {
    background: rgba(245,158,11,0.12);
    border: 2px solid rgba(245,158,11,0.4);
}
.aptitud-apta {
    background: rgba(16,185,129,0.12);
    border: 2px solid rgba(16,185,129,0.4);
}
.aptitud-icon { font-size: 2.2rem; margin-bottom: 8px; }
.aptitud-label {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 800;
    letter-spacing: 1px;
}

/* Separador */
hr { border-color: #232840 !important; }

/* Ocultar elementos de Streamlit */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# CASOS DE PRUEBA PRECARGADOS
# =============================================================================
CASOS_PRECARGADOS = {
    "Seleccionar caso...": {},
    "C1 — Batería descargada":              {"bateria_descargada": True},
    "C2 — Falla mecánica (aceite + humo)":  {"nivel_aceite_bajo": True, "humo_azul": True},
    "C3 — Frenos desgastados":              {"pastillas_desgastadas": True},
    "C4 — Sin combustible":                 {"sin_combustible": True},
    "C5 — Motor sobrecalentado":            {"motor_sobrecalentado": True},
    "C6 — Cadena suelta + llanta baja":     {"cadena_suelta": True, "llanta_baja": True},
    "C7 — Fuga de aceite activa":           {"aceite_en_suelo": True, "nivel_aceite_bajo": True},
    "C8 — Múltiples fallas (caso crítico)": {"pastillas_desgastadas": True, "motor_sobrecalentado": True, "llanta_baja": True},
}

APTITUD_CONFIG = {
    "no_apta_para_uso":    ("aptitud-no_apta",    "🔴", "NO APTA PARA CIRCULAR", "#fca5a5"),
    "usar_con_precaucion": ("aptitud-precaucion",  "🟡", "USAR CON PRECAUCIÓN",   "#fcd34d"),
    "apta_para_uso":       ("aptitud-apta",        "🟢", "APTA PARA CIRCULAR",    "#6ee7b7"),
}

URGENCIA_BADGE = {
    "alta":  "badge-alta",
    "media": "badge-media",
    "baja":  "badge-baja",
}


# =============================================================================
# HEADER
# =============================================================================
st.markdown("""
<div class="header-block">
    <div class="header-badge">Sistema Basado en Conocimiento · IA II</div>
    <h1 class="header-title">Diag<span>Moto</span></h1>
    <p class="header-sub">
        Diagnóstico experto de fallas en motocicletas mediante encadenamiento hacia adelante.<br>
        Selecciona los síntomas observados y obtén un diagnóstico inmediato con trazabilidad completa.
    </p>
</div>
""", unsafe_allow_html=True)


# =============================================================================
# LAYOUT PRINCIPAL: 2 columnas
# =============================================================================
col_izq, col_der = st.columns([1, 1.4], gap="large")


# =============================================================================
# COLUMNA IZQUIERDA — Entrada de síntomas
# =============================================================================
with col_izq:

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-title">① Casos de prueba precargados</p>', unsafe_allow_html=True)

    caso_sel = st.selectbox(
        "Cargar caso:",
        list(CASOS_PRECARGADOS.keys()),
        label_visibility="collapsed",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Determinar valores iniciales según caso seleccionado
    caso_hechos = CASOS_PRECARGADOS.get(caso_sel, {})

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-title">② Selecciona los síntomas observados</p>', unsafe_allow_html=True)

    sintomas_seleccionados = {}
    for clave, etiqueta in SINTOMAS_ETIQUETAS.items():
        valor_defecto = caso_hechos.get(clave, False)
        sintomas_seleccionados[clave] = st.checkbox(
            etiqueta,
            value=valor_defecto,
            key=f"cb_{clave}_{caso_sel}",
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # Botones
    col_btn1, col_btn2 = st.columns([2, 1])
    with col_btn1:
        ejecutar = st.button("🔍  Ejecutar diagnóstico", use_container_width=True)
    with col_btn2:
        limpiar = st.button("↺  Limpiar", use_container_width=True)

    if limpiar:
        st.rerun()


# =============================================================================
# COLUMNA DERECHA — Resultados
# =============================================================================
with col_der:

    hechos_activos = {k: True for k, v in sintomas_seleccionados.items() if v}

    if not ejecutar and not hechos_activos:
        # Estado inicial — instrucciones
        st.markdown("""
        <div style="
            background:#161b27; border:1px dashed #2a2f40;
            border-radius:14px; padding:48px 32px; text-align:center; color:#4a5068;">
            <div style="font-size:2.8rem; margin-bottom:16px">🏍️</div>
            <p style="font-family:'Syne',sans-serif; font-size:1rem; font-weight:700;
               color:#6b7280; letter-spacing:1px; text-transform:uppercase;">
               Selecciona síntomas y ejecuta el diagnóstico
            </p>
            <p style="font-size:0.85rem; margin-top:8px; color:#3d4461;">
                Puedes usar un caso precargado o marcar síntomas manualmente.
            </p>
        </div>
        """, unsafe_allow_html=True)

    elif ejecutar or hechos_activos:

        if not hechos_activos:
            st.warning("⚠️ Selecciona al menos un síntoma antes de ejecutar.")
        else:
            hechos_finales, traza = encadenamiento_adelante(hechos_activos)

            # ------------------------------------------------------------------
            # Sin conclusión
            # ------------------------------------------------------------------
            if sin_conclusion(hechos_finales):
                st.markdown("""
                <div class="result-card result-baja">
                    <p style="font-family:'Syne',sans-serif; font-weight:700; color:#fcd34d; margin:0 0 6px">
                        ⚠️ Sin conclusión derivable
                    </p>
                    <p style="color:#8891a8; font-size:0.88rem; margin:0">
                        Los síntomas seleccionados no activan ninguna regla del sistema.
                        Intenta con una combinación diferente.
                    </p>
                </div>
                """, unsafe_allow_html=True)

            else:
                fallas    = hechos_finales.get("tipo_fallas", [])
                urgencia  = hechos_finales.get("urgencia", "")
                accion    = hechos_finales.get("accion_recomendada", "")
                aptitud   = hechos_finales.get("aptitud", "")

                # --------------------------------------------------------------
                # TARJETA — Fallas detectadas + Urgencia
                # --------------------------------------------------------------
                clase_card = f"result-{urgencia}"
                badge_urg  = URGENCIA_BADGE.get(urgencia, "badge-baja")
                badges_tipo = "".join(
                    f'<span class="badge-tipo">{TIPO_FALLA_ETIQUETAS.get(f, f)}</span>'
                    for f in fallas
                )

                st.markdown(f"""
                <div class="section-card" style="margin-bottom:14px">
                    <p class="section-title">③ Fallas detectadas</p>
                    <div style="margin-bottom:12px">{badges_tipo}</div>
                    <div style="display:flex; align-items:center; gap:10px">
                        <span style="color:#8891a8; font-size:0.85rem">Urgencia máxima:</span>
                        <span class="{badge_urg}">{urgencia.upper()}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # --------------------------------------------------------------
                # TARJETA — Aptitud de uso
                # --------------------------------------------------------------
                apt_class, apt_icon, apt_label, apt_color = APTITUD_CONFIG.get(
                    aptitud, ("aptitud-baja", "⚪", "DESCONOCIDA", "#ccc")
                )
                accion_texto = DESCRIPCIONES_ACCION.get(accion, accion)

                st.markdown(f"""
                <div class="section-card" style="margin-bottom:14px">
                    <p class="section-title">④ Diagnóstico final</p>
                    <div class="aptitud-box {apt_class}">
                        <div class="aptitud-icon">{apt_icon}</div>
                        <div class="aptitud-label" style="color:{apt_color}">{apt_label}</div>
                        <div style="color:#8891a8; font-size:0.85rem; margin-top:8px">{accion_texto}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # --------------------------------------------------------------
                # TARJETA — Cadena de inferencia
                # --------------------------------------------------------------
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<p class="section-title">⑤ Cadena de inferencia</p>', unsafe_allow_html=True)

                for i, paso in enumerate(traza, 1):
                    conds = " ∧ ".join(f"{c[0]}={c[1]}" for c in paso["condiciones"])
                    ck, cv = paso["conclusion"]
                    certeza = paso.get("certeza", 1.0)
                    cert_str = f" <span style='color:#4a5068;font-size:0.75rem'>[CF={certeza:.2f}]</span>" if certeza < 1.0 else ""
                    st.markdown(f"""
                    <div class="paso-item">
                        <span class="paso-regla">[{paso['regla']}]</span>
                        <span class="paso-cond"> SI {conds}</span>
                        → <span class="paso-conc">ENTONCES {ck} = {cv}</span>{cert_str}
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

                # --------------------------------------------------------------
                # SECCIÓN — ¿Por qué? (explicación detallada)
                # --------------------------------------------------------------
                with st.expander("❓ ¿Por qué se llegó a estas conclusiones?"):
                    col_p1, col_p2 = st.columns(2)
                    with col_p1:
                        exp_urgencia = porque("urgencia", urgencia, hechos_finales, traza)
                        st.markdown(f"""
                        <div style="background:#1a1f2e; border-radius:10px; padding:14px 16px;
                             font-size:0.83rem; color:#c8cdd8; font-family:monospace; white-space:pre-wrap">
{exp_urgencia}
                        </div>""", unsafe_allow_html=True)
                    with col_p2:
                        exp_accion = porque("accion_recomendada", accion, hechos_finales, traza)
                        st.markdown(f"""
                        <div style="background:#1a1f2e; border-radius:10px; padding:14px 16px;
                             font-size:0.83rem; color:#c8cdd8; font-family:monospace; white-space:pre-wrap">
{exp_accion}
                        </div>""", unsafe_allow_html=True)

                # --------------------------------------------------------------
                # REPORTE COMPLETO (descargable)
                # --------------------------------------------------------------
                reporte = explicar_razonamiento(hechos_finales, traza)
                st.download_button(
                    label="⬇️  Descargar reporte completo (.txt)",
                    data=reporte,
                    file_name="diagnostico_moto.txt",
                    mime="text/plain",
                    use_container_width=True,
                )


# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#3d4461; font-size:0.78rem; padding:8px 0">
    DiagMoto · Sistema Basado en Conocimiento · Inteligencia Artificial II<br>
    Manuel Bermudez &amp; Wilson Sarmiento · Fundación Universitaria Los Libertadores · 2026
</div>
""", unsafe_allow_html=True)
