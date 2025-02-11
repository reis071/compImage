import os
import sys
import threading
import shutil
from datetime import datetime

# Lista de dependências necessárias
REQUIRED_LIBS = ["flet", "Pillow"]

# Função para verificar e instalar dependências ausentes
def check_and_install_dependencies():
    missing_libs = []
    for lib in REQUIRED_LIBS:
        try:
            __import__(lib)
        except ImportError:
            missing_libs.append(lib)
    
    if missing_libs:
        print(f"🔧 Instalando dependências ausentes: {', '.join(missing_libs)}...")
        os.system(f"{sys.executable} -m pip install {' '.join(missing_libs)}")

# Executa a verificação antes de iniciar o programa
check_and_install_dependencies()

import flet as ft
from PIL import Image

# Configuração padrão
DEFAULT_MAX_WIDTH = 1200  # Largura máxima padrão da imagem
QUALITY_LEVELS = {
    "Altíssima (100%)": 100,
    "Alta (90%)": 90,
    "Média (80%)": 80,
    "Baixa (60%)": 60,
    "Muito Baixa (40%)": 40,
}

MAX_WIDTH_OPTIONS = ["800", "1200", "1600", "Original"]

# Funções auxiliares
def sanitize_filename(filename):
    """Substitui espaços por hífens no nome do arquivo e limita o tamanho para SEO."""
    sanitized = filename.replace(" ", "-")
    return sanitized[:50]  # Limita o nome do arquivo a 50 caracteres

def format_path(path):
    """Substitui \ por / no caminho do diretório."""
    return path.replace("\\", "/")

def compress_image(input_path, output_path, quality, format_, max_width):
    """Compressão de imagens mantendo qualidade e redimensionando."""
    try:
        img = Image.open(input_path)
        img = img.convert("RGB")
        
        if max_width != "Original":
            max_width = int(max_width)
            if img.width > max_width:
                img.thumbnail((max_width, img.height * max_width // img.width))
        
        img.save(output_path, format_.upper(), quality=quality)
        return True
    except Exception as e:
        return str(e)

def main(page: ft.Page):
    page.title = "Compressor de Imagens Offline"
    page.padding = 20
    page.spacing = 20
    page.theme_mode = "light"

    # Componentes da interface
    input_folder = ft.TextField(label="📁 Pasta de Entrada", hint_text="Digite o caminho da pasta", expand=True)
    output_folder = ft.TextField(label="📂 Pasta de Saída (Opcional)", hint_text="Se não informado, será criada dentro da pasta de entrada", expand=True)
    name_prefix = ft.TextField(label="🔤 Nome base das imagens", hint_text="Ex: produto-xyz", expand=True)
    company_name = ft.TextField(label="🏢 Nome da Empresa", hint_text="Digite o nome da empresa para SEO", expand=True)
    
    max_width_dropdown = ft.Dropdown(
        label="📏 Largura Máxima",
        options=[ft.dropdown.Option(option) for option in MAX_WIDTH_OPTIONS],
        value="1200", expand=True
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
    
    def start_compression(e):
        input_path = format_path(input_folder.value.strip())
        output_path = format_path(output_folder.value.strip())
        
        if not output_path:
            output_path = f"{input_path}-otimizada"
        
        os.makedirs(output_path, exist_ok=True)
        
        quality = QUALITY_LEVELS[quality_level.value]
        format_ = output_format.value
        max_width = max_width_dropdown.value
        
        if not os.path.exists(input_path):
            log_text.value = f"❌ A pasta de entrada '{input_path}' não existe. Verifique o caminho."
            log_text.visible = True
            page.update()
            return
        
        images = []
        for root, _, files in os.walk(input_path):  # Mantém a estrutura de pastas
            for file in files:
                if file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                    images.append(os.path.join(root, file))
        
        total_images = len(images)
        
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
            errors = []
            for index, input_file in enumerate(images, start=1):
                relative_path = os.path.relpath(input_file, input_path)
                output_file = os.path.join(output_path, relative_path)
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                
                filename = os.path.basename(input_file)
                new_name = sanitize_filename(f"{name_prefix.value.strip()}-{company_name.value.strip()}-{index}.{format_}")
                output_file = os.path.join(os.path.dirname(output_file), new_name)
                
                result = compress_image(input_file, output_file, quality, format_, max_width)
                if result is not True:
                    errors.append(filename)
                    log_text.value += f"\n❌ Erro ao processar {filename}: {result}"
                    log_text.visible = True
                
                progress_percentage = (index / total_images) * 100
                progress_bar.value = progress_percentage / 100
                progress_text.value = f"Progresso: {int(progress_percentage)}%"
                page.update()
            
            if errors:
                log_text.value += f"\n⚠️ {len(errors)} imagens apresentaram erros."
                log_text.visible = True
            else:
                log_text.value = f"🚀 Compressão concluída! Arquivos salvos em '{output_path}'."
                log_text.visible = True
            
            progress_bar.visible = False
            progress_text.visible = False
            page.update()
        
        threading.Thread(target=process_images).start()
    
    btn_compress = ft.ElevatedButton(
        text="🚀 INICIAR CONVERSÃO",
        on_click=start_compression,
        bgcolor=ft.colors.GREEN,
        color=ft.colors.WHITE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=20,
            text_style=ft.TextStyle(size=18, weight="bold")
        ),
        width=300,
        height=60
    )
    
    page.add(
        ft.Text("💡 Compressor de Imagens Offline", size=24, weight="bold"),
        ft.Row([input_folder, output_folder], spacing=20),
        ft.Row([name_prefix, company_name, max_width_dropdown, output_format, quality_level], spacing=20),
        ft.Row([btn_compress], alignment="center"),
        ft.Row([progress_bar]),
        progress_text,
        log_text
    )

ft.app(target=main)