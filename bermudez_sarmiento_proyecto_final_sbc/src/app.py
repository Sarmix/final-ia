# =============================================================================
# app.py — DiagMoto v2
# Sistema Basado en Conocimiento — Diagnóstico de Fallas en Motocicletas
# Autores: Manuel Bermudez - Wilson Sarmiento
# =============================================================================

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from motor_inferencia import encadenamiento_adelante, explicar_razonamiento, porque, sin_conclusion
from base_conocimiento import SINTOMAS_ETIQUETAS, TIPO_FALLA_ETIQUETAS, DESCRIPCIONES_ACCION, DESCRIPCIONES_APTITUD

st.set_page_config(page_title="DiagMoto", page_icon="🏍️", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
    font-family: 'Space Grotesk', sans-serif !important;
    background: #080b14 !important;
    color: #e2e8f0 !important;
}

/* ── FONDO con grid ── */
.stApp::before {
    content: '';
    position: fixed; inset: 0; z-index: 0;
    background-image:
        linear-gradient(rgba(99,102,241,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,102,241,0.04) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
}

.block-container { position: relative; z-index: 1; padding: 2rem 3rem 3rem !important; max-width: 1400px !important; }

/* ── HEADER ── */
.dm-header {
    display: flex; align-items: flex-start; justify-content: space-between;
    padding: 2.5rem 3rem;
    background: linear-gradient(135deg, #0d1117 0%, #0f172a 50%, #0d1117 100%);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 20px;
    margin-bottom: 2rem;
    position: relative; overflow: hidden;
}
.dm-header::after {
    content: '';
    position: absolute; top: -80px; right: -80px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 65%);
    border-radius: 50%;
}
.dm-logo { font-size: 3rem; font-weight: 700; letter-spacing: -2px; line-height: 1; }
.dm-logo span { color: #6366f1; }
.dm-logo sub { font-size: 1rem; font-weight: 300; color: #475569; letter-spacing: 0; vertical-align: middle; margin-left: 8px; }
.dm-desc { font-size: 0.88rem; color: #475569; margin-top: 8px; font-weight: 300; line-height: 1.6; }
.dm-pill {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.25);
    color: #818cf8; font-size: 0.7rem; font-weight: 600;
    letter-spacing: 1.5px; text-transform: uppercase;
    padding: 5px 14px; border-radius: 100px; margin-bottom: 12px;
}
.dm-stats {
    display: flex; flex-direction: column; align-items: flex-end; gap: 8px;
    z-index: 1;
}
.dm-stat { text-align: right; }
.dm-stat-n { font-size: 1.8rem; font-weight: 700; color: #6366f1; line-height: 1; }
.dm-stat-l { font-size: 0.68rem; color: #334155; text-transform: uppercase; letter-spacing: 1px; }

/* ── PANEL CARD ── */
.dm-card {
    background: #0d1117;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1rem;
    position: relative;
}
.dm-card-title {
    font-size: 0.65rem; font-weight: 600;
    letter-spacing: 2px; text-transform: uppercase;
    color: #334155; margin-bottom: 1.2rem;
    display: flex; align-items: center; gap: 8px;
}
.dm-card-title::after {
    content: ''; flex: 1; height: 1px;
    background: rgba(255,255,255,0.05);
}

/* ── CHECKBOXES ── */
.stCheckbox { margin-bottom: 2px !important; }
.stCheckbox label {
    color: #94a3b8 !important; font-size: 0.87rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    transition: color 0.15s;
}
.stCheckbox label:hover { color: #e2e8f0 !important; }
.stCheckbox [data-testid="stCheckbox"] { gap: 10px !important; }

/* ── SELECTBOX ── */
.stSelectbox > div > div {
    background: #0f172a !important;
    border: 1px solid rgba(99,102,241,0.2) !important;
    border-radius: 10px !important;
    color: #94a3b8 !important;
    font-size: 0.87rem !important;
}

/* ── BOTONES ── */
.stButton > button {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important; font-size: 0.87rem !important;
    border-radius: 10px !important; border: none !important;
    transition: all 0.2s ease !important;
}
.stButton:first-child > button {
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    color: #fff !important;
    box-shadow: 0 0 20px rgba(99,102,241,0.3), inset 0 1px 0 rgba(255,255,255,0.1) !important;
    padding: 0.65rem 1.5rem !important;
}
.stButton:first-child > button:hover {
    box-shadow: 0 0 35px rgba(99,102,241,0.5), inset 0 1px 0 rgba(255,255,255,0.15) !important;
    transform: translateY(-1px) !important;
}
.stButton:last-child > button {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #475569 !important;
}
.stButton:last-child > button:hover {
    border-color: rgba(255,255,255,0.15) !important;
    color: #94a3b8 !important;
}

/* ── RESULTADO: estado vacío ── */
.dm-empty {
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    padding: 4rem 2rem; text-align: center;
    border: 1px dashed rgba(255,255,255,0.06); border-radius: 16px;
    background: #0d1117;
}
.dm-empty-icon { font-size: 3rem; margin-bottom: 1rem; opacity: 0.3; }
.dm-empty-text { font-size: 0.8rem; color: #1e293b; text-transform: uppercase; letter-spacing: 2px; font-weight: 600; }

/* ── BADGES FALLA ── */
.dm-badge-falla {
    display: inline-flex; align-items: center;
    background: rgba(99,102,241,0.08);
    border: 1px solid rgba(99,102,241,0.2);
    color: #818cf8; font-size: 0.75rem; font-weight: 600;
    padding: 4px 14px; border-radius: 100px; margin: 3px 4px 3px 0;
    letter-spacing: 0.3px;
}

/* ── URGENCIA ── */
.dm-urg {
    display: inline-flex; align-items: center; gap: 6px;
    font-size: 0.72rem; font-weight: 700; letter-spacing: 1.5px;
    text-transform: uppercase; padding: 5px 16px; border-radius: 100px;
}
.dm-urg-alta   { background: rgba(239,68,68,0.12);  border: 1px solid rgba(239,68,68,0.3);  color: #f87171; }
.dm-urg-media  { background: rgba(234,179,8,0.12);  border: 1px solid rgba(234,179,8,0.3);  color: #facc15; }
.dm-urg-baja   { background: rgba(34,197,94,0.12);  border: 1px solid rgba(34,197,94,0.3);  color: #4ade80; }

/* ── APTITUD BOX ── */
.dm-apt {
    border-radius: 14px; padding: 1.8rem;
    text-align: center; margin: 0.5rem 0;
}
.dm-apt-icon { font-size: 2.5rem; margin-bottom: 0.6rem; }
.dm-apt-label {
    font-size: 1rem; font-weight: 700; letter-spacing: 1px;
    text-transform: uppercase; margin-bottom: 0.4rem;
}
.dm-apt-desc { font-size: 0.8rem; opacity: 0.7; font-weight: 300; }
.dm-apt-alta   { background: rgba(239,68,68,0.07);  border: 1px solid rgba(239,68,68,0.2);  }
.dm-apt-alta .dm-apt-label   { color: #f87171; }
.dm-apt-media  { background: rgba(234,179,8,0.07);  border: 1px solid rgba(234,179,8,0.2);  }
.dm-apt-media .dm-apt-label  { color: #facc15; }
.dm-apt-baja   { background: rgba(34,197,94,0.07);  border: 1px solid rgba(34,197,94,0.2);  }
.dm-apt-baja .dm-apt-label   { color: #4ade80; }

/* ── CADENA DE INFERENCIA ── */
.dm-step {
    display: flex; align-items: flex-start; gap: 12px;
    padding: 10px 14px; border-radius: 10px;
    background: #080b14; border: 1px solid rgba(255,255,255,0.04);
    margin-bottom: 6px; font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem; line-height: 1.5;
}
.dm-step-num {
    min-width: 22px; height: 22px;
    background: rgba(99,102,241,0.15); border: 1px solid rgba(99,102,241,0.3);
    border-radius: 6px; color: #6366f1; font-weight: 600;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.65rem; flex-shrink: 0; margin-top: 1px;
}
.dm-step-regla { color: #6366f1; font-weight: 600; }
.dm-step-cond  { color: #64748b; }
.dm-step-arrow { color: #334155; }
.dm-step-conc  { color: #4ade80; }
.dm-step-cf    { color: #334155; font-size: 0.68rem; }

/* ── PORQUE ── */
.dm-porque {
    background: #080b14; border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px; padding: 1rem 1.2rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem; color: #64748b; line-height: 1.8;
    white-space: pre-wrap;
}

/* ── DOWNLOAD ── */
.stDownloadButton > button {
    background: transparent !important;
    border: 1px solid rgba(99,102,241,0.25) !important;
    color: #6366f1 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.82rem !important; font-weight: 500 !important;
    border-radius: 10px !important; width: 100% !important;
    margin-top: 0.5rem !important;
}
.stDownloadButton > button:hover {
    background: rgba(99,102,241,0.08) !important;
    border-color: rgba(99,102,241,0.4) !important;
}

/* ── EXPANDER ── */
.streamlit-expanderHeader {
    background: #0d1117 !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 10px !important;
    color: #475569 !important;
    font-size: 0.82rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
.streamlit-expanderContent {
    background: #0d1117 !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
}

/* ── MISC ── */
#MainMenu, footer, header { visibility: hidden; }
.stAlert { border-radius: 10px !important; font-family: 'Space Grotesk', sans-serif !important; }
hr { border-color: rgba(255,255,255,0.04) !important; }
</style>
""", unsafe_allow_html=True)

# ── CASOS PRECARGADOS ────────────────────────────────────────
CASOS = {
    "Seleccionar caso...": {},
    "C1 — Batería descargada":               {"bateria_descargada": True},
    "C2 — Falla mecánica (aceite + humo)":   {"nivel_aceite_bajo": True, "humo_azul": True},
    "C3 — Frenos desgastados":               {"pastillas_desgastadas": True},
    "C4 — Sin combustible":                  {"sin_combustible": True},
    "C5 — Motor sobrecalentado":             {"motor_sobrecalentado": True},
    "C6 — Cadena suelta + llanta baja":      {"cadena_suelta": True, "llanta_baja": True},
    "C7 — Fuga de aceite activa":            {"aceite_en_suelo": True, "nivel_aceite_bajo": True},
    "C8 — Múltiples fallas críticas":        {"pastillas_desgastadas": True, "motor_sobrecalentado": True, "llanta_baja": True},
}

APT_CFG = {
    "no_apta_para_uso":    ("dm-apt-alta",  "🔴", "NO APTA PARA CIRCULAR",  "No debe usarse hasta ser reparada."),
    "usar_con_precaucion": ("dm-apt-media", "🟡", "USAR CON PRECAUCIÓN",    "Solo trayectos cortos y baja velocidad."),
    "apta_para_uso":       ("dm-apt-baja",  "🟢", "APTA PARA CIRCULAR",     "Puede circular con normalidad."),
}
URG_CLS = {"alta": "dm-urg-alta", "media": "dm-urg-media", "baja": "dm-urg-baja"}

# ── HEADER ──────────────────────────────────────────────────
st.markdown("""
<div class="dm-header">
  <div>
    <div class="dm-pill">⬡ Sistema Basado en Conocimiento · IA II</div>
    <div class="dm-logo">Diag<span>Moto</span><sub>SBC</sub></div>
    <div class="dm-desc">
      Diagnóstico experto de fallas en motocicletas.<br>
      27 reglas · Encadenamiento hacia adelante · Trazabilidad completa.
    </div>
  </div>
  <div class="dm-stats">
    <div class="dm-stat"><div class="dm-stat-n">27</div><div class="dm-stat-l">Reglas</div></div>
    <div class="dm-stat"><div class="dm-stat-n">12</div><div class="dm-stat-l">Síntomas</div></div>
    <div class="dm-stat"><div class="dm-stat-n">11</div><div class="dm-stat-l">Tipos de falla</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── LAYOUT ──────────────────────────────────────────────────
col_l, col_r = st.columns([1, 1.5], gap="large")

with col_l:
    # Casos precargados
    st.markdown('<div class="dm-card"><div class="dm-card-title">① Casos de prueba precargados</div>', unsafe_allow_html=True)
    caso_sel = st.selectbox("caso", list(CASOS.keys()), label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    caso_hechos = CASOS.get(caso_sel, {})

    # Síntomas
    st.markdown('<div class="dm-card"><div class="dm-card-title">② Síntomas observados</div>', unsafe_allow_html=True)
    checks = {}
    for k, label in SINTOMAS_ETIQUETAS.items():
        checks[k] = st.checkbox(label, value=caso_hechos.get(k, False), key=f"{k}_{caso_sel}")
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([3, 1])
    with c1: ejecutar = st.button("⬡  Ejecutar diagnóstico", use_container_width=True)
    with c2: limpiar  = st.button("↺", use_container_width=True)

    if limpiar:
        st.rerun()

# ── RESULTADOS ───────────────────────────────────────────────
with col_r:
    hechos_activos = {k: True for k, v in checks.items() if v}

    if not ejecutar and not hechos_activos:
        st.markdown("""
        <div class="dm-empty">
          <div class="dm-empty-icon">⬡</div>
          <div class="dm-empty-text">Selecciona síntomas y ejecuta el diagnóstico</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        if not hechos_activos:
            st.warning("Selecciona al menos un síntoma.")
        else:
            hf, traza = encadenamiento_adelante(hechos_activos)

            if sin_conclusion(hf):
                st.markdown("""
                <div class="dm-card" style="border-color:rgba(234,179,8,0.2)">
                  <div class="dm-card-title">Sin conclusión</div>
                  <p style="color:#64748b;font-size:0.85rem">
                    Los síntomas seleccionados no activan ninguna regla. Intenta otra combinación.
                  </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                fallas   = hf.get("tipo_fallas", [])
                urgencia = hf.get("urgencia", "")
                accion   = hf.get("accion_recomendada", "")
                aptitud  = hf.get("aptitud", "")

                # ③ Fallas + urgencia
                badges = "".join(
                    f'<span class="dm-badge-falla">{TIPO_FALLA_ETIQUETAS.get(f,f)}</span>'
                    for f in fallas
                )
                urg_cls = URG_CLS.get(urgencia, "dm-urg-baja")
                st.markdown(f"""
                <div class="dm-card">
                  <div class="dm-card-title">③ Fallas detectadas</div>
                  <div style="margin-bottom:14px">{badges}</div>
                  <div style="display:flex;align-items:center;gap:10px">
                    <span style="color:#334155;font-size:0.78rem;text-transform:uppercase;letter-spacing:1px">Urgencia máxima</span>
                    <span class="dm-urg {urg_cls}">{urgencia.upper()}</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                # ④ Aptitud
                apt_cls, apt_icon, apt_lbl, apt_desc = APT_CFG.get(aptitud, ("dm-apt-baja","⚪","—",""))
                accion_txt = DESCRIPCIONES_ACCION.get(accion, accion)
                st.markdown(f"""
                <div class="dm-card">
                  <div class="dm-card-title">④ Diagnóstico final</div>
                  <div class="dm-apt {apt_cls}">
                    <div class="dm-apt-icon">{apt_icon}</div>
                    <div class="dm-apt-label">{apt_lbl}</div>
                    <div class="dm-apt-desc">{accion_txt}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                # ⑤ Cadena de inferencia
                pasos_html = ""
                for i, paso in enumerate(traza, 1):
                    conds = " ∧ ".join(f"{c[0]}={c[1]}" for c in paso["condiciones"])
                    ck, cv = paso["conclusion"]
                    cf = paso.get("certeza", 1.0)
                    cf_str = f'<span class="dm-step-cf"> [CF={cf:.2f}]</span>' if cf < 1.0 else ""
                    pasos_html += f"""
                    <div class="dm-step">
                      <div class="dm-step-num">{i}</div>
                      <div>
                        <span class="dm-step-regla">[{paso['regla']}]</span>
                        <span class="dm-step-cond"> SI {conds}</span>
                        <span class="dm-step-arrow"> → </span>
                        <span class="dm-step-conc">{ck} = {cv}</span>{cf_str}
                      </div>
                    </div>"""

                st.markdown(f"""
                <div class="dm-card">
                  <div class="dm-card-title">⑤ Cadena de inferencia</div>
                  {pasos_html}
                </div>
                """, unsafe_allow_html=True)

                # ¿Por qué?
                with st.expander("◈  ¿Por qué se llegó a estas conclusiones?"):
                    c1e, c2e = st.columns(2)
                    with c1e:
                        st.markdown(f'<div class="dm-porque">{porque("urgencia", urgencia, hf, traza)}</div>', unsafe_allow_html=True)
                    with c2e:
                        st.markdown(f'<div class="dm-porque">{porque("accion_recomendada", accion, hf, traza)}</div>', unsafe_allow_html=True)

                # Descarga
                reporte = explicar_razonamiento(hf, traza)
                st.download_button("⬇  Descargar reporte (.txt)", data=reporte,
                    file_name="diagnostico_moto.txt", mime="text/plain", use_container_width=True)

# ── FOOTER ───────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#1e293b;font-size:0.72rem;padding:6px 0;font-family:'Space Grotesk',sans-serif">
  DiagMoto · SBC · IA II · Manuel Bermudez &amp; Wilson Sarmiento · Los Libertadores · 2026
</div>
""", unsafe_allow_html=True)
