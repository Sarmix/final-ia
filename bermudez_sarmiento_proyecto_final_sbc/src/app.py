import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from motor_inferencia import encadenamiento_adelante, explicar_razonamiento, porque, sin_conclusion
from base_conocimiento import SINTOMAS_ETIQUETAS, TIPO_FALLA_ETIQUETAS, DESCRIPCIONES_ACCION, DESCRIPCIONES_APTITUD

st.set_page_config(page_title="DiagMoto", page_icon="🏍️", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Space Grotesk', sans-serif !important;
    background: #080b14 !important;
    color: #e2e8f0 !important;
}
.stApp::before {
    content: '';
    position: fixed; inset: 0; z-index: 0;
    background-image:
        linear-gradient(rgba(99,102,241,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,102,241,0.04) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
}
.block-container { position:relative; z-index:1; padding: 2rem 2.5rem 3rem !important; max-width:1400px !important; }

/* HEADER */
.dm-header {
    padding: 2.2rem 2.8rem;
    background: #0d1117;
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 18px;
    margin-bottom: 1.8rem;
    position: relative; overflow: hidden;
}
.dm-header::after {
    content: '';
    position: absolute; top: -80px; right: -60px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(99,102,241,0.13) 0%, transparent 65%);
    border-radius: 50%;
}
.dm-pill {
    display: inline-flex; align-items: center;
    background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.25);
    color: #818cf8; font-size: 0.68rem; font-weight: 600;
    letter-spacing: 1.5px; text-transform: uppercase;
    padding: 4px 13px; border-radius: 100px; margin-bottom: 10px;
}
.dm-logo { font-size: 2.6rem; font-weight: 700; letter-spacing: -2px; line-height: 1; margin-bottom: 6px; }
.dm-logo span { color: #6366f1; }
.dm-desc { font-size: 0.85rem; color: #475569; font-weight: 300; line-height: 1.6; }
.dm-nums { display:flex; gap:2rem; margin-top:1rem; }
.dm-num-n { font-size:1.4rem; font-weight:700; color:#6366f1; line-height:1; }
.dm-num-l { font-size:0.62rem; color:#334155; text-transform:uppercase; letter-spacing:1px; }

/* SECTION LABEL */
.sec-label {
    font-size: 0.62rem; font-weight: 700; letter-spacing: 2px;
    text-transform: uppercase; color: #334155;
    margin-bottom: 0.7rem; margin-top: 1.4rem;
    display: flex; align-items: center; gap: 8px;
}
.sec-label::after { content:''; flex:1; height:1px; background:rgba(255,255,255,0.04); }

/* SELECTBOX */
.stSelectbox label { display:none !important; }
.stSelectbox > div > div {
    background: #0f172a !important;
    border: 1px solid rgba(99,102,241,0.2) !important;
    border-radius: 10px !important;
    color: #94a3b8 !important;
    font-size: 0.87rem !important;
}

/* CHECKBOXES */
.stCheckbox { margin-bottom: 1px !important; }
.stCheckbox label {
    color: #64748b !important; font-size: 0.86rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    padding: 5px 0 !important;
    transition: color 0.15s;
}
.stCheckbox label:hover { color: #e2e8f0 !important; }

/* BOTONES */
.stButton > button {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important; font-size: 0.87rem !important;
    border-radius: 10px !important; border: none !important;
    transition: all 0.2s !important;
    height: 42px !important;
}
div[data-testid="column"]:first-child .stButton > button {
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    color: #fff !important;
    box-shadow: 0 0 24px rgba(99,102,241,0.3) !important;
}
div[data-testid="column"]:first-child .stButton > button:hover {
    box-shadow: 0 0 38px rgba(99,102,241,0.5) !important;
    transform: translateY(-1px) !important;
}
div[data-testid="column"]:last-child .stButton > button {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #475569 !important;
}

/* RESULTADOS */
.dm-empty {
    display:flex; flex-direction:column; align-items:center; justify-content:center;
    padding: 5rem 2rem; text-align:center;
    border: 1px dashed rgba(255,255,255,0.05); border-radius:16px;
    background: #0d1117;
}
.dm-empty-icon { font-size:2.5rem; opacity:0.2; margin-bottom:1rem; }
.dm-empty-text { font-size:0.72rem; color:#1e293b; text-transform:uppercase; letter-spacing:2px; font-weight:600; }

/* RESULT CARDS */
.dm-rcard {
    background: #0d1117;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 0.8rem;
}
.dm-rcard-title {
    font-size: 0.62rem; font-weight:700; letter-spacing:2px;
    text-transform:uppercase; color:#334155;
    margin-bottom: 0.9rem;
    display:flex; align-items:center; gap:8px;
}
.dm-rcard-title::after { content:''; flex:1; height:1px; background:rgba(255,255,255,0.04); }

/* BADGES */
.dm-badge {
    display:inline-flex; align-items:center;
    background:rgba(99,102,241,0.08); border:1px solid rgba(99,102,241,0.2);
    color:#818cf8; font-size:0.73rem; font-weight:600;
    padding:4px 13px; border-radius:100px; margin:3px 4px 3px 0;
}
.dm-urg {
    display:inline-flex; align-items:center;
    font-size:0.7rem; font-weight:700; letter-spacing:1.5px;
    text-transform:uppercase; padding:4px 14px; border-radius:100px;
}
.u-alta  { background:rgba(239,68,68,0.12); border:1px solid rgba(239,68,68,0.3);  color:#f87171; }
.u-media { background:rgba(234,179,8,0.12); border:1px solid rgba(234,179,8,0.3);  color:#facc15; }
.u-baja  { background:rgba(34,197,94,0.12); border:1px solid rgba(34,197,94,0.3);  color:#4ade80; }

/* APTITUD */
.dm-apt { border-radius:12px; padding:1.5rem; text-align:center; }
.dm-apt-icon { font-size:2rem; margin-bottom:0.4rem; }
.dm-apt-label { font-size:0.9rem; font-weight:700; letter-spacing:1px; text-transform:uppercase; margin-bottom:0.3rem; }
.dm-apt-desc  { font-size:0.78rem; opacity:0.6; font-weight:300; }
.a-alta  { background:rgba(239,68,68,0.07);  border:1px solid rgba(239,68,68,0.18);  }
.a-alta .dm-apt-label  { color:#f87171; }
.a-media { background:rgba(234,179,8,0.07);  border:1px solid rgba(234,179,8,0.18);  }
.a-media .dm-apt-label { color:#facc15; }
.a-baja  { background:rgba(34,197,94,0.07);  border:1px solid rgba(34,197,94,0.18);  }
.a-baja .dm-apt-label  { color:#4ade80; }

/* CADENA */
.dm-step {
    display:flex; align-items:flex-start; gap:10px;
    padding:9px 12px; border-radius:9px;
    background:#080b14; border:1px solid rgba(255,255,255,0.04);
    margin-bottom:5px;
    font-family:'JetBrains Mono',monospace; font-size:0.73rem; line-height:1.6;
}
.dm-sn {
    min-width:20px; height:20px;
    background:rgba(99,102,241,0.12); border:1px solid rgba(99,102,241,0.25);
    border-radius:5px; color:#6366f1; font-weight:600;
    display:flex; align-items:center; justify-content:center;
    font-size:0.62rem; flex-shrink:0; margin-top:2px;
}
.sc { color:#334155; }
.sr { color:#6366f1; font-weight:600; }
.sk { color:#4ade80; }
.scf{ color:#1e293b; font-size:0.66rem; }

/* PORQUE */
.dm-pq {
    background:#080b14; border:1px solid rgba(255,255,255,0.04);
    border-radius:10px; padding:1rem 1.2rem;
    font-family:'JetBrains Mono',monospace;
    font-size:0.73rem; color:#475569; line-height:1.8; white-space:pre-wrap;
}

/* DOWNLOAD */
.stDownloadButton > button {
    background: transparent !important;
    border: 1px solid rgba(99,102,241,0.2) !important;
    color: #6366f1 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size:0.82rem !important; font-weight:500 !important;
    border-radius:10px !important; width:100% !important;
}
.stDownloadButton > button:hover {
    background: rgba(99,102,241,0.07) !important;
}

/* EXPANDER */
details { background:#0d1117 !important; border:1px solid rgba(255,255,255,0.05) !important; border-radius:10px !important; }
summary { color:#334155 !important; font-size:0.8rem !important; font-family:'Space Grotesk',sans-serif !important; }

#MainMenu, footer, header { visibility:hidden; }
hr { border-color:rgba(255,255,255,0.04) !important; }
</style>
""", unsafe_allow_html=True)

# ── DATOS ────────────────────────────────────────────────────
CASOS = {
    "Seleccionar caso...": {},
    "C1 — Batería descargada":             {"bateria_descargada": True},
    "C2 — Falla mecánica (aceite + humo)": {"nivel_aceite_bajo": True, "humo_azul": True},
    "C3 — Frenos desgastados":             {"pastillas_desgastadas": True},
    "C4 — Sin combustible":                {"sin_combustible": True},
    "C5 — Motor sobrecalentado":           {"motor_sobrecalentado": True},
    "C6 — Cadena suelta + llanta baja":    {"cadena_suelta": True, "llanta_baja": True},
    "C7 — Fuga de aceite activa":          {"aceite_en_suelo": True, "nivel_aceite_bajo": True},
    "C8 — Múltiples fallas críticas":      {"pastillas_desgastadas": True, "motor_sobrecalentado": True, "llanta_baja": True},
}
APT_CFG = {
    "no_apta_para_uso":    ("a-alta",  "🔴", "NO APTA PARA CIRCULAR",  "No debe usarse hasta ser reparada."),
    "usar_con_precaucion": ("a-media", "🟡", "USAR CON PRECAUCIÓN",    "Solo trayectos cortos y baja velocidad."),
    "apta_para_uso":       ("a-baja",  "🟢", "APTA PARA CIRCULAR",     "Puede circular con normalidad."),
}
URG_CLS = {"alta": "u-alta", "media": "u-media", "baja": "u-baja"}

# ── HEADER ───────────────────────────────────────────────────
st.markdown("""
<div class="dm-header">
  <div class="dm-pill">⬡ Sistema Basado en Conocimiento · IA II</div>
  <div class="dm-logo">Diag<span>Moto</span></div>
  <div class="dm-desc">Diagnóstico experto de fallas en motocicletas · Encadenamiento hacia adelante · Trazabilidad completa</div>
  <div class="dm-nums">
    <div><div class="dm-num-n">27</div><div class="dm-num-l">Reglas</div></div>
    <div><div class="dm-num-n">12</div><div class="dm-num-l">Síntomas</div></div>
    <div><div class="dm-num-n">11</div><div class="dm-num-l">Tipos de falla</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── LAYOUT ───────────────────────────────────────────────────
col_l, col_r = st.columns([1, 1.5], gap="large")

with col_l:
    st.markdown('<div class="sec-label">① Caso de prueba precargado</div>', unsafe_allow_html=True)
    caso_sel = st.selectbox("caso", list(CASOS.keys()), label_visibility="collapsed")
    caso_hechos = CASOS.get(caso_sel, {})

    st.markdown('<div class="sec-label">② Síntomas observados</div>', unsafe_allow_html=True)
    checks = {}
    for k, label in SINTOMAS_ETIQUETAS.items():
        checks[k] = st.checkbox(label, value=caso_hechos.get(k, False), key=f"{k}_{caso_sel}")

    st.markdown("<br>", unsafe_allow_html=True)
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
          <div class="dm-empty-icon">🏍️</div>
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
                <div class="dm-rcard">
                  <div class="dm-rcard-title">Sin conclusión</div>
                  <p style="color:#475569;font-size:0.85rem">
                    Los síntomas seleccionados no activan ninguna regla. Intenta otra combinación.
                  </p>
                </div>""", unsafe_allow_html=True)
            else:
                fallas   = hf.get("tipo_fallas", [])
                urgencia = hf.get("urgencia", "")
                accion   = hf.get("accion_recomendada", "")
                aptitud  = hf.get("aptitud", "")

                # Fallas + urgencia
                badges = "".join(f'<span class="dm-badge">{TIPO_FALLA_ETIQUETAS.get(f,f)}</span>' for f in fallas)
                urg_cls = URG_CLS.get(urgencia, "u-baja")
                st.markdown(
                    f'<div class="dm-rcard"><div class="dm-rcard-title">③ Fallas detectadas</div>'
                    f'<div style="margin-bottom:12px">{badges}</div>'
                    f'<div style="display:flex;align-items:center;gap:10px">'
                    f'<span style="color:#334155;font-size:0.72rem;text-transform:uppercase;letter-spacing:1px">Urgencia máxima</span>'
                    f'<span class="dm-urg {urg_cls}">{urgencia.upper()}</span>'
                    f'</div></div>',
                    unsafe_allow_html=True
                )

                # Aptitud
                apt_cls, apt_icon, apt_lbl, apt_desc = APT_CFG.get(aptitud, ("a-baja","⚪","—",""))
                accion_txt = DESCRIPCIONES_ACCION.get(accion, accion)
                st.markdown(
                    f'<div class="dm-rcard"><div class="dm-rcard-title">④ Diagnóstico final</div>'
                    f'<div class="dm-apt {apt_cls}">'
                    f'<div class="dm-apt-icon">{apt_icon}</div>'
                    f'<div class="dm-apt-label">{apt_lbl}</div>'
                    f'<div class="dm-apt-desc">{accion_txt}</div>'
                    f'</div></div>',
                    unsafe_allow_html=True
                )

                # Cadena de inferencia
                pasos_html = ""
                for i, paso in enumerate(traza, 1):
                    conds = " ∧ ".join(f"{c[0]}={c[1]}" for c in paso["condiciones"])
                    ck, cv = paso["conclusion"]
                    cf = paso.get("certeza", 1.0)
                    cf_str = f'<span class="scf"> [CF={cf:.2f}]</span>' if cf < 1.0 else ""
                    pasos_html += (
                        f'<div class="dm-step">'
                        f'<div class="dm-sn">{i}</div>'
                        f'<div><span class="sr">[{paso["regla"]}]</span>'
                        f'<span class="sc"> SI {conds} → </span>'
                        f'<span class="sk">{ck} = {cv}</span>{cf_str}</div>'
                        f'</div>'
                    )

                st.markdown(
                    f'<div class="dm-rcard"><div class="dm-rcard-title">⑤ Cadena de inferencia</div>{pasos_html}</div>',
                    unsafe_allow_html=True
                )

                # ¿Por qué?
                with st.expander("◈  ¿Por qué se llegó a estas conclusiones?"):
                    ca, cb = st.columns(2)
                    with ca:
                        st.markdown(f'<div class="dm-pq">{porque("urgencia", urgencia, hf, traza)}</div>', unsafe_allow_html=True)
                    with cb:
                        st.markdown(f'<div class="dm-pq">{porque("accion_recomendada", accion, hf, traza)}</div>', unsafe_allow_html=True)

                st.download_button("⬇  Descargar reporte (.txt)", data=explicar_razonamiento(hf, traza),
                    file_name="diagnostico_moto.txt", mime="text/plain", use_container_width=True)

st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#1e293b;font-size:0.7rem;padding:4px 0;font-family:'Space Grotesk',sans-serif">
  DiagMoto · IA II · Manuel Bermudez &amp; Wilson Sarmiento · Los Libertadores · 2026
</div>""", unsafe_allow_html=True)
