import os
import threading
import flet as ft
from core.compress import compress_image
from utils.filename_utils import sanitize_filename, format_path
from utils.folder_utils import open_folder

QUALITY_LEVELS = {
    "Altíssima (100%)": 100,
    "Alta (90%)": 90,
    "Média (80%)": 80,
    "Baixa (60%)": 60,
    "Muito Baixa (40%)": 40,
}

MAX_SIZE_OPTIONS = {
    "Full HD (1920x1080)": (1920, 1080),
    "HD (1600x900)": (1600, 900),
    "Web Padrão (1200x800)": (1200, 800),
    "Instagram Post (1080x1080)": (1080, 1080),
    "Stories/Reels (1080x1920)": (1080, 1920),
    "Miniatura (800x800)": (800, 800),
    "Thumbnail (600x400)": (600, 400),
    "Perfil Pequeno (400x400)": (400, 400),
    "Original": None
}

def main(page: ft.Page):
    page.title = "CompImage - Compressor de Imagens Offline"
    page.padding = 20
    page.spacing = 20

    global output_folder, input_folder
    input_folder = ft.TextField(label="📁 Pasta de Entrada", hint_text="Digite o caminho da pasta", expand=True)
    output_folder = ft.TextField(label="📂 Pasta de Saída (Opcional)", hint_text="Se não informado, será criada dentro da pasta de entrada", expand=True)
    name_prefix = ft.TextField(label="🔤 Nome base das imagens", hint_text="Ex: produto-xyz", expand=True)
    company_name = ft.TextField(label="🏢 Nome da Empresa", hint_text="Digite o nome da empresa para SEO", expand=True)
    numbering_toggle = ft.Switch(label="🔢 Numerar imagens automaticamente", value=False)

    max_size_dropdown = ft.Dropdown(
        label="📏 Tamanho Máximo",
        options=[ft.dropdown.Option(option) for option in MAX_SIZE_OPTIONS.keys()],
        value="Full HD (1920x1080)", expand=True
    )

    output_format = ft.Dropdown(
        label="📷 Formato de saída",
        options=[ft.dropdown.Option(fmt) for fmt in ["webp", "jpg", "jpeg", "png"]],
        value="webp", expand=True
    )

    quality_level = ft.Dropdown(
        label="🎚 Qualidade da imagem",
        options=[ft.dropdown.Option(q) for q in QUALITY_LEVELS.keys()],
        value="Média (80%)", expand=True
    )

    progress_bar = ft.ProgressBar(width=400, height=10, visible=False)
    progress_text = ft.Text("", size=14, visible=False)
    log_text = ft.Text(value="", size=12, selectable=True, visible=False)
    success_text = ft.Text(value="", size=16, weight="bold", color="green", visible=False)
    open_folder_button = ft.ElevatedButton(text="📂 Abrir Pasta", visible=False, on_click=lambda e: open_folder(input_folder.value, output_folder.value))

    def start_compression(e):
        input_path = format_path(input_folder.value.strip())
        output_path = format_path(output_folder.value.strip())

        if not output_path:
            output_path = f"{input_path}-otimizada"

        os.makedirs(output_path, exist_ok=True)

        quality = QUALITY_LEVELS[quality_level.value]
        format_ = output_format.value
        max_size = MAX_SIZE_OPTIONS[max_size_dropdown.value]

        if not os.path.exists(input_path):
            log_text.value = f"❌ A pasta de entrada '{input_path}' não existe."
            log_text.visible = True
            page.update()
            return

        images = [
            os.path.join(root, file)
            for root, _, files in os.walk(input_path)
            for file in files if file.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
        ]

        if not images:
            log_text.value = "⚠️ Nenhuma imagem encontrada na pasta selecionada!"
            log_text.visible = True
            page.update()
            return

        log_text.visible = False
        progress_bar.value = 0
        progress_bar.visible = True
        progress_text.visible = True
        page.update()

        def process_images():
            for index, input_file in enumerate(images, start=1):
                filename = os.path.basename(input_file)
                base_name = name_prefix.value.strip() or os.path.splitext(filename)[0]
                base_name = sanitize_filename(base_name)

                company = company_name.value.strip()
                numbering = f"-{index}" if numbering_toggle.value else ""

                if company:
                    new_name = f"{base_name}-{company}{numbering}.{format_}"
                else:
                    new_name = f"{base_name}{numbering}.{format_}"

                output_file = os.path.join(output_path, new_name)
                compress_image(input_file, output_file, quality, format_, max_size)

                progress_bar.value = index / len(images)
                progress_text.value = f"{int((index / len(images)) * 100)}%"
                page.update()

            progress_bar.visible = False
            success_text.value = f"✅ Compressão concluída! Arquivos salvos em: {output_path}"
            success_text.visible = True
            open_folder_button.visible = True
            page.update()

        threading.Thread(target=process_images).start()

    page.add(
        ft.Text("💡 CompImage - Compressor de Imagens Offline", size=24, weight="bold"),
        ft.Row([input_folder, output_folder], spacing=20),
        ft.Row([name_prefix, company_name, max_size_dropdown, output_format, quality_level], spacing=20),
        numbering_toggle,
        ft.Row([ft.ElevatedButton(text="🚀 INICIAR CONVERSÃO", on_click=start_compression)], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([progress_bar], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([progress_text], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([success_text], alignment=ft.MainAxisAlignment.CENTER),
        open_folder_button,
        log_text
    )
