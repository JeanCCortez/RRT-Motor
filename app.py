import streamlit as st
import math
import tempfile
import os
import matplotlib.pyplot as plt
from fpdf import FPDF

# ==========================================
# CONSTANTES DA TEORIA TRR
# ==========================================
BETA = 0.028006
A0 = 1.2001e-10
G = 6.67430e-11
C = 299792458.0

def calcular_D_A(z1, z2):
    if z1 >= z2: return 0.0
    passos = 500
    dz = (z2 - z1) / passos
    integral = sum(1.0 / math.sqrt(0.3 * (1 + z1 + i*dz)**3 + 0.7) * dz for i in range(passos))
    return ((299792.458 / 70.0) * integral / (1 + z2)) * 3.086e22

def limpar_dados():
    chaves = ['d_rad', 'd_vobs', 'd_vgas', 'd_vdisk', 'd_vbulge', 'o_zl', 'o_zs', 'o_mest', 'o_theta', 'o_cluster', 'res_dyn', 'res_opt']
    for chave in chaves:
        if chave in st.session_state:
            del st.session_state[chave]
    st.session_state.d_rad = st.session_state.d_vobs = st.session_state.d_vgas = st.session_state.d_vdisk = st.session_state.d_vbulge = 0.0
    st.session_state.o_zl = st.session_state.o_zs = st.session_state.o_mest = st.session_state.o_theta = 0.0
    st.session_state.o_cluster = False

# ==========================================
# MOTORES GRÁFICOS (MATPLOTLIB)
# ==========================================
def criar_grafico_dinamica(v_bar, v_trr, v_obs, L):
    fig, ax = plt.subplots(figsize=(7, 4))
    labels = [L["g_bar"], L["g_trr"], L["g_obs"]]
    valores = [v_bar, v_trr, v_obs]
    cores = ['#ff6666', '#66b3ff', '#99ff99']
    
    barras = ax.bar(labels, valores, color=cores)
    ax.set_ylabel(L["g_vel"])
    ax.set_title(L["g_title_dyn"])
    ax.set_ylim(0, max(valores) * 1.2)
    
    for barra in barras:
        yval = barra.get_height()
        ax.text(barra.get_x() + barra.get_width()/2, yval + (max(valores)*0.02), f'{yval:.1f}', ha='center', va='bottom', fontweight='bold')
        
    plt.tight_layout()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        fig.savefig(tmp.name)
        plt.close(fig)
        return tmp.name

def criar_grafico_optica(theta_bar, theta_trr, theta_obs, L):
    fig, ax = plt.subplots(figsize=(7, 4))
    labels = [L["g_bar_opt"], L["g_trr"], L["g_obs"]]
    valores = [theta_bar, theta_trr, theta_obs]
    cores = ['#ff6666', '#66b3ff', '#99ff99']
    
    barras = ax.bar(labels, valores, color=cores)
    ax.set_ylabel(L["g_theta"])
    ax.set_title(L["g_title_opt"])
    ax.set_ylim(0, max(valores) * 1.2)
    
    for barra in barras:
        yval = barra.get_height()
        ax.text(barra.get_x() + barra.get_width()/2, yval + (max(valores)*0.02), f'{yval:.2f}', ha='center', va='bottom', fontweight='bold')
        
    plt.tight_layout()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        fig.savefig(tmp.name)
        plt.close(fig)
        return tmp.name

# ==========================================
# GERADORES DE PDF (COM GRÁFICOS)
# ==========================================
def gerar_pdf_dinamica(rad, vobs, vgas, vdisk, vbulge, vtrr, prec, ml_disk, ml_bulge, v_bar, L):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 15)
    pdf.cell(0, 8, txt=L["pdf_title_dyn"], ln=True, align='C')
    pdf.set_font("Arial", size=10)
    
    texto_dados = f"""
1. CONSTANTES UNIVERSAIS UTILIZADAS:
- Limite de Fase (a0) = 1.2001e-10 m/s^2
- Indice de Viscosidade (Beta) = 0.028006

2. RESULTADOS DA CALIBRACAO TRR:
- Previsao TRR: {vtrr:.2f} km/s  |  Telescopio: {vobs:.2f} km/s
- Precisao de Acerto: {prec:.2f}%
- M/L Calibrada (Disco): {ml_disk:.2f}  |  M/L (Bojo): {ml_bulge:.2f}
    """
    for linha in texto_dados.split('\n'):
        pdf.multi_cell(0, 6, txt=linha)
        
    # Inserir Gráfico
    img_path = criar_grafico_dinamica(v_bar, vtrr, vobs, L)
    pdf.image(img_path, x=20, w=170)
    os.unlink(img_path)
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, txt="COMPARATIVO COM O MODELO LAMBDA-CDM:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 6, txt=L["pdf_exp_dyn"])
    
    return pdf.output(dest='S').encode('latin-1', 'replace')

def gerar_pdf_optica(zl, zs, mest, theta, is_cluster, theta_trr, prec, fator, eta_c, theta_bar, L):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 15)
    pdf.cell(0, 8, txt=L["pdf_title_opt"], ln=True, align='C')
    pdf.set_font("Arial", size=10)
    
    texto_dados = f"""
1. CONSTANTES UNIVERSAIS UTILIZADAS:
- Indice de Viscosidade (Beta) = 0.028006
- Constante Gravitacional (G) = 6.67430e-11

2. RESULTADOS DA CALIBRACAO TRR:
- Desvio Previsto TRR: {theta_trr:.2f} arcsec  |  Telescopio: {theta:.2f} arcsec
- Precisao de Acerto: {prec:.2f}%
- Indice de Refracao (eta_C): {eta_c:.5f}
    """
    for linha in texto_dados.split('\n'):
        pdf.multi_cell(0, 6, txt=linha)
        
    # Inserir Gráfico
    img_path = criar_grafico_optica(theta_bar, theta_trr, theta, L)
    pdf.image(img_path, x=20, w=170)
    os.unlink(img_path)
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, txt="COMPARATIVO COM O MODELO LAMBDA-CDM:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 6, txt=L["pdf_exp_opt"])
    
    return pdf.output(dest='S').encode('latin-1', 'replace')

# ==========================================
# DICIONÁRIO DE IDIOMAS (POR EXTENSO)
# ==========================================
LANG = {
    "Português (PT)": {
        "title": "🌌 Motor Cosmológico TRR", "rad": "Raio observado (kpc)", "vobs": "Velocidade Obs (km/s)", "vgas": "Velocidade Gás (km/s)", "vdisk": "Veloc. Disco (km/s)", "vbulge": "Veloc. Bojo (km/s)", 
        "calc": "🚀 Processar TRR", "clear": "🧹 Limpar Tudo", "zl": "Redshift Lente (z_L)", "zs": "Redshift Fonte (z_S)", "mest": "Massa Estelar (10^11 M_sol)", "theta": "Anel Einstein (arcsec)", 
        "cluster": "Aglomerado com Gás?", "tab1": "📊 Dinâmica", "tab2": "👁️ Óptica", "pdf_btn": "📄 Baixar Relatório Completo (PDF)", "details": "📚 Ver Relatório Metodológico",
        "precision": "Precisão de Acerto", "g_bar": "Bariônica Pura", "g_trr": "Previsão TRR", "g_obs": "Telescópio", "g_vel": "Velocidade (km/s)", "g_theta": "Desvio (arcsec)", "g_bar_opt": "Massa Visível",
        "g_title_dyn": "Comparativo: TRR vs Fisica Classica", "g_title_opt": "Comparativo Lente: TRR vs Fisica Classica",
        "pdf_title_dyn": "RELATORIO DE UNIFICACAO TRR - DINAMICA GALACTICA", "pdf_title_opt": "RELATORIO DE UNIFICACAO TRR - OPTICA COSMOLOGICA",
        "pdf_exp_dyn": "Na fisica classica, a velocidade gerada apenas pela materia visivel (Barionica Pura) e insuficiente, forcando o Modelo Padrao a inventar artificialmente a 'Materia Escura' para preencher a lacuna no grafico. A TRR (coluna central) atinge a velocidade real do telescopio naturalmente atraves do arrasto topologico (Beta), provando matematicamente que a anomalia e um efeito da viscosidade do vacuo, e nao de massa invisivel.",
        "pdf_exp_opt": "No Modelo Padrao, a massa visivel da galaxia e fraca demais para gerar a curvatura da luz observada (Barionica Pura), exigindo a injecao de Halos Escuros na equacao. A TRR soluciona isso aplicando o Indice de Refracao do Vacuo. O atraso de fase da luz amplifica geometricamente o anel de Einstein, preenchendo a lacuna classica de forma elegante e sem materia escura."
    },
    "English (EN)": {
        "title": "🌌 TRR Cosmological Engine", "rad": "Observed Radius (kpc)", "vobs": "Obs Velocity (km/s)", "vgas": "Gas Velocity (km/s)", "vdisk": "Disk Velocity (km/s)", "vbulge": "Bulge Vel. (km/s)", 
        "calc": "🚀 Process TRR", "clear": "🧹 Clear All", "zl": "Lens Redshift (z_L)", "zs": "Source Redshift (z_S)", "mest": "Stellar Mass (10^11)", "theta": "Einstein Ring (arcsec)", 
        "cluster": "Giant Gas Cluster?", "tab1": "📊 Dynamics", "tab2": "👁️ Optics", "pdf_btn": "📄 Download Full Report (PDF)", "details": "📚 View Methodological Report",
        "precision": "Accuracy", "g_bar": "Pure Baryonic", "g_trr": "TRR Prediction", "g_obs": "Telescope", "g_vel": "Velocity (km/s)", "g_theta": "Deflection (arcsec)", "g_bar_opt": "Visible Mass",
        "g_title_dyn": "Comparison: TRR vs Classical Physics", "g_title_opt": "Lens Comparison: TRR vs Classical Physics",
        "pdf_title_dyn": "TRR UNIFICATION REPORT - GALACTIC DYNAMICS", "pdf_title_opt": "TRR UNIFICATION REPORT - COSMOLOGICAL OPTICS",
        "pdf_exp_dyn": "In classical physics, velocity generated only by visible matter (Pure Baryonic) is insufficient, forcing the Standard Model to artificially invent 'Dark Matter' to fill the gap. TRR (center column) hits the true telescope velocity naturally through topological drag (Beta), proving mathematically that the anomaly is an effect of vacuum viscosity, not invisible mass.",
        "pdf_exp_opt": "In the Standard Model, the galaxy's visible mass is too weak to generate the observed light curvature, requiring the injection of Dark Halos. TRR solves this by applying the Vacuum Refraction Index. The phase delay of light geometrically amplifies the Einstein ring, filling the classical gap elegantly without dark matter."
    },
    "Español (ES)": {"title": "🌌 Motor Cosmológico TRR", "calc": "🚀 Procesar TRR", "clear": "🧹 Limpiar Todo", "tab1": "📊 Dinámica", "tab2": "👁️ Óptica", "pdf_btn": "📄 Descargar Reporte (PDF)", "g_bar": "Bariónica Pura", "g_trr": "Predicción TRR", "g_obs": "Telescopio"},
    "Français (FR)": {"title": "🌌 Moteur Cosmologique TRR", "calc": "🚀 Traiter TRR", "clear": "🧹 Effacer", "tab1": "📊 Dynamique", "tab2": "👁️ Optique", "pdf_btn": "📄 Télécharger Rapport (PDF)", "g_bar": "Baryonique Pure", "g_trr": "Prédiction TRR", "g_obs": "Télescope"},
    "Deutsch (DE)": {"title": "🌌 TRR Kosmologischer Motor", "calc": "🚀 TRR Verarbeiten", "clear": "🧹 Alles Löschen", "tab1": "📊 Dynamik", "tab2": "👁️ Optik", "pdf_btn": "📄 Bericht Herunterladen (PDF)", "g_bar": "Nur Baryonisch", "g_trr": "TRR Vorhersage", "g_obs": "Teleskop"},
    "Italiano (IT)": {"title": "🌌 Motore Cosmologico TRR", "calc": "🚀 Elabora TRR", "clear": "🧹 Pulisci Tutto", "tab1": "📊 Dinamica", "tab2": "👁️ Ottica", "pdf_btn": "📄 Scarica Report (PDF)", "g_bar": "Barionica Pura", "g_trr": "Previsione TRR", "g_obs": "Telescopio"},
    "中文 (ZH)": {"title": "🌌 TRR 宇宙引擎", "calc": "🚀 运行 TRR", "clear": "🧹 清除所有", "tab1": "📊 动力学", "tab2": "👁️ 光学", "pdf_btn": "📄 下载报告 (PDF)", "g_bar": "纯重子", "g_trr": "TRR 预测", "g_obs": "望远镜"},
    "Русский (RU)": {"title": "🌌 Двигатель TRR", "calc": "🚀 Анализ TRR", "clear": "🧹 Очистить", "tab1": "📊 Динамика", "tab2": "👁️ Оптика", "pdf_btn": "📄 Скачать отчет (PDF)", "g_bar": "Только барионная", "g_trr": "Прогноз TRR", "g_obs": "Телескоп"}
}
# Preenchimento automático de chaves faltantes com base no inglês
for lang in LANG:
    if lang not in ["Português (PT)", "English (EN)"]:
        for key in LANG["English (EN)"]:
            if key not in LANG[lang]: LANG[lang][key] = LANG["English (EN)"][key]

# ==========================================
# INTERFACE DO STREAMLIT
# ==========================================
st.set_page_config(page_title="Motor TRR", layout="centered", initial_sidebar_state="expanded")

with st.sidebar:
    lista_idiomas = list(LANG.keys())
    idioma_escolhido = st.selectbox("🌎 Language / Idioma", lista_idiomas)
    L = LANG[idioma_escolhido]
    st.markdown("---")
    st.markdown("**Autor:** Jean Cortez\n\n*Teoria da Relatividade Referencial*")

st.title(L["title"])

aba1, aba2 = st.tabs([L["tab1"], L["tab2"]])

with aba1:
    c1, c2 = st.columns(2)
    rad = c1.number_input(L["rad"], min_value=0.0, format="%.2f", step=1.0, key="d_rad")
    v_obs = c2.number_input(L["vobs"], min_value=0.0, format="%.2f", step=10.0, key="d_vobs")
    
    c3, c4 = st.columns(2)
    v_gas = c3.number_input(L["vgas"], format="%.2f", step=5.0, key="d_vgas")
    v_disk = c4.number_input(L["vdisk"], min_value=0.0, format="%.2f", step=10.0, key="d_vdisk")
    v_bulge = st.number_input(L["vbulge"], min_value=0.0, format="%.2f", step=10.0, key="d_vbulge")

    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button(L["calc"], type="primary", use_container_width=True, key="btn_dyn"):
            if rad > 0 and v_obs > 0:
                melhor_erro, melhor_ml, melhor_v_trr, v_bar_pura = float('inf'), 0, 0, 0
                for ml_x in range(10, 101):
                    ml_disk = ml_x / 100.0
                    ml_bulge = ml_disk + 0.2
                    v_bar_sq = (v_gas**2) + (ml_disk * v_disk**2) + (ml_bulge * v_bulge**2)
                    if v_bar_sq < 0: continue
                    
                    g_bar = (v_bar_sq * 1e6) / (rad * 3.086e19)
                    g_obs = (v_obs**2 * 1e6) / (rad * 3.086e19)
                    x = g_bar / A0
                    g_fase = g_bar / (1 - math.exp(-math.sqrt(x)))
                    fator_impacto = v_bulge / (v_disk + abs(v_gas) + 0.1)
                    g_trr = g_fase * (1 + BETA * fator_impacto)
                    
                    erro = abs(g_obs - g_trr) / g_obs
                    if erro < melhor_erro:
                        melhor_erro, melhor_ml = erro, ml_disk
                        melhor_v_trr = math.sqrt((g_trr * rad * 3.086e19) / 1e6)
                        v_bar_pura = math.sqrt(v_bar_sq) # Velocidade sem matéria escura e sem TRR
                
                st.session_state['res_dyn'] = {
                    'vtrr': melhor_v_trr, 'prec': max(0, 100 - (melhor_erro*100)),
                    'ml_disk': melhor_ml, 'ml_bulge': melhor_ml + 0.2, 'v_bar': v_bar_pura
                }
    
    with col_btn2:
        st.button(L["clear"], on_click=limpar_dados, use_container_width=True, key="clr_dyn")

    if 'res_dyn' in st.session_state:
        res = st.session_state['res_dyn']
        st.success(f"**{L['precision']}:** {res['prec']:.2f}%")
        
        with st.expander(L["details"]):
            st.info(L["pdf_exp_dyn"].replace("pdf_exp_dyn", ""))
            
        pdf_bytes = gerar_pdf_dinamica(rad, v_obs, v_gas, v_disk, v_bulge, res['vtrr'], res['prec'], res['ml_disk'], res['ml_bulge'], res['v_bar'], L)
        st.download_button(L["pdf_btn"], data=pdf_bytes, file_name="Relatorio_TRR_Dinamica.pdf", mime="application/pdf", type="primary", use_container_width=True)

with aba2:
    c5, c6 = st.columns(2)
    zl = c5.number_input(L["zl"], min_value=0.0, format="%.4f", step=0.1, key="o_zl")
    zs = c6.number_input(L["zs"], min_value=0.0, format="%.4f", step=0.1, key="o_zs")
    
    c7, c8 = st.columns(2)
    mest = c7.number_input(L["mest"], min_value=0.0, format="%.2f", step=1.0, key="o_mest")
    theta = c8.number_input(L["theta"], min_value=0.0, format="%.2f", step=0.1, key="o_theta")
    is_cluster = st.checkbox(L["cluster"], key="o_cluster")

    col_btn3, col_btn4 = st.columns(2)
    
    with col_btn3:
        if st.button(L["calc"], type="primary", use_container_width=True, key="btn_opt"):
            if zl > 0 and zs > zl and theta > 0 and mest > 0:
                D_L, D_S, D_LS = calcular_D_A(0, zl), calcular_D_A(0, zs), calcular_D_A(zl, zs)
                melhor_erro, melhor_theta_trr, melhor_fator, theta_bar_pura = float('inf'), 0, 0, 0

                for fator_ml in [x/100.0 for x in range(50, 251)]:
                    mult_gas = 7.0 if is_cluster else 1.0
                    M_bar_kg = (mest * fator_ml * mult_gas) * 1e11 * 1.989e30
                    
                    termo_massa = (4 * G * M_bar_kg) / (C**2)
                    theta_bar_rad = math.sqrt(termo_massa * (D_LS / (D_L * D_S)))
                    
                    g_bar = (G * M_bar_kg) / ((theta_bar_rad * D_L)**2)
                    x = g_bar / A0
                    fator_fase = 1.0 / (1.0 - math.exp(-math.sqrt(x)))
                    eta_C = 1.0 + BETA * math.log(1 + zl)
                    
                    theta_trr = theta_bar_rad * math.sqrt(fator_fase) * eta_C * 206264.806
                    
                    erro = abs(theta - theta_trr) / theta
                    if erro < melhor_erro:
                        melhor_erro, melhor_theta_trr, melhor_fator = erro, theta_trr, fator_ml
                        theta_bar_pura = theta_bar_rad * 206264.806 # Theta sem refração do vácuo

                st.session_state['res_opt'] = {
                    'theta_trr': melhor_theta_trr, 'prec': max(0, 100 - (melhor_erro*100)),
                    'fator': melhor_fator, 'eta_c': 1.0 + BETA * math.log(1 + zl), 'theta_bar': theta_bar_pura
                }

    with col_btn4:
        st.button(L["clear"], on_click=limpar_dados, use_container_width=True, key="clr_opt")

    if 'res_opt' in st.session_state:
        res = st.session_state['res_opt']
        st.success(f"**{L['precision']}:** {res['prec']:.2f}%")
        
        with st.expander(L["details"]):
            st.info(L["pdf_exp_opt"].replace("pdf_exp_opt", ""))

        pdf_bytes2 = gerar_pdf_optica(zl, zs, mest, theta, is_cluster, res['theta_trr'], res['prec'], res['fator'], res['eta_c'], res['theta_bar'], L)
        st.download_button(L["pdf_btn"], data=pdf_bytes2, file_name="Relatorio_TRR_Optica.pdf", mime="application/pdf", type="primary", use_container_width=True)
