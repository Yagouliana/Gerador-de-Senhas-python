import flet as ft
import random
import string

def main(page: ft.Page):
    page.title = "Gerador de Senhas"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 350
    page.window_height = 600
    page.padding = 20

    senha_atual = ""
    senha_visivel = True  # Para controlar mostrar/ocultar senha

    def gerar_senha(e):
        nonlocal senha_atual
        comprimento = int(slider.value)
        caracteres = ""
        if upper_switch.value:
            caracteres += string.ascii_uppercase
        if lower_switch.value:
            caracteres += string.ascii_lowercase
        if numbers_switch.value:
            caracteres += string.digits
        if symbols_switch.value:
            caracteres += string.punctuation

        if caracteres:
            senha = "".join(random.choice(caracteres) for _ in range(comprimento))
            senha_output.value = senha if senha_visivel else "●" * len(senha)
            senha_atual = senha
            copiar_btn.visible = True
            limpar_btn.visible = True
            salvar_btn.visible = True
            mostrar_btn.visible = True
            text_display.visible = False
        else:
            senha_output.value = "Selecione ao menos um tipo de caractere."
            senha_atual = ""
            copiar_btn.visible = False
            limpar_btn.visible = False
            salvar_btn.visible = False
            mostrar_btn.visible = False
        page.update()

    def mostrar_senha_copiada(e):
        if senha_atual:
            text_display.value = f"Senha copiada: {senha_atual}"
            text_display.visible = True
            try:
                page.set_clipboard(senha_atual)
            except:
                pass
        page.update()

    def limpar_senha(e):
        nonlocal senha_atual
        senha_atual = ""
        senha_output.value = ""
        text_display.visible = False
        copiar_btn.visible = False
        limpar_btn.visible = False
        salvar_btn.visible = False
        mostrar_btn.visible = False
        page.update()

    def salvar_senha(e):
        if senha_atual:
            with open("senhas_salvas.txt", "a", encoding="utf-8") as f:
                f.write(senha_atual + "\n")
            text_display.value = "Senha salva em senhas_salvas.txt"
            text_display.visible = True
            page.update()

    def toggle_mostrar(e):
        nonlocal senha_visivel
        senha_visivel = not senha_visivel
        if senha_atual:
            senha_output.value = senha_atual if senha_visivel else "●" * len(senha_atual)
        mostrar_btn.text = "OCULTAR SENHA" if senha_visivel else "MOSTRAR SENHA"
        page.update()

    def toggle_theme(e):
        nonlocal is_dark
        is_dark = not is_dark
        page.theme_mode = ft.ThemeMode.DARK if is_dark else ft.ThemeMode.LIGHT
        theme_button.icon = ft.Icons.DARK_MODE if is_dark else ft.Icons.LIGHT_MODE
        page.update()

    is_dark = False

    theme_button = ft.IconButton(
        icon=ft.Icons.LIGHT_MODE,
        on_click=toggle_theme
    )

    title_switch_row = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[ft.Text("Gerador de Senhas", size=28, weight="bold"), theme_button]
    )

    senha_output = ft.TextField(
        value="",
        label="Senha Gerada",
        read_only=True,
        width=280,
        bgcolor=ft.Colors.ON_SURFACE_VARIANT
    )

    text_display = ft.Text(value="", color=ft.Colors.GREEN, visible=False)

    copiar_btn = ft.ElevatedButton(text="COPIAR SENHA", on_click=mostrar_senha_copiada,
                                   color=ft.Colors.ON_SECONDARY, bgcolor=ft.Colors.SECONDARY, visible=False)

    limpar_btn = ft.ElevatedButton(text="LIMPAR SENHA", on_click=limpar_senha,
                                   color=ft.Colors.ON_ERROR, bgcolor=ft.Colors.ERROR, visible=False)

    salvar_btn = ft.ElevatedButton(text="SALVAR SENHA", on_click=salvar_senha,
                                   color=ft.Colors.ON_TERTIARY, bgcolor=ft.Colors.TERTIARY, visible=False)

    mostrar_btn = ft.ElevatedButton(text="OCULTAR SENHA", on_click=toggle_mostrar,
                                    color=ft.Colors.ON_PRIMARY_CONTAINER, bgcolor=ft.Colors.PRIMARY_CONTAINER, visible=False)

    slider = ft.Slider(min=8, max=20, value=12, divisions=12, label="CARACTERES: {value}")

    upper_switch = ft.Switch(label="Letras maiúsculas")
    lower_switch = ft.Switch(label="Letras minúsculas", value=True)
    numbers_switch = ft.Switch(label="Incluir números")
    symbols_switch = ft.Switch(label="Incluir símbolos")

    gerar_button = ft.ElevatedButton(text="GERAR SENHA", on_click=gerar_senha,
                                     color=ft.Colors.ON_PRIMARY, bgcolor=ft.Colors.PRIMARY)

    page.add(
        ft.Column(
            [
                title_switch_row,
                senha_output,
                text_display,
                copiar_btn,
                limpar_btn,
                salvar_btn,
                mostrar_btn,
                slider,
                upper_switch,
                lower_switch,
                numbers_switch,
                symbols_switch,
                gerar_button,
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )
    )

ft.app(target=main, assets_dir="assets")
