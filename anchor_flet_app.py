# anchor_flet_app.py
import flet as ft
import math

def main(page: ft.Page):
    page.title = "Analisador de Ancoragens"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    
    # ========== VARIÁVEIS GLOBAIS ==========
    unit_type = "N"  # "N" ou "kgf"
    
    # ========== FUNÇÕES DE CONVERSÃO ==========
    def n_to_kgf(n):
        return n / 9.80665
    
    def kgf_to_n(kgf):
        return kgf * 9.80665
    
    # ========== REFERÊNCIAS DOS CAMPOS ==========
    # Dados do Ponto
    point_name = ft.TextField(label="Nome do Ponto", value="C00", width=300)
    point_type = ft.Dropdown(label="Tipo", value="Outlet", width=300,
                              options=[ft.dropdown.Option("Inlet"), ft.dropdown.Option("Outlet")])
    d_nom = ft.TextField(label="Diâmetro Nominal (mm)", value="350", width=300)
    
    # Cargas Aplicadas
    fx = ft.TextField(label="Fx", value="-70", width=200)
    fy = ft.TextField(label="Fy", value="-3661", width=200)
    fz = ft.TextField(label="Fz", value="-114", width=200)
    mx = ft.TextField(label="Mx", value="-415", width=200)
    my = ft.TextField(label="My", value="71", width=200)
    mz = ft.TextField(label="Mz", value="3151", width=200)
    
    # Valores Admissíveis
    allow_fx = ft.TextField(label="Fx Adm", value="25095", width=200)
    allow_fy = ft.TextField(label="Fy Adm", value="62450", width=200)
    allow_fz = ft.TextField(label="Fz Adm", value="49900", width=200)
    allow_mx = ft.TextField(label="Mx Adm", value="379", width=200)
    allow_my = ft.TextField(label="My Adm", value="191", width=200)
    allow_mz = ft.TextField(label="Mz Adm", value="191", width=200)
    
    # Limit 2
    fc = ft.TextField(label="Fc (kgf)", value="4314.654", width=250)
    mc = ft.TextField(label="Mc (kgf.cm)", value="21930.49", width=250)
    dc = ft.TextField(label="Dc (mm)", value="290.815", width=250)
    
    # Área de resultados
    result_text = ft.TextField(
        label="Resultados da Análise",
        multiline=True,
        min_lines=20,
        max_lines=30,
        read_only=True,
        width=900,
        height=500
    )
    
    # ========== FUNÇÃO PRINCIPAL DE ANÁLISE ==========
    def analyze(e):
        try:
            # Verificar unidade
            unit = unit_type
            
            # Coletar valores
            fx_val = float(fx.value)
            fy_val = float(fy.value)
            fz_val = float(fz.value)
            mx_val = float(mx.value)
            my_val = float(my.value)
            mz_val = float(mz.value)
            
            # Converter se necessário (kgf para N)
            if unit == "kgf":
                fx_val = kgf_to_n(fx_val)
                fy_val = kgf_to_n(fy_val)
                fz_val = kgf_to_n(fz_val)
                mx_val = kgf_to_n(mx_val) / 100  # kgf.cm -> N.m
                my_val = kgf_to_n(my_val) / 100
                mz_val = kgf_to_n(mz_val) / 100
            
            # Coletar valores admissíveis
            allow_fx_val = float(allow_fx.value)
            allow_fy_val = float(allow_fy.value)
            allow_fz_val = float(allow_fz.value)
            allow_mx_val = float(allow_mx.value)
            allow_my_val = float(allow_my.value)
            allow_mz_val = float(allow_mz.value)
            
            if unit == "kgf":
                allow_fx_val = kgf_to_n(allow_fx_val)
                allow_fy_val = kgf_to_n(allow_fy_val)
                allow_fz_val = kgf_to_n(allow_fz_val)
                allow_mx_val = kgf_to_n(allow_mx_val) / 100
                allow_my_val = kgf_to_n(allow_my_val) / 100
                allow_mz_val = kgf_to_n(allow_mz_val) / 100
            
            # Coletar dados do Limit 2
            fc_val = float(fc.value)
            mc_val = float(mc.value)
            dc_val = float(dc.value)
            
            # Cálculos
            fr = math.sqrt(fx_val**2 + fy_val**2 + fz_val**2)
            
            # Construir resultado
            results = []
            results.append("=" * 70)
            results.append(f"ANÁLISE DO PONTO: {point_name.value}")
            results.append(f"Tipo: {point_type.value}")
            results.append("=" * 70)
            
            # Forças
            results.append("\n📊 FORÇAS APLICADAS:")
            results.append(f"Fx: {fx_val:>10.2f} N ({n_to_kgf(fx_val):>10.2f} kgf) | Adm: {allow_fx_val:>10.2f} N")
            results.append(f"Fy: {fy_val:>10.2f} N ({n_to_kgf(fy_val):>10.2f} kgf) | Adm: {allow_fy_val:>10.2f} N")
            results.append(f"Fz: {fz_val:>10.2f} N ({n_to_kgf(fz_val):>10.2f} kgf) | Adm: {allow_fz_val:>10.2f} N")
            results.append(f"FR: {fr:>10.2f} N ({n_to_kgf(fr):>10.2f} kgf)")
            
            # Momentos
            results.append("\n🔄 MOMENTOS APLICADOS:")
            results.append(f"Mx: {mx_val:>10.2f} N.m ({n_to_kgf(mx_val*100):>10.2f} kgf.cm) | Adm: {allow_mx_val:>10.2f} N.m")
            results.append(f"My: {my_val:>10.2f} N.m ({n_to_kgf(my_val*100):>10.2f} kgf.cm) | Adm: {allow_my_val:>10.2f} N.m")
            results.append(f"Mz: {mz_val:>10.2f} N.m ({n_to_kgf(mz_val*100):>10.2f} kgf.cm) | Adm: {allow_mz_val:>10.2f} N.m")
            
            # Verificação de Cargas
            results.append("\n✅ VERIFICAÇÃO DE CARGAS:")
            checks_passed = True
            
            # Verificar forças
            for name, val, adm in [("Fx", abs(fx_val), allow_fx_val), 
                                    ("Fy", abs(fy_val), allow_fy_val), 
                                    ("Fz", abs(fz_val), allow_fz_val)]:
                if val > adm:
                    results.append(f"❌ {name}: {val:.2f} > {adm:.2f} (excesso: {(val-adm)/adm*100:.1f}%)")
                    checks_passed = False
                else:
                    results.append(f"✅ {name}: {val:.2f} ≤ {adm:.2f}")
            
            # Verificar momentos
            for name, val, adm in [("Mx", abs(mx_val), allow_mx_val), 
                                    ("My", abs(my_val), allow_my_val), 
                                    ("Mz", abs(mz_val), allow_mz_val)]:
                if val > adm:
                    results.append(f"❌ {name}: {val:.2f} > {adm:.2f} (excesso: {(val-adm)/adm*100:.1f}%)")
                    checks_passed = False
                else:
                    results.append(f"✅ {name}: {val:.2f} ≤ {adm:.2f}")
            
            # Critério Limit 2
            results.append("\n📐 CRITÉRIO LIMIT 2:")
            left_side = 1.0 * fc_val + 1.640 * mc_val
            right_side = 21.900 * dc_val
            
            results.append(f"Fc: {fc_val:.3f} kgf")
            results.append(f"Mc: {mc_val:.3f} kgf.cm")
            results.append(f"Dc: {dc_val:.3f} mm")
            results.append(f"Lado Esquerdo: {left_side:.2f}")
            results.append(f"Lado Direito: {right_side:.2f}")
            
            if left_side <= right_side:
                results.append(f"✅ Limit 2 ATENDIDO")
            else:
                results.append(f"❌ Limit 2 NÃO ATENDIDO (excesso: {(left_side-right_side)/right_side*100:.1f}%)")
                checks_passed = False
            
            # Resultado Final
            results.append("\n" + "=" * 70)
            if checks_passed:
                results.append("✅ RESULTADO FINAL: PONTO APROVADO!")
            else:
                results.append("❌ RESULTADO FINAL: PONTO REPROVADO!")
            results.append("=" * 70)
            
            # Atualizar texto do resultado
            result_text.value = "\n".join(results)
            page.update()
            
        except Exception as err:
            result_text.value = f"❌ ERRO NA ANÁLISE:\n{str(err)}"
            page.update()
    
    # ========== FUNÇÃO PARA LIMPAR RESULTADOS ==========
    def clear_results(e):
        result_text.value = ""
        page.update()
    
    # ========== FUNÇÃO PARA TROCAR UNIDADE ==========
    def change_unit(e):
        nonlocal unit_type
        unit_type = e.control.value
        unit_label.value = f"Unidade atual: {unit_type} / {unit_type}.m"
        page.update()
    
    # ========== CONSTRUÇÃO DA INTERFACE ==========
    
    # Cabeçalho
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("Analisador de Ancoragens", size=32, weight="bold", color=ft.Colors.BLUE_700),
                ft.Text("Sistema de Verificação de Cargas e Momentos", size=16, color=ft.Colors.GREY_600),
            ]),
            margin=ft.margin.only(bottom=20)
        )
    )
    
    # Seletor de Unidade
    unit_label = ft.Text("Unidade atual: N / N.m", size=14, weight="bold")
    
    unit_selector = ft.RadioGroup(
        value="N",
        on_change=change_unit,
        content=ft.Row([
            ft.Radio(value="N", label="N / N.m"),
            ft.Radio(value="kgf", label="kgf / kgf.cm"),
        ])
    )
    
    # Usando Container com título em vez de ExpansionTile (mais compatível)
    
    # Aba 1: Dados do Ponto
    ponto_header = ft.Container(
        content=ft.Text("📌 Dados do Ponto", size=18, weight="bold"),
        bgcolor=ft.Colors.BLUE_100,
        padding=10,
        border_radius=5,
        margin=ft.margin.only(top=10, bottom=5)
    )
    
    ponto_content = ft.Container(
        content=ft.Column([
            ft.Row([point_name, point_type]),
            ft.Row([d_nom]),
        ]),
        padding=20,
        bgcolor=ft.Colors.GREY_50,
        border_radius=5
    )
    
    # Aba 2: Cargas Aplicadas
    cargas_header = ft.Container(
        content=ft.Text("⚡ Cargas Aplicadas", size=18, weight="bold"),
        bgcolor=ft.Colors.GREEN_100,
        padding=10,
        border_radius=5,
        margin=ft.margin.only(top=10, bottom=5)
    )
    
    cargas_content = ft.Container(
        content=ft.Column([
            ft.Text("Forças (N ou kgf):", weight="bold"),
            ft.Row([fx, fy, fz]),
            ft.Divider(height=10, color="transparent"),
            ft.Text("Momentos (N.m ou kgf.cm):", weight="bold"),
            ft.Row([mx, my, mz]),
        ]),
        padding=20,
        bgcolor=ft.Colors.GREY_50,
        border_radius=5
    )
    
    # Aba 3: Valores Admissíveis
    admissiveis_header = ft.Container(
        content=ft.Text("✅ Valores Admissíveis", size=18, weight="bold"),
        bgcolor=ft.Colors.ORANGE_100,
        padding=10,
        border_radius=5,
        margin=ft.margin.only(top=10, bottom=5)
    )
    
    admissiveis_content = ft.Container(
        content=ft.Column([
            ft.Text("Forças Admissíveis (N ou kgf):", weight="bold"),
            ft.Row([allow_fx, allow_fy, allow_fz]),
            ft.Divider(height=10, color="transparent"),
            ft.Text("Momentos Admissíveis (N.m ou kgf.cm):", weight="bold"),
            ft.Row([allow_mx, allow_my, allow_mz]),
        ]),
        padding=20,
        bgcolor=ft.Colors.GREY_50,
        border_radius=5
    )
    
    # Aba 4: Critério Limit 2
    limit2_header = ft.Container(
        content=ft.Text("📐 Critério Limit 2", size=18, weight="bold"),
        bgcolor=ft.Colors.PURPLE_100,
        padding=10,
        border_radius=5,
        margin=ft.margin.only(top=10, bottom=5)
    )
    
    limit2_content = ft.Container(
        content=ft.Column([
            ft.Text("Fórmula: 1.000 × Fc + 1.640 × Mc ≤ 21.900 × Dc", 
                   weight="bold", color=ft.Colors.BLUE_700),
            ft.Divider(),
            ft.Row([fc, mc, dc]),
            ft.Text("Onde:", size=12, color=ft.Colors.GREY_600),
            ft.Text("Fc = Força combinada (kgf)", size=12),
            ft.Text("Mc = Momento combinado (kgf.cm)", size=12),
            ft.Text("Dc = Diâmetro combinado (mm)", size=12),
        ]),
        padding=20,
        bgcolor=ft.Colors.GREY_50,
        border_radius=5
    )
    
    # Botões de ação
    action_buttons = ft.Row([
        ft.ElevatedButton(
            "🔍 ANALISAR ANCORAGEM",
            on_click=analyze,
            icon=ft.Icons.ANALYTICS,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.GREEN_700,
            width=250,
            height=50
        ),
        ft.OutlinedButton(
            "🗑️ LIMPAR RESULTADOS",
            on_click=clear_results,
            icon=ft.Icons.CLEAR,
            width=200,
            height=50
        )
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
    
    # Adicionar tudo à página
    page.add(
        ft.Divider(),
        unit_selector,
        unit_label,
        ft.Divider(),
        ponto_header,
        ponto_content,
        cargas_header,
        cargas_content,
        admissiveis_header,
        admissiveis_content,
        limit2_header,
        limit2_content,
        ft.Divider(height=20),
        action_buttons,
        ft.Divider(height=20),
        result_text
    )

# ========== INICIAR APLICATIVO ==========
if __name__ == "__main__":
    ft.app(target=main)
