import os
import sys
import threading
import subprocess
import webbrowser


# Lista de dependências necessárias
dependencias = ["flet", "pillow"]

def verificar_instalacao(biblioteca):
    """Verifica se a biblioteca está instalada usando pip show"""
    try:
        resultado = subprocess.run(
            [sys.executable, "-m", "pip", "show", biblioteca],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return bool(resultado.stdout)
    except Exception:
        return False

def instalar_dependencias():
    """Instala apenas as bibliotecas que ainda não estão instaladas"""
    bibliotecas_faltando = [lib for lib in dependencias if not verificar_instalacao(lib)]
    if not bibliotecas_faltando:
        print("\n✅ Todas as dependências já estão instaladas.")
        return

    print(f"\n📦 Instalando: {', '.join(bibliotecas_faltando)}...")
    subprocess.run([sys.executable, "-m", "pip", "install", *bibliotecas_faltando], check=True)
    print("\n✅ Instalação concluída!")

# Verificar e instalar dependências antes de rodar o script
instalar_dependencias()

import flet as ft
from PIL import Image

# Configuração padrão
DEFAULT_MAX_WIDTH = 1200  # Largura máxima padrão da imagem
DEFAULT_MAX_HEIGHT = 1200 # Altura máxima padrão da imagem
QUALITY_LEVELS = {
    "Altíssima (100%)": 100,
    "Alta (90%)": 90,
    "Média (80%)": 80,
    "Baixa (60%)": 60,
    "Muito Baixa (40%)": 40,
}

MAX_SIZE_OPTIONS = ["800x800", "1200x1200", "1600x1600", "Original"]

# Funções auxiliares
def sanitize_filename(filename):
    """Substitui espaços por hífens no nome do arquivo e limita o tamanho para SEO."""
    sanitized = filename.replace(" ", "-")
    return sanitized[:50]  # Limita o nome do arquivo a 50 caracteres

def format_path(path):
    """Substitui \ por / no caminho do diretório."""
    return path.replace("\\", "/")

def open_folder(e):
    """Abre a pasta de saída no explorador de arquivos."""
    output_path = format_path(output_folder.value.strip())
    if not output_path:
        output_path = f"{format_path(input_folder.value.strip())}-otimizada"
    webbrowser.open(f"file://{os.path.abspath(output_path)}")

def compress_image(input_path, output_path, quality, format_, max_size):
    """Compressão de imagens mantendo qualidade e redimensionando."""
    try:
        img = Image.open(input_path)
        img = img.convert("RGB")
        
        if max_size != "Original":
            max_width, max_height = map(int, max_size.split("x"))
            img.thumbnail((max_width, max_height))
        
        img.save(output_path, format_.upper(), quality=quality)
        return True
    except Exception as e:
        return str(e)

def main(page: ft.Page):
    page.title = "CompImage - Compressor de Imagens Offline"
    page.padding = 20
    page.spacing = 20


    # Componentes da interface
    global output_folder, input_folder
    input_folder = ft.TextField(label="📁 Pasta de Entrada", hint_text="Digite o caminho da pasta", expand=True)
    output_folder = ft.TextField(label="📂 Pasta de Saída (Opcional)", hint_text="Se não informado, será criada dentro da pasta de entrada", expand=True)
    name_prefix = ft.TextField(label="🔤 Nome base das imagens", hint_text="Ex: produto-xyz", expand=True)
    company_name = ft.TextField(label="🏢 Nome da Empresa", hint_text="Digite o nome da empresa para SEO", expand=True)
    numbering_toggle = ft.Switch(label="🔢 Numerar imagens automaticamente", value=False)
    
    max_size_dropdown = ft.Dropdown(
        label="📏 Tamanho Máximo (Largura x Altura)",
        options=[ft.dropdown.Option(option) for option in MAX_SIZE_OPTIONS],
        value="1200x1200", expand=True
    )
    
    output_format = ft.Dropdown(
        label="📷 Formato de saída",
        options=[
            ft.dropdown.Option("webp"),
            ft.dropdown.Option("jpg"),
            ft.dropdown.Option("jpeg"),
            ft.dropdown.Option("png"),
        ],
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
    open_folder_button = ft.ElevatedButton(text="📂 Abrir Pasta", visible=False, on_click=open_folder)
    
    def start_compression(e):
        input_path = format_path(input_folder.value.strip())
        output_path = format_path(output_folder.value.strip())
        
        if not output_path:
            output_path = f"{input_path}-otimizada"
        
        os.makedirs(output_path, exist_ok=True)
        
        quality = QUALITY_LEVELS[quality_level.value]
        format_ = output_format.value
        max_size = max_size_dropdown.value
        
        if not os.path.exists(input_path):
            log_text.value = f"❌ A pasta de entrada '{input_path}' não existe. Verifique o caminho."
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
        
        log_text.value = ""
        log_text.visible = False
        progress_bar.value = 0
        progress_bar.visible = True
        progress_text.visible = True
        page.update()
        
        def process_images():
            for index, input_file in enumerate(images, start=1):
                relative_path = os.path.relpath(input_file, input_path)
                output_file = os.path.join(output_path, relative_path)
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                
                filename = os.path.basename(input_file)
                base_name = name_prefix.value.strip() if name_prefix.value.strip() else os.path.splitext(filename)[0]
                new_name = sanitize_filename(f"{base_name}-{company_name.value.strip()}{('-' + str(index)) if numbering_toggle.value else ''}.{format_}")
                output_file = os.path.join(os.path.dirname(output_file), new_name)
                
                compress_image(input_file, output_file, quality, format_, max_size)
                
                progress_percentage = (index / len(images)) * 100
                progress_bar.value = progress_percentage / 100
                progress_text.value = f"{int(progress_percentage)}%"
                page.update()
            
            progress_bar.visible = False
            progress_text.visible = False
            success_text.value = f"✅ Compressão concluída! Arquivos salvos em: {output_path}"
            success_text.visible = True
            open_folder_button.visible = True
            page.update()
        
        threading.Thread(target=process_images).start()
    def on_hover(e):
        e.control.bgcolor = "blue" if e.data == "true" else "black"
        e.control.update()
    
    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            theme_button.text = "🌑"
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_button.text = "☀️"
        page.update()

    # Button to toggle theme
    theme_button = ft.ElevatedButton(
        text="☀️  " if page.theme_mode == ft.ThemeMode.LIGHT else "🌑",
        on_click=toggle_theme
    )

   
    page.add(
        ft.Text("💡 CompImage - Compressor de Imagens Offline", size=24, weight="bold"),
        ft.Row([input_folder, output_folder], spacing=20),
        ft.Row([name_prefix, company_name, max_size_dropdown, output_format, quality_level], spacing=20),
        numbering_toggle,theme_button,
        ft.Row([ft.ElevatedButton(text="🚀 INICIAR CONVERSÃO", on_click=start_compression, bgcolor="black", color="white", on_hover=on_hover)], alignment="center"),
        
        ft.Row([progress_bar], alignment="center"),
        ft.Row([progress_text], alignment="center"),
        success_text,
        open_folder_button,
        log_text
    )

ft.app(target=main)