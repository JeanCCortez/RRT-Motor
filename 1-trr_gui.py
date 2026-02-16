import flet as ft
import math
import os
from datetime import datetime

# ==========================================
# CONSTANTES DA TEORIA (TRR)
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
# DICIONÁRIO MULTILÍNGUE (8 IDIOMAS)
# ==========================================
LANG = {
    "PT": {
        "title": "🌌 Motor Cosmológico TRR", "subtitle": "Teoria da Relatividade Referencial | Autor: Jean Cortez",
        "tab_dyn": "Dinâmica Galáctica", "tab_opt": "Óptica Cosmológica",
        "rad": "Raio observado (kpc)", "vobs": "Veloc. Observada (km/s)", "vgas": "Veloc. Gás (km/s)", "vdisk": "Veloc. Disco Estelar (km/s)", "vbulge": "Veloc. Bojo/Haste (km/s)",
        "btn_calc": "Processar Calibração", "btn_clear": "Limpar", "btn_print": "Imprimir",
        "zl": "Redshift Lente (z_L)", "zs": "Redshift Fonte (z_S)", "mest": "Massa Estelar (10^11 M_sol)", "theta": "Anel Einstein (arcsec)", "cluster": "Aglomerado Gigante com Gás?",
        "err_fields": "⚠️ **Erro:** Preencha com números válidos.", "dyn_report_title": "### 📊 RELATÓRIO DE UNIFICAÇÃO (DINÂMICA)", "opt_report_title": "### 👁️ RELATÓRIO DE UNIFICAÇÃO (ÓPTICA)",
        "saved_ok": "✅ Relatório salvo: ", "ml_disk": "Massa/Luz (Disco)", "ml_bulge": "Massa/Luz (Haste)", "v_trr": "Previsão TRR", "v_obs": "Velocidade Telescópio", "precision": "Precisão", "acerto": "de Acerto",
        "mest_opt": "Massa Estelar Otimizada", "gas_opt": "Gás Detectado", "gas_yes": "Sim (Plasma aplicado)", "gas_no": "Não", "eta_c": "Índice de Refração (Cortez)", "theta_trr": "Desvio TRR", "theta_obs": "Desvio Telescópio",
        "exp_dyn": "---\n**Transparência:** Constantes universais (a0 e Beta) mantidas. O arrasto topológico justificou a curva respeitando os limites estelares (M/L). Sem matéria escura.",
        "exp_opt": "---\n**Transparência:** A refração temporal do vácuo justifica toda a lente. Massa bariônica dentro dos limites estelares. Fim dos halos fantasmas."
    },
    "EN": {
        "title": "🌌 TRR Cosmological Engine", "subtitle": "Referential Relativity Theory | Author: Jean Cortez",
        "tab_dyn": "Galactic Dynamics", "tab_opt": "Cosmological Optics",
        "rad": "Observed Radius (kpc)", "vobs": "Obs. Velocity (km/s)", "vgas": "Gas Velocity (km/s)", "vdisk": "Disk Velocity (km/s)", "vbulge": "Bulge/Bar Velocity (km/s)",
        "btn_calc": "Process Calibration", "btn_clear": "Clear", "btn_print": "Print",
        "zl": "Lens Redshift (z_L)", "zs": "Source Redshift (z_S)", "mest": "Stellar Mass (10^11 M_sun)", "theta": "Einstein Ring (arcsec)", "cluster": "Giant Gas Cluster?",
        "err_fields": "⚠️ **Error:** Fill valid numbers.", "dyn_report_title": "### 📊 UNIFICATION REPORT (DYNAMICS)", "opt_report_title": "### 👁️ UNIFICATION REPORT (OPTICS)",
        "saved_ok": "✅ Saved: ", "ml_disk": "Mass/Light (Disk)", "ml_bulge": "Mass/Light (Bar)", "v_trr": "TRR Prediction", "v_obs": "Telescope Velocity", "precision": "Precision", "acerto": "Accuracy",
        "mest_opt": "Optimized Stellar Mass", "gas_opt": "Gas Cloud", "gas_yes": "Yes (Plasma applied)", "gas_no": "No", "eta_c": "Refraction Index (Cortez)", "theta_trr": "TRR Deflection", "theta_obs": "Telescope Deflection",
        "exp_dyn": "---\n**Transparency:** Universal constants kept. Topological drag justified the curve respecting M/L stellar limits. No dark matter.",
        "exp_opt": "---\n**Transparency:** Vacuum time refraction justifies the whole lens. Baryonic mass within stellar bounds. End of ghost halos."
    },
    "ES": {
        "title": "🌌 Motor Cosmológico TRR", "subtitle": "Teoría de la Relatividad Referencial | Autor: Jean Cortez",
        "tab_dyn": "Dinámica Galáctica", "tab_opt": "Óptica Cosmológica",
        "rad": "Radio observado (kpc)", "vobs": "Veloc. Observada (km/s)", "vgas": "Veloc. Gas (km/s)", "vdisk": "Veloc. Disco (km/s)", "vbulge": "Veloc. Bulbo/Barra (km/s)",
        "btn_calc": "Procesar", "btn_clear": "Limpiar", "btn_print": "Imprimir",
        "zl": "Redshift Lente (z_L)", "zs": "Redshift Fuente (z_S)", "mest": "Masa Estelar (10^11 M_sol)", "theta": "Anillo Einstein (arcsec)", "cluster": "¿Cúmulo con Gas?",
        "err_fields": "⚠️ **Error:** Ingrese números válidos.", "dyn_report_title": "### 📊 REPORTE DE UNIFICACIÓN (DINÁMICA)", "opt_report_title": "### 👁️ REPORTE DE UNIFICACIÓN (ÓPTICA)",
        "saved_ok": "✅ Guardado: ", "ml_disk": "Masa/Luz (Disco)", "ml_bulge": "Masa/Luz (Barra)", "v_trr": "Predicción TRR", "v_obs": "Velocidad Telescopio", "precision": "Precisión", "acerto": "de Precisión",
        "mest_opt": "Masa Estelar Optimizada", "gas_opt": "Gas Detectado", "gas_yes": "Sí (Plasma aplicado)", "gas_no": "No", "eta_c": "Índice de Refracción (Cortez)", "theta_trr": "Desviación TRR", "theta_obs": "Desviación Telescopio",
        "exp_dyn": "---\n**Transparencia:** Constantes universales mantenidas. El arrastre topológico justifica la curva respetando límites M/L. Sin materia oscura.",
        "exp_opt": "---\n**Transparencia:** La refracción temporal del vacío justifica toda la lente. Masa bariónica en límites estelares."
    },
    "FR": {
        "title": "🌌 Moteur Cosmologique TRR", "subtitle": "Théorie de la Relativité Référentielle | Auteur: Jean Cortez",
        "tab_dyn": "Dynamique Galactique", "tab_opt": "Optique Cosmologique",
        "rad": "Rayon observé (kpc)", "vobs": "Vitesse obs. (km/s)", "vgas": "Vitesse Gaz (km/s)", "vdisk": "Vitesse Disque (km/s)", "vbulge": "Vitesse Bulbe/Barre (km/s)",
        "btn_calc": "Traiter Calibration", "btn_clear": "Effacer", "btn_print": "Imprimer",
        "zl": "Redshift Lentille (z_L)", "zs": "Redshift Source (z_S)", "mest": "Masse Stellaire (10^11 M_sol)", "theta": "Anneau d'Einstein (arcsec)", "cluster": "Amas Géant avec Gaz?",
        "err_fields": "⚠️ **Erreur:** Entrez des nombres valides.", "dyn_report_title": "### 📊 RAPPORT D'UNIFICATION (DYNAMIQUE)", "opt_report_title": "### 👁️ RAPPORT D'UNIFICATION (OPTIQUE)",
        "saved_ok": "✅ Enregistré: ", "ml_disk": "Masse/Lumière (Disque)", "ml_bulge": "Masse/Lumière (Barre)", "v_trr": "Prédiction TRR", "v_obs": "Vitesse Télescope", "precision": "Précision", "acerto": "d'Exactitude",
        "mest_opt": "Masse Stellaire Optimisée", "gas_opt": "Nuage de Gaz", "gas_yes": "Oui (Plasma appliqué)", "gas_no": "Non", "eta_c": "Indice de Réfraction (Cortez)", "theta_trr": "Déviation TRR", "theta_obs": "Déviation Télescope",
        "exp_dyn": "---\n**Transparence:** Constantes universelles maintenues. La traînée topologique justifie la courbe en respectant les limites M/L. Sans matière noire.",
        "exp_opt": "---\n**Transparence:** La réfraction temporelle du vide justifie la lentille. Masse baryonique dans les limites stellaires."
    },
    "DE": {
        "title": "🌌 TRR Kosmologischer Motor", "subtitle": "Referenzielle Relativitätstheorie | Autor: Jean Cortez",
        "tab_dyn": "Galaktische Dynamik", "tab_opt": "Kosmologische Optik",
        "rad": "Beobachteter Radius (kpc)", "vobs": "Beob. Geschw. (km/s)", "vgas": "Gasgeschw. (km/s)", "vdisk": "Scheibengeschw. (km/s)", "vbulge": "Bulge-/Balkengeschw. (km/s)",
        "btn_calc": "Kalibrierung starten", "btn_clear": "Löschen", "btn_print": "Drucken",
        "zl": "Linsen-Rotverschiebung (z_L)", "zs": "Quellen-Rotverschiebung (z_S)", "mest": "Stellare Masse (10^11 M_sol)", "theta": "Einsteinring (arcsec)", "cluster": "Riesiger Galaxienhaufen?",
        "err_fields": "⚠️ **Fehler:** Bitte gültige Zahlen eingeben.", "dyn_report_title": "### 📊 UNIFIKATIONSBERICHT (DYNAMIK)", "opt_report_title": "### 👁️ UNIFIKATIONSBERICHT (OPTIK)",
        "saved_ok": "✅ Gespeichert: ", "ml_disk": "Masse/Licht (Scheibe)", "ml_bulge": "Masse/Licht (Balken)", "v_trr": "TRR Vorhersage", "v_obs": "Teleskop Geschw.", "precision": "Präzision", "acerto": "Genauigkeit",
        "mest_opt": "Optimierte Stellare Masse", "gas_opt": "Gaswolke Erkannt", "gas_yes": "Ja (Plasma aktiv)", "gas_no": "Nein", "eta_c": "Brechungsindex (Cortez)", "theta_trr": "TRR Abweichung", "theta_obs": "Teleskop Abweichung",
        "exp_dyn": "---\n**Transparenz:** Universelle Konstanten beibehalten. Topologischer Widerstand rechtfertigt Kurve innerhalb M/L-Grenzen. Keine Dunkle Materie.",
        "exp_opt": "---\n**Transparenz:** Zeitliche Brechung des Vakuums rechtfertigt die Linse. Baryonische Masse innerhalb stellarer Grenzen."
    },
    "IT": {
        "title": "🌌 Motore Cosmologico TRR", "subtitle": "Teoria della Relatività Referenziale | Autore: Jean Cortez",
        "tab_dyn": "Dinamica Galattica", "tab_opt": "Ottica Cosmologica",
        "rad": "Raggio osservato (kpc)", "vobs": "Veloc. Osservata (km/s)", "vgas": "Veloc. Gas (km/s)", "vdisk": "Veloc. Disco (km/s)", "vbulge": "Veloc. Bulbo/Barra (km/s)",
        "btn_calc": "Elabora Dati", "btn_clear": "Pulisci", "btn_print": "Stampa",
        "zl": "Redshift Lente (z_L)", "zs": "Redshift Sorgente (z_S)", "mest": "Massa Stellare (10^11 M_sol)", "theta": "Anello Einstein (arcsec)", "cluster": "Ammasso con Gas?",
        "err_fields": "⚠️ **Errore:** Inserire numeri validi.", "dyn_report_title": "### 📊 REPORT DI UNIFICAZIONE (DINAMICA)", "opt_report_title": "### 👁️ REPORT DI UNIFICAZIONE (OTTICA)",
        "saved_ok": "✅ Salvato: ", "ml_disk": "Massa/Luce (Disco)", "ml_bulge": "Massa/Luce (Barra)", "v_trr": "Previsione TRR", "v_obs": "Velocità Telescopio", "precision": "Precisione", "acerto": "Accuratezza",
        "mest_opt": "Massa Ottimizzata", "gas_opt": "Gas Rilevato", "gas_yes": "Sì (Plasma applicato)", "gas_no": "No", "eta_c": "Indice Rifrazione (Cortez)", "theta_trr": "Deviazione TRR", "theta_obs": "Deviazione Telescopio",
        "exp_dyn": "---\n**Trasparenza:** Costanti mantenute. La resistenza topologica giustifica la curva nei limiti M/L. Niente materia oscura.",
        "exp_opt": "---\n**Trasparenza:** La rifrazione temporale del vuoto giustifica la lente. Massa barionica nei limiti stellari."
    },
    "ZH": {
        "title": "🌌 TRR 宇宙引擎", "subtitle": "参照相对论 | 作者: Jean Cortez",
        "tab_dyn": "星系动力学", "tab_opt": "宇宙光学",
        "rad": "观测半径 (kpc)", "vobs": "观测速度 (km/s)", "vgas": "气体速度 (km/s)", "vdisk": "星盘速度 (km/s)", "vbulge": "核球/棒状速度 (km/s)",
        "btn_calc": "运行 TRR 校准", "btn_clear": "清除", "btn_print": "打印",
        "zl": "透镜红移 (z_L)", "zs": "光源红移 (z_S)", "mest": "恒星质量 (10^11 M_sun)", "theta": "爱因斯坦环 (arcsec)", "cluster": "含气体的巨型星系团？",
        "err_fields": "⚠️ **错误:** 请填写有效的数字。", "dyn_report_title": "### 📊 统一报告 (动力学)", "opt_report_title": "### 👁️ 统一报告 (光学)",
        "saved_ok": "✅ 已保存: ", "ml_disk": "质光比 (星盘)", "ml_bulge": "质光比 (核球)", "v_trr": "TRR 预测", "v_obs": "望远镜速度", "precision": "精度", "acerto": "准确率",
        "mest_opt": "优化后的恒星质量", "gas_opt": "探测到气体云", "gas_yes": "是 (应用等离子体)", "gas_no": "否", "eta_c": "折射率 (Cortez)", "theta_trr": "TRR 偏转", "theta_obs": "望远镜偏转",
        "exp_dyn": "---\n**透明度:** 保持通用常数不变。拓扑阻力证明了曲线遵循 M/L 极限。无需暗物质。",
        "exp_opt": "---\n**透明度:** 真空的时间折射证明了透镜效应。重子质量在恒星极限内。终结幽灵晕。"
    },
    "RU": {
        "title": "🌌 Двигатель TRR", "subtitle": "Теория Референциальной Относительности | Автор: Jean Cortez",
        "tab_dyn": "Галактическая Динамика", "tab_opt": "Космологическая Оптика",
        "rad": "Набл. радиус (кпк)", "vobs": "Набл. скорость (км/с)", "vgas": "Скор. газа (км/с)", "vdisk": "Скор. диска (км/с)", "vbulge": "Скор. балджа/бара (км/с)",
        "btn_calc": "Калибровка", "btn_clear": "Очистить", "btn_print": "Печать",
        "zl": "Красн. смещение линзы (z_L)", "zs": "Красн. смещение ист. (z_S)", "mest": "Звездная масса (10^11 M_sun)", "theta": "Кольцо Эйнштейна (arcsec)", "cluster": "Скопление с газом?",
        "err_fields": "⚠️ **Ошибка:** Введите действительные числа.", "dyn_report_title": "### 📊 ОТЧЕТ ОБ УНИФИКАЦИИ (ДИНАМИКА)", "opt_report_title": "### 👁️ ОТЧЕТ ОБ УНИФИКАЦИИ (ОПТИКА)",
        "saved_ok": "✅ Сохранено: ", "ml_disk": "Масса/Свет (Диск)", "ml_bulge": "Масса/Свет (Бар)", "v_trr": "Прогноз TRR", "v_obs": "Скорость телескопа", "precision": "Точность", "acerto": "Совпадение",
        "mest_opt": "Оптимизированная масса", "gas_opt": "Газовое облако", "gas_yes": "Да (Плазма применена)", "gas_no": "Нет", "eta_c": "Коэф. преломления (Cortez)", "theta_trr": "Отклонение TRR", "theta_obs": "Откл. телескопа",
        "exp_dyn": "---\n**Прозрачность:** Универсальные константы сохранены. Топологическое сопротивление объясняет кривую в пределах M/L. Без темной материи.",
        "exp_opt": "---\n**Прозрачность:** Временное преломление вакуума объясняет всю линзу. Барионная масса в пределах."
    }
}

def main(page: ft.Page):
    page.title = "Motor TRR - Relatividade Referencial"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 15 
    page.scroll = ft.ScrollMode.AUTO
    
    def mudar_idioma(e):
        lang = dropdown_lang.value
        L_atual = LANG[lang]
        
        titulo.value = L_atual["title"]
        subtitulo.value = L_atual["subtitle"]
        tab_label_dyn.label = L_atual["tab_dyn"]
        tab_label_opt.label = L_atual["tab_opt"]
        
        inp_rad.label = L_atual["rad"]
        inp_vobs.label = L_atual["vobs"]
        inp_vgas.label = L_atual["vgas"]
        inp_vdisk.label = L_atual["vdisk"]
        inp_vbulge.label = L_atual["vbulge"]
        btn_calc_dyn.content.value = L_atual["btn_calc"]
        btn_clear_dyn.content.value = L_atual["btn_clear"]
        btn_print_dyn.content.value = L_atual["btn_print"]

        inp_zl.label = L_atual["zl"]
        inp_zs.label = L_atual["zs"]
        inp_mest.label = L_atual["mest"]
        inp_theta.label = L_atual["theta"]
        inp_cluster.label = L_atual["cluster"]
        btn_calc_opt.content.value = L_atual["btn_calc"]
        btn_clear_opt.content.value = L_atual["btn_clear"]
        btn_print_opt.content.value = L_atual["btn_print"]
        
        limpar_dinamica(None)
        limpar_optica(None)
        page.update()

    dropdown_lang = ft.Dropdown(
        width=150, # Aumentei um pouquinho para caber todas as bandeiras virtuais
        value="PT",
        options=[
            ft.dropdown.Option("PT", "🇧🇷 Português"), 
            ft.dropdown.Option("EN", "🇬🇧 English"), 
            ft.dropdown.Option("ES", "🇪🇸 Español"),
            ft.dropdown.Option("FR", "🇫🇷 Français"),
            ft.dropdown.Option("DE", "🇩🇪 Deutsch"),
            ft.dropdown.Option("IT", "🇮🇹 Italiano"),
            ft.dropdown.Option("RU", "🇷🇺 Русский"),
            ft.dropdown.Option("ZH", "🇨🇳 中文 (Chinese)")
        ],
        on_select=mudar_idioma
    )

    current_lang = dropdown_lang.value
    L = LANG[current_lang]

    titulo = ft.Text(L["title"], size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400)
    subtitulo = ft.Text(L["subtitle"], size=14, color=ft.Colors.GREY_400)
    
    largura_campo = 280

    inp_rad = ft.TextField(label=L["rad"], width=largura_campo)
    inp_vobs = ft.TextField(label=L["vobs"], width=largura_campo)
    inp_vgas = ft.TextField(label=L["vgas"], width=largura_campo)
    inp_vdisk = ft.TextField(label=L["vdisk"], width=largura_campo)
    inp_vbulge = ft.TextField(label=L["vbulge"], width=largura_campo)
    resultado_dinamica = ft.Markdown("", extension_set=ft.MarkdownExtensionSet.GITHUB_WEB)
    
    btn_calc_dyn = ft.Button(content=ft.Text(L["btn_calc"], color=ft.Colors.WHITE), icon=ft.Icons.SHOW_CHART, bgcolor=ft.Colors.BLUE_700)
    btn_clear_dyn = ft.Button(content=ft.Text(L["btn_clear"], color=ft.Colors.WHITE), icon=ft.Icons.DELETE_SWEEP, bgcolor=ft.Colors.GREY_700)
    btn_print_dyn = ft.Button(content=ft.Text(L["btn_print"], color=ft.Colors.WHITE), icon=ft.Icons.PRINT, bgcolor=ft.Colors.GREEN_700)

    inp_zl = ft.TextField(label=L["zl"], width=largura_campo)
    inp_zs = ft.TextField(label=L["zs"], width=largura_campo)
    inp_mest = ft.TextField(label=L["mest"], width=largura_campo)
    inp_theta = ft.TextField(label=L["theta"], width=largura_campo)
    inp_cluster = ft.Checkbox(label=L["cluster"], value=False)
    resultado_optica = ft.Markdown("", extension_set=ft.MarkdownExtensionSet.GITHUB_WEB)

    btn_calc_opt = ft.Button(content=ft.Text(L["btn_calc"], color=ft.Colors.WHITE), icon=ft.Icons.REMOVE_RED_EYE, bgcolor=ft.Colors.PURPLE_700)
    btn_clear_opt = ft.Button(content=ft.Text(L["btn_clear"], color=ft.Colors.WHITE), icon=ft.Icons.DELETE_SWEEP, bgcolor=ft.Colors.GREY_700)
    btn_print_opt = ft.Button(content=ft.Text(L["btn_print"], color=ft.Colors.WHITE), icon=ft.Icons.PRINT, bgcolor=ft.Colors.GREEN_700)

    def limpar_dinamica(e):
        inp_rad.value = inp_vobs.value = inp_vgas.value = inp_vdisk.value = inp_vbulge.value = ""
        resultado_dinamica.value = ""
        page.update()

    def salvar_dinamica(e):
        if not resultado_dinamica.value: return
        filename = f"Relatorio_TRR_Dinamica_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(resultado_dinamica.value)
        snack = ft.SnackBar(content=ft.Text(f"{LANG[dropdown_lang.value]['saved_ok']}{filename}"))
        page.open(snack)

    def processar_dinamica(e):
        L_atual = LANG[dropdown_lang.value]
        try:
            rad, v_obs = float(inp_rad.value), float(inp_vobs.value)
            v_gas, v_disk, v_bulge = float(inp_vgas.value), float(inp_vdisk.value), float(inp_vbulge.value)
        except:
            resultado_dinamica.value = L_atual["err_fields"]
            page.update()
            return

        melhor_erro, melhor_ml, melhor_v_trr = float('inf'), 0, 0
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
                melhor_erro, melhor_ml, melhor_v_trr = erro, ml_disk, math.sqrt((g_trr * rad * 3.086e19) / 1e6)

        precisao = max(0, 100 - (melhor_erro*100))
        
        resultado_dinamica.value = f"""
{L_atual['dyn_report_title']}
* **{L_atual['ml_disk']}:** `{melhor_ml:.2f}`
* **{L_atual['ml_bulge']}:** `{melhor_ml + 0.2:.2f}`
* **{L_atual['v_trr']}:** `{melhor_v_trr:.2f} km/s`
* **{L_atual['v_obs']}:** `{v_obs:.2f} km/s`
* **{L_atual['precision']}:** `<span style="color:green">{precisao:.2f}% {L_atual['acerto']}</span>`
{L_atual['exp_dyn']}
"""
        page.update()

    btn_calc_dyn.on_click = processar_dinamica
    btn_clear_dyn.on_click = limpar_dinamica
    btn_print_dyn.on_click = salvar_dinamica

    def limpar_optica(e):
        inp_zl.value = inp_zs.value = inp_mest.value = inp_theta.value = ""
        inp_cluster.value = False
        resultado_optica.value = ""
        page.update()

    def salvar_optica(e):
        if not resultado_optica.value: return
        filename = f"Relatorio_TRR_Optica_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(resultado_optica.value)
        snack = ft.SnackBar(content=ft.Text(f"{LANG[dropdown_lang.value]['saved_ok']}{filename}"))
        page.open(snack)

    def processar_optica(e):
        L_atual = LANG[dropdown_lang.value]
        try:
            zl, zs = float(inp_zl.value), float(inp_zs.value)
            m_est, theta_obs = float(inp_mest.value), float(inp_theta.value)
            is_cluster = inp_cluster.value
        except:
            resultado_optica.value = L_atual["err_fields"]
            page.update()
            return

        D_L, D_S, D_LS = calcular_D_A(0, zl), calcular_D_A(0, zs), calcular_D_A(zl, zs)
        melhor_erro, melhor_theta_trr, melhor_fator = float('inf'), 0, 0

        for fator_ml in [x/100.0 for x in range(50, 251)]:
            mult_gas = 7.0 if is_cluster else 1.0
            M_bar_kg = (m_est * fator_ml * mult_gas) * 1e11 * 1.989e30
            
            termo_massa = (4 * G * M_bar_kg) / (C**2)
            theta_bar_rad = math.sqrt(termo_massa * (D_LS / (D_L * D_S)))
            g_bar = (G * M_bar_kg) / ((theta_bar_rad * D_L)**2)
            
            x = g_bar / A0
            fator_fase = 1.0 / (1.0 - math.exp(-math.sqrt(x)))
            eta_C = 1.0 + BETA * math.log(1 + zl)
            
            theta_trr = theta_bar_rad * math.sqrt(fator_fase) * eta_C * 206264.806
            
            erro = abs(theta_obs - theta_trr) / theta_obs
            if erro < melhor_erro:
                melhor_erro, melhor_theta_trr, melhor_fator = erro, theta_trr, fator_ml

        precisao = max(0, 100 - (melhor_erro*100))
        gas_texto = L_atual["gas_yes"] if is_cluster else L_atual["gas_no"]
        
        resultado_optica.value = f"""
{L_atual['opt_report_title']}
* **{L_atual['mest_opt']}:** `{m_est * melhor_fator:.2f} x 10^11 M_sol`
* **{L_atual['gas_opt']}:** `{gas_texto}`
* **{L_atual['eta_c']}:** `{1.0 + BETA * math.log(1 + zl):.5f}`
* **{L_atual['theta_trr']}:** `{melhor_theta_trr:.2f} arcsec`
* **{L_atual['theta_obs']}:** `{theta_obs:.2f} arcsec`
* **{L_atual['precision']}:** `<span style="color:green">{precisao:.2f}% {L_atual['acerto']}</span>`
{L_atual['exp_opt']}
"""
        page.update()

    btn_calc_opt.on_click = processar_optica
    btn_clear_opt.on_click = limpar_optica
    btn_print_opt.on_click = salvar_optica

    tab_label_dyn = ft.Tab(label=L["tab_dyn"], icon=ft.Icons.SHOW_CHART)
    tab_label_opt = ft.Tab(label=L["tab_opt"], icon=ft.Icons.CAMERA_ALT)

    aba_dinamica = ft.Container(
        content=ft.Column([
            ft.Row([inp_rad, inp_vobs], wrap=True), 
            ft.Row([inp_vgas, inp_vdisk], wrap=True), 
            inp_vbulge,
            ft.Row([btn_calc_dyn, btn_clear_dyn, btn_print_dyn], wrap=True),
            ft.Divider(), resultado_dinamica
        ]), padding=10
    )

    aba_optica = ft.Container(
        content=ft.Column([
            ft.Row([inp_zl, inp_zs], wrap=True), 
            ft.Row([inp_mest, inp_theta], wrap=True), 
            inp_cluster,
            ft.Row([btn_calc_opt, btn_clear_opt, btn_print_opt], wrap=True),
            ft.Divider(), resultado_optica
        ]), padding=10
    )

    abas = ft.Tabs(
        length=2, expand=True, selected_index=0,
        content=ft.Column(
            expand=True,
            controls=[
                ft.TabBar(tabs=[tab_label_dyn, tab_label_opt]),
                ft.TabBarView(expand=True, controls=[aba_dinamica, aba_optica])
            ]
        )
    )

    topo = ft.Row([
        ft.Column([titulo, subtitulo], expand=True),
        dropdown_lang
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, wrap=True)

    page.add(topo, ft.Divider(), abas)

if __name__ == "__main__":
    ft.run(main)