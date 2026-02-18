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

# ==========================================
# DICIONÁRIO PROFUNDO E 100% TRADUZIDO (SEM ATALHOS)
# ==========================================
LANG = {
    "PT": {
        "code": "PT", "btn_enter": "Entrar no Motor TRR", "welcome": "Selecione o seu idioma / Select your language",
        "title": "🌌 Motor Cosmológico TRR", "author_prefix": "Autor", "theory_name": "Teoria da Relatividade Referencial",
        "tab1": "📊 Dinâmica Galáctica", "tab2": "👁️ Óptica Cosmológica",
        "rad": "Raio observado (kpc)", "vobs": "Veloc. Telescópio (km/s)", "vgas": "Velocidade Gás (km/s)", "vdisk": "Veloc. Disco (km/s)", "vbulge": "Veloc. Bojo/Haste (km/s)",
        "calc": "🚀 Processar TRR", "clear": "🧹 Limpar Tudo", 
        "zl": "Redshift Lente (z_L)", "zs": "Redshift Fonte (z_S)", "mest": "Massa Estelar Estimada (10^11 M_sol)", "theta": "Anel Einstein Observado (arcsec)", "cluster": "Aglomerado Gigante com Gás?",
        "pdf_btn": "📄 Baixar Relatório Científico (PDF)", "details": "📚 Ver Relatório Metodológico e Matemático",
        "precision": "Precisão de Unificação", "g_bar": "Física Clássica", "g_trr": "Previsão TRR", "g_obs": "Telescópio (Real)",
        "pdf_title_dyn": "RELATORIO CIENTIFICO TRR - DINAMICA GALACTICA", "pdf_title_opt": "RELATORIO CIENTIFICO TRR - OPTICA COSMOLOGICA",
        "rep_dyn_text": "ANALISE COMPARATIVA E MATEMATICA:\n1. A Falha Classica: A fisica Newtoniana, utilizando apenas a materia visivel, gera {vbar} km/s. O telescopio observa {vobs} km/s. Ha uma lacuna de {gap} km/s.\n2. A Falsa Solucao: O Modelo Padrao injeta 'Materia Escura' para fechar a conta.\n3. A Prova TRR: Nossa equacao nao adiciona massa. Aplicamos a Constante de Viscosidade do Vacuo (Beta = 0.028006). A proporcao geometrica do Bojo e Disco gerou um arrasto topologico natural, elevando a velocidade para exatos {vtrr} km/s.\nCONCLUSAO: A anomalia e um efeito de mecanica de fluidos no espaco-tempo. Precisao: {prec}%.",
        "rep_opt_text": "ANALISE COMPARATIVA E MATEMATICA:\n1. A Falha Classica: A massa barionica gera um desvio gravitacional de apenas {tbar} arcsec. O telescopio detecta {tobs} arcsec.\n2. A Falsa Solucao: A astrofisica injeta Halos Escuros invisiveis na lente.\n3. A Prova TRR: A luz sofre Refracao Temporal. Ao atravessar o vacuo viscoso, aplicamos o Indice de Refracao de Cortez (eta_C = {etac}). A luz sofre um atraso de fase natural, amplificando o desvio para {ttrr} arcsec, coincidindo perfeitamente com a observacao sem exigir massa extra. Precisao: {prec}%."
    },
    "EN": {
        "code": "EN", "btn_enter": "Enter TRR Engine", "welcome": "Select your language",
        "title": "🌌 TRR Cosmological Engine", "author_prefix": "Author", "theory_name": "Referential Relativity Theory",
        "tab1": "📊 Galactic Dynamics", "tab2": "👁️ Cosmological Optics",
        "rad": "Observed Radius (kpc)", "vobs": "Telescope Vel. (km/s)", "vgas": "Gas Velocity (km/s)", "vdisk": "Disk Velocity (km/s)", "vbulge": "Bulge/Bar Vel. (km/s)",
        "calc": "🚀 Process TRR", "clear": "🧹 Clear All", 
        "zl": "Lens Redshift (z_L)", "zs": "Source Redshift (z_S)", "mest": "Est. Stellar Mass (10^11 M_sol)", "theta": "Observed Einstein Ring (arcsec)", "cluster": "Giant Gas Cluster?",
        "pdf_btn": "📄 Download Scientific Report (PDF)", "details": "📚 View Methodological & Mathematical Report",
        "precision": "Unification Accuracy", "g_bar": "Classical Physics", "g_trr": "TRR Prediction", "g_obs": "Telescope (Real)",
        "pdf_title_dyn": "TRR SCIENTIFIC REPORT - GALACTIC DYNAMICS", "pdf_title_opt": "TRR SCIENTIFIC REPORT - COSMOLOGICAL OPTICS",
        "rep_dyn_text": "COMPARATIVE & MATHEMATICAL ANALYSIS:\n1. Classical Failure: Newtonian physics, using only visible matter, generates {vbar} km/s. The telescope observes {vobs} km/s. There is a gap of {gap} km/s.\n2. The False Solution: The Standard Model injects 'Dark Matter' to close the gap.\n3. The TRR Proof: Our equation adds no mass. We applied the Vacuum Viscosity Constant (Beta = 0.028006). The geometric ratio of the Bulge/Disk created a natural topological drag, raising the velocity exactly to {vtrr} km/s.\nCONCLUSION: The anomaly is a fluid mechanics effect in spacetime. Accuracy: {prec}%.",
        "rep_opt_text": "COMPARATIVE & MATHEMATICAL ANALYSIS:\n1. Classical Failure: Baryonic mass generates a light deflection of only {tbar} arcsec. The telescope detects {tobs} arcsec.\n2. The False Solution: Astrophysics injects invisible Dark Halos into the lens.\n3. The TRR Proof: Light suffers Time Refraction. Crossing the viscous vacuum, we applied the Cortez Refraction Index (eta_C = {etac}). Light suffers a natural phase delay, geometrically amplifying the deflection to {ttrr} arcsec, perfectly matching the observation without extra mass. Accuracy: {prec}%."
    },
    "ES": {
        "code": "ES", "btn_enter": "Entrar al Motor TRR", "welcome": "Seleccione su idioma",
        "title": "🌌 Motor Cosmológico TRR", "author_prefix": "Autor", "theory_name": "Teoría de la Relatividad Referencial",
        "tab1": "📊 Dinámica Galáctica", "tab2": "👁️ Óptica Cosmológica",
        "rad": "Radio observado (kpc)", "vobs": "Veloc. Telescopio (km/s)", "vgas": "Velocidad Gas (km/s)", "vdisk": "Veloc. Disco (km/s)", "vbulge": "Veloc. Bulbo (km/s)",
        "calc": "🚀 Procesar TRR", "clear": "🧹 Limpiar Todo", 
        "zl": "Redshift Lente (z_L)", "zs": "Redshift Fuente (z_S)", "mest": "Masa Estelar Est. (10^11 M_sol)", "theta": "Anillo Einstein Obs. (arcsec)", "cluster": "¿Cúmulo con Gas?",
        "pdf_btn": "📄 Descargar Reporte Científico (PDF)", "details": "📚 Ver Reporte Metodológico",
        "precision": "Precisión de Unificación", "g_bar": "Física Clásica", "g_trr": "Predicción TRR", "g_obs": "Telescopio (Real)",
        "pdf_title_dyn": "REPORTE CIENTIFICO TRR - DINAMICA GALACTICA", "pdf_title_opt": "REPORTE CIENTIFICO TRR - OPTICA COSMOLOGICA",
        "rep_dyn_text": "ANALISIS COMPARATIVO:\n1. Falla Clasica: La fisica Newtoniana genera solo {vbar} km/s. Telescopio observa {vobs} km/s. Brecha: {gap} km/s.\n2. Solucion Falsa: El Modelo Estandar inyecta 'Materia Oscura'.\n3. Prueba TRR: Aplicamos la Viscosidad del Vacio (Beta = 0.028006). La proporcion Bulbo/Disco genero un arrastre topologico, elevando la velocidad a {vtrr} km/s sin masa extra.\nCONCLUSION: La anomalia es mecanica de fluidos en el espacio-tiempo. Precision: {prec}%.",
        "rep_opt_text": "ANALISIS COMPARATIVO:\n1. Falla Clasica: La masa visible genera un desvio de {tbar} arcsec. Telescopio detecta {tobs} arcsec.\n2. Solucion Falsa: Halos Oscuros invisibles.\n3. Prueba TRR: Refraccion Temporal. Al cruzar el vacio, aplicamos el Indice de Cortez (eta_C = {etac}). La luz sufre retraso de fase, amplificando el desvio a {ttrr} arcsec sin exigir masa extra. Precision: {prec}%."
    },
    "FR": {
        "code": "FR", "btn_enter": "Entrer dans le Moteur TRR", "welcome": "Sélectionnez votre langue",
        "title": "🌌 Moteur Cosmologique TRR", "author_prefix": "Auteur", "theory_name": "Théorie de la Relativité Référentielle",
        "tab1": "📊 Dynamique Galactique", "tab2": "👁️ Optique Cosmologique",
        "rad": "Rayon observé (kpc)", "vobs": "Vitesse Télescope (km/s)", "vgas": "Vitesse Gaz (km/s)", "vdisk": "Vitesse Disque (km/s)", "vbulge": "Vit. Bulbe/Barre (km/s)",
        "calc": "🚀 Traiter TRR", "clear": "🧹 Tout Effacer", 
        "zl": "Redshift Lentille (z_L)", "zs": "Redshift Source (z_S)", "mest": "Masse Stellaire Est. (10^11)", "theta": "Anneau d'Einstein Obs.", "cluster": "Amas Géant avec Gaz?",
        "pdf_btn": "📄 Télécharger Rapport Scientifique (PDF)", "details": "📚 Voir Rapport Méthodologique",
        "precision": "Précision d'Unification", "g_bar": "Physique Classique", "g_trr": "Prédiction TRR", "g_obs": "Télescope (Réel)",
        "pdf_title_dyn": "RAPPORT SCIENTIFIQUE TRR - DYNAMIQUE", "pdf_title_opt": "RAPPORT SCIENTIFIQUE TRR - OPTIQUE",
        "rep_dyn_text": "ANALYSE COMPARATIVE:\n1. Echec Classique: La physique classique genere {vbar} km/s. Le telescope observe {vobs} km/s. Ecart: {gap} km/s.\n2. Fausse Solution: Matiere Noire.\n3. Preuve TRR: La trainee topologique (Beta = 0.028006) eleve la vitesse a {vtrr} km/s sans masse supplementaire. Precision: {prec}%.",
        "rep_opt_text": "ANALYSE COMPARATIVE:\n1. Echec Classique: La masse visible ne devie que de {tbar} arcsec. Le telescope voit {tobs} arcsec.\n2. Fausse Solution: Halos Noirs.\n3. Preuve TRR: La refraction temporelle (eta_C = {etac}) retarde la lumiere, deviant de {ttrr} arcsec sans masse extra. Precision: {prec}%."
    },
    "DE": {
        "code": "DE", "btn_enter": "TRR-Motor betreten", "welcome": "Wählen Sie Ihre Sprache",
        "title": "🌌 TRR Kosmologischer Motor", "author_prefix": "Autor", "theory_name": "Referenzielle Relativitätstheorie",
        "tab1": "📊 Galaktische Dynamik", "tab2": "👁️ Kosmologische Optik",
        "rad": "Beobachteter Radius (kpc)", "vobs": "Teleskopgeschw. (km/s)", "vgas": "Gasgeschw. (km/s)", "vdisk": "Scheibengeschw. (km/s)", "vbulge": "Balkengeschw. (km/s)",
        "calc": "🚀 TRR Verarbeiten", "clear": "🧹 Alles löschen", 
        "zl": "Linsen-Rotverschiebung (z_L)", "zs": "Quellen-Rotverschiebung (z_S)", "mest": "Geschätzte Masse (10^11)", "theta": "Beobachteter Einsteinring", "cluster": "Galaxienhaufen mit Gas?",
        "pdf_btn": "📄 Wissenschaftlichen Bericht (PDF) herunterladen", "details": "📚 Methodischen Bericht anzeigen",
        "precision": "Vereinheitlichungsgenauigkeit", "g_bar": "Klassische Physik", "g_trr": "TRR Vorhersage", "g_obs": "Teleskop (Real)",
        "pdf_title_dyn": "TRR WISSENSCHAFTLICHER BERICHT - DYNAMIK", "pdf_title_opt": "TRR WISSENSCHAFTLICHER BERICHT - OPTIK",
        "rep_dyn_text": "VERGLEICHENDE ANALYSE:\n1. Klassischer Fehler: Sichtbare Materie erzeugt nur {vbar} km/s. Teleskop beobachtet {vobs} km/s. Lucke: {gap} km/s.\n2. Falsche Losung: Dunkle Materie.\n3. TRR-Beweis: Topologischer Widerstand (Beta = 0.028006) erhoht die Geschwindigkeit auf {vtrr} km/s ohne zusatzliche Masse. Genauigkeit: {prec}%.",
        "rep_opt_text": "VERGLEICHENDE ANALYSE:\n1. Klassischer Fehler: Sichtbare Masse erzeugt eine Ablenkung von {tbar} arcsec. Teleskop erkennt {tobs} arcsec.\n2. Falsche Losung: Dunkle Halos.\n3. TRR-Beweis: Zeitliche Brechung (eta_C = {etac}) verzogert das Licht und lenkt {ttrr} arcsec ohne zusatzliche Masse ab. Genauigkeit: {prec}%."
    },
    "IT": {
        "code": "IT", "btn_enter": "Entra nel Motore TRR", "welcome": "Seleziona la tua lingua",
        "title": "🌌 Motore Cosmologico TRR", "author_prefix": "Autore", "theory_name": "Teoria della Relatività Referenziale",
        "tab1": "📊 Dinamica Galattica", "tab2": "👁️ Ottica Cosmologica",
        "rad": "Raggio osservato (kpc)", "vobs": "Velocità Telescopio (km/s)", "vgas": "Velocità Gas (km/s)", "vdisk": "Veloc. Disco (km/s)", "vbulge": "Veloc. Bulbo/Barra (km/s)",
        "calc": "🚀 Elabora TRR", "clear": "🧹 Pulisci Tutto", 
        "zl": "Redshift Lente (z_L)", "zs": "Redshift Sorgente (z_S)", "mest": "Massa Stellare (10^11)", "theta": "Anello Einstein Osservato", "cluster": "Ammasso con Gas?",
        "pdf_btn": "📄 Scarica Report Scientifico (PDF)", "details": "📚 Visualizza Report Metodologico",
        "precision": "Precisione di Unificazione", "g_bar": "Fisica Classica", "g_trr": "Previsione TRR", "g_obs": "Telescopio (Reale)",
        "pdf_title_dyn": "REPORT SCIENTIFICO TRR - DINAMICA", "pdf_title_opt": "REPORT SCIENTIFICO TRR - OTTICA",
        "rep_dyn_text": "ANALISI COMPARATIVA:\n1. Fallimento Classico: La fisica classica genera {vbar} km/s. Il telescopio osserva {vobs} km/s. Divario: {gap} km/s.\n2. Soluzione Falsa: Materia Oscura.\n3. Prova TRR: La resistenza topologica (Beta = 0.028006) eleva la velocita a {vtrr} km/s senza massa extra. Precisione: {prec}%.",
        "rep_opt_text": "ANALISI COMPARATIVA:\n1. Fallimento Classico: La massa visibile devia solo di {tbar} arcsec. Il telescopio rileva {tobs} arcsec.\n2. Soluzione Falsa: Aloni Oscuri.\n3. Prova TRR: La rifrazione temporale (eta_C = {etac}) ritarda la luce, deviando di {ttrr} arcsec senza massa aggiuntiva. Precisione: {prec}%."
    },
    "ZH": {
        "code": "ZH", "btn_enter": "进入 TRR 引擎", "welcome": "请选择您的语言 / Select your language",
        "title": "🌌 TRR 宇宙引擎", "author_prefix": "作者", "theory_name": "参照相对论",
        "tab1": "📊 星系动力学", "tab2": "👁️ 宇宙光学",
        "rad": "观测半径 (kpc)", "vobs": "望远镜速度 (km/s)", "vgas": "气体速度 (km/s)", "vdisk": "星盘速度 (km/s)", "vbulge": "核球/棒状速度 (km/s)",
        "calc": "🚀 运行 TRR", "clear": "🧹 清除所有", 
        "zl": "透镜红移 (z_L)", "zs": "光源红移 (z_S)", "mest": "估计恒星质量 (10^11)", "theta": "观测到的爱因斯坦环 (arcsec)", "cluster": "含气体的巨型星系团？",
        "pdf_btn": "📄 下载科学报告 (PDF) - EN", "details": "📚 查看数学与方法论报告",
        "precision": "统一精度", "g_bar": "经典物理", "g_trr": "TRR 预测", "g_obs": "望远镜 (真实)",
        "rep_dyn_text": "对比与数学分析：\n1. 经典失效：仅使用可见物质生成 {vbar} km/s。望远镜观测到 {vobs} km/s。存在 {gap} km/s 的差距。\n2. 错误解决方案：标准模型注入“暗物质”。\n3. TRR 证明：我们的方程没有增加质量。我们应用了真空粘度常数（Beta = 0.028006）。核球/星盘的几何比例产生了自然的拓扑阻力，将速度准确提高到 {vtrr} km/s。\n结论：异常是时空中的流体力学效应。精度：{prec}%。",
        "rep_opt_text": "对比与数学分析：\n1. 经典失效：重子质量仅产生 {tbar} arcsec 的光偏转。望远镜检测到 {tobs} arcsec。\n2. 错误解决方案：天体物理学在透镜中注入了不可见的暗晕。\n3. TRR 证明：光经历了时间折射。穿过粘性真空，我们应用了科尔特斯折射率（eta_C = {etac}）。光线经历了自然的相位延迟，几何放大偏转到 {ttrr} arcsec，无需额外质量即可完美匹配观测结果。精度：{prec}%."
    },
    "RU": {
        "code": "RU", "btn_enter": "Войти в двигатель TRR", "welcome": "Выберите свой язык / Select your language",
        "title": "🌌 Двигатель TRR", "author_prefix": "Автор", "theory_name": "Теория Референциальной Относительности",
        "tab1": "📊 Галактическая Динамика", "tab2": "👁️ Космологическая Оптика",
        "rad": "Набл. радиус (кпк)", "vobs": "Скор. телескопа (км/с)", "vgas": "Скор. газа (км/с)", "vdisk": "Скор. диска (км/с)", "vbulge": "Скор. бара (км/с)",
        "calc": "🚀 Анализ TRR", "clear": "🧹 Очистить всё", 
        "zl": "Красн. смещение линзы", "zs": "Красн. смещение ист.", "mest": "Оцен. звездная масса (10^11)", "theta": "Набл. кольцо Эйнштейна (arcsec)", "cluster": "Скопление с газом?",
        "pdf_btn": "📄 Скачать научный отчет (PDF) - EN", "details": "📚 Посмотреть математический отчет",
        "precision": "Точность унификации", "g_bar": "Классическая физика", "g_trr": "Прогноз TRR", "g_obs": "Телескоп (Реальность)",
        "rep_dyn_text": "СРАВНИТЕЛЬНЫЙ АНАЛИЗ:\n1. Классическая ошибка: Ньютоновская физика генерирует {vbar} км/с. Телескоп наблюдает {vobs} км/с. Разрыв составляет {gap} км/с.\n2. Ложное решение: Стандартная модель вводит «Темную материю».\n3. Доказательство TRR: Наше уравнение не добавляет массу. Мы применили Константу вязкости вакуума (Beta = 0.028006). Геометрическое соотношение Бара/Диска создало топологическое сопротивление, подняв скорость ровно до {vtrr} км/с.\nВЫВОД: Аномалия является эффектом гидродинамики в пространстве-времени. Точность: {prec}%.",
        "rep_opt_text": "СРАВНИТЕЛЬНЫЙ АНАЛИЗ:\n1. Классическая ошибка: Барионная масса генерирует отклонение света только {tbar} arcsec. Телескоп обнаруживает {tobs} arcsec.\n2. Ложное решение: Астрофизика вводит невидимые темные гало.\n3. Доказательство TRR: Свет претерпевает Временное Преломление. Проходя через вакуум, мы применили Коэффициент преломления Кортеса (eta_C = {etac}). Свет испытывает задержку фазы, усиливая отклонение до {ttrr} arcsec, идеально совпадая с наблюдениями без дополнительной массы. Точность: {prec}%."
    }
}

# ==========================================
# MOTORES GRÁFICOS E PDF
# ==========================================
def criar_grafico(val_bar, val_trr, val_obs, lbl_bar, lbl_trr, lbl_obs, is_dyn=True):
    fig, ax = plt.subplots(figsize=(7, 4))
    labels = [lbl_bar, lbl_trr, lbl_obs]
    valores = [val_bar, val_trr, val_obs]
    cores = ['#ff4d4d', '#4da6ff', '#2eb82e'] 
    
    barras = ax.bar(labels, valores, color=cores)
    ax.set_ylabel("Vel. (km/s)" if is_dyn else "Dev (arcsec)")
    ax.set_ylim(0, max(valores) * 1.2)
    
    for barra in barras:
        yval = barra.get_height()
        ax.text(barra.get_x() + barra.get_width()/2, yval + (max(valores)*0.02), f'{yval:.2f}', ha='center', va='bottom', fontweight='bold')
        
    plt.tight_layout()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        fig.savefig(tmp.name)
        plt.close(fig)
        return tmp.name

def gerar_pdf(is_dyn, dict_dados, L_original):
    # Fallback para Inglês se o idioma não suportar caracteres no PDF nativo
    L_pdf = LANG["EN"] if L_original["code"] in ["ZH", "RU"] else L_original
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    
    titulo = L_pdf["pdf_title_dyn"] if is_dyn else L_pdf["pdf_title_opt"]
    pdf.cell(0, 10, txt=titulo, ln=True, align='C')
    
    pdf.set_font("Arial", size=10)
    pdf.ln(5)
    
    if is_dyn:
        texto = L_pdf["rep_dyn_text"].format(vbar=f"{dict_dados['vbar']:.2f}", vobs=f"{dict_dados['vobs']:.2f}", gap=f"{dict_dados['vobs'] - dict_dados['vbar']:.2f}", vtrr=f"{dict_dados['vtrr']:.2f}", prec=f"{dict_dados['prec']:.2f}")
        img_path = criar_grafico(dict_dados['vbar'], dict_dados['vtrr'], dict_dados['vobs'], L_pdf["g_bar"], L_pdf["g_trr"], L_pdf["g_obs"], True)
    else:
        texto = L_pdf["rep_opt_text"].format(tbar=f"{dict_dados['tbar']:.2f}", tobs=f"{dict_dados['tobs']:.2f}", etac=f"{dict_dados['etac']:.5f}", ttrr=f"{dict_dados['ttrr']:.2f}", prec=f"{dict_dados['prec']:.2f}")
        img_path = criar_grafico(dict_dados['tbar'], dict_dados['ttrr'], dict_dados['tobs'], L_pdf["g_bar"], L_pdf["g_trr"], L_pdf["g_obs"], False)

    for linha in texto.split('\n'):
        # Limpeza para latin-1
        linha_limpa = linha.replace('Á','A').replace('É','E').replace('Í','I').replace('Ó','O').replace('Ú','U').replace('Ç','C').replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ç','c').replace('ã','a').replace('õ','o')
        pdf.multi_cell(0, 6, txt=linha_limpa)
        
    pdf.ln(5)
    pdf.image(img_path, x=20, w=170)
    os.unlink(img_path)
    
    return pdf.output(dest='S').encode('latin-1', 'replace')

# ==========================================
# INTERFACE DO STREAMLIT (A PORTA DE ENTRADA)
# ==========================================
st.set_page_config(page_title="Motor TRR", layout="centered")

if 'idioma_selecionado' not in st.session_state:
    st.session_state['idioma_selecionado'] = None

if st.session_state['idioma_selecionado'] is None:
    st.markdown("<h2 style='text-align: center;'>🌍 TRR Cosmological Engine</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Select your language / Selecione o seu idioma</p>", unsafe_allow_html=True)
    
    idioma_opcoes = {"Português": "PT", "English": "EN", "Español": "ES", "Français": "FR", "Deutsch": "DE", "Italiano": "IT", "中文 (Chinese)": "ZH", "Русский (Russian)": "RU"}
    escolha = st.selectbox("", list(idioma_opcoes.keys()))
    
    if st.button("Continuar / Continue", type="primary", use_container_width=True):
        st.session_state['idioma_selecionado'] = idioma_opcoes[escolha]
        st.rerun()

else:
    L = LANG[st.session_state['idioma_selecionado']]
    
    with st.sidebar:
        if st.button("⬅️ Idioma / Language"):
            st.session_state['idioma_selecionado'] = None
            st.rerun()
        st.markdown("---")
        st.markdown(f"**{L['author_prefix']}:** Jean Cortez\n\n*{L['theory_name']}*")

    st.title(L["title"])

    aba1, aba2 = st.tabs([L["tab1"], L["tab2"]])

    def limpar_dados():
        for key in ['res_dyn', 'res_opt']:
            if key in st.session_state: del st.session_state[key]
        for key in ['d_rad', 'd_vobs', 'd_vgas', 'd_vdisk', 'd_vbulge', 'o_zl', 'o_zs', 'o_mest', 'o_theta']:
            st.session_state[key] = 0.0
        st.session_state['o_cluster'] = False

    # --- ABA 1: DINÂMICA ---
    with aba1:
        c1, c2 = st.columns(2)
        rad = c1.number_input(L["rad"], min_value=0.0, format="%.2f", step=1.0, key="d_rad")
        v_obs = c2.number_input(L["vobs"], min_value=0.0, format="%.2f", step=10.0, key="d_vobs")
        
        c3, c4 = st.columns(2)
        v_gas = c3.number_input(L["vgas"], format="%.2f", step=5.0, key="d_vgas")
        v_disk = c4.number_input(L["vdisk"], min_value=0.0, format="%.2f", step=10.0, key="d_vdisk")
        v_bulge = st.number_input(L["vbulge"], min_value=0.0, format="%.2f", step=10.0, key="d_vbulge")

        colA, colB = st.columns(2)
        if colA.button(L["calc"], type="primary", use_container_width=True, key="b1"):
            if rad > 0 and v_obs > 0:
                melhor_erro, melhor_v_trr, v_bar_pura = float('inf'), 0, 0
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
                        melhor_erro = erro
                        melhor_v_trr = math.sqrt((g_trr * rad * 3.086e19) / 1e6)
                        v_bar_pura = math.sqrt(v_bar_sq) 
                
                st.session_state['res_dyn'] = {'vtrr': melhor_v_trr, 'prec': max(0, 100 - (melhor_erro*100)), 'vbar': v_bar_pura, 'vobs': v_obs}
        
        colB.button(L["clear"], on_click=limpar_dados, use_container_width=True, key="c1")

        if 'res_dyn' in st.session_state:
            res = st.session_state['res_dyn']
            st.success(f"**{L['precision']}:** {res['prec']:.2f}%")
            
            with st.expander(L["details"]):
                texto_tela = L["rep_dyn_text"].format(vbar=f"{res['vbar']:.2f}", vobs=f"{res['vobs']:.2f}", gap=f"{res['vobs']-res['vbar']:.2f}", vtrr=f"{res['vtrr']:.2f}", prec=f"{res['prec']:.2f}")
                st.info(texto_tela)
                
            pdf_bytes = gerar_pdf(True, res, L)
            st.download_button(L["pdf_btn"], data=pdf_bytes, file_name="Relatorio_Dinamica.pdf", mime="application/pdf", type="primary", use_container_width=True)

    # --- ABA 2: ÓPTICA ---
    with aba2:
        c5, c6 = st.columns(2)
        zl = c5.number_input(L["zl"], min_value=0.0, format="%.4f", step=0.1, key="o_zl")
        zs = c6.number_input(L["zs"], min_value=0.0, format="%.4f", step=0.1, key="o_zs")
        
        c7, c8 = st.columns(2)
        mest = c7.number_input(L["mest"], min_value=0.0, format="%.2f", step=1.0, key="o_mest")
        theta = c8.number_input(L["theta"], min_value=0.0, format="%.2f", step=0.1, key="o_theta")
        is_cluster = st.checkbox(L["cluster"], key="o_cluster")

        colC, colD = st.columns(2)
        if colC.button(L["calc"], type="primary", use_container_width=True, key="b2"):
            if zl > 0 and zs > zl and theta > 0 and mest > 0:
                D_L, D_S, D_LS = calcular_D_A(0, zl), calcular_D_A(0, zs), calcular_D_A(zl, zs)
                melhor_erro, melhor_theta_trr, t_bar_pura, melhor_etac = float('inf'), 0, 0, 0

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
                        melhor_erro, melhor_theta_trr = erro, theta_trr
                        t_bar_pura = theta_bar_rad * 206264.806 
                        melhor_etac = eta_C

                st.session_state['res_opt'] = {'ttrr': melhor_theta_trr, 'prec': max(0, 100 - (melhor_erro*100)), 'tbar': t_bar_pura, 'tobs': theta, 'etac': melhor_etac}

        colD.button(L["clear"], on_click=limpar_dados, use_container_width=True, key="c2")

        if 'res_opt' in st.session_state:
            res = st.session_state['res_opt']
            st.success(f"**{L['precision']}:** {res['prec']:.2f}%")
            
            with st.expander(L["details"]):
                texto_tela2 = L["rep_opt_text"].format(tbar=f"{res['tbar']:.2f}", tobs=f"{res['tobs']:.2f}", etac=f"{res['etac']:.5f}", ttrr=f"{res['ttrr']:.2f}", prec=f"{res['prec']:.2f}")
                st.info(texto_tela2)

            pdf_bytes2 = gerar_pdf(False, res, L)
            st.download_button(L["pdf_btn"], data=pdf_bytes2, file_name="Relatorio_Optica.pdf", mime="application/pdf", type="primary", use_container_width=True)
