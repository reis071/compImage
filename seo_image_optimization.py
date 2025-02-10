import os
import sys
import subprocess
import flet as ft
from PIL import Image

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

# Configuração padrão
MAX_WIDTH = 1200  # Largura máxima da imagem

# Determina a pasta da Área de Trabalho do usuário
desktop_folder = os.path.join(os.path.expanduser("~"), "Desktop")  # Windows, macOS e Linux compatível
DEFAULT_OUTPUT_FOLDER = os.path.join(desktop_folder, "imagens_otimizadas")  # Criará na área de trabalho

# Mapeamento dos níveis de qualidade
QUALITY_LEVELS = {
    "Altíssima (100%)": 100,
    "Alta (90%)": 90,
    "Média (80%)": 80,
    "Baixa (60%)": 60,
    "Muito Baixa (40%)": 40,
}

def main(page: ft.Page):
    page.title = "CompImage "
    page.padding = 20
    page.spacing = 20

    # Variáveis para armazenar os diretórios, nome base, formato de saída e qualidade
    input_folder = ft.TextField(label="📁 Pasta de Entrada", hint_text="Digite o caminho da pasta", expand=True)
    output_folder = ft.TextField(label="📂 Pasta de Saída (Opcional)", hint_text=f"Se não informado, criará {DEFAULT_OUTPUT_FOLDER}", expand=True)
    name_prefix = ft.TextField(label="🔤 Nome base das imagens", hint_text="Ex: produto-xyz", expand=True)

    # Opção de formato de saída
    output_format = ft.Dropdown(
        label="📷 Formato de saída",
        options=[
            ft.dropdown.Option("webp"),
            ft.dropdown.Option("jpg"),
            ft.dropdown.Option("jpeg"),
            ft.dropdown.Option("png"),
        ],
        value="webp",  # Valor padrão
        expand=True
    )

    # Opção de qualidade
    quality_level = ft.Dropdown(
        label="🎚 Qualidade da imagem",
        options=[ft.dropdown.Option(q) for q in QUALITY_LEVELS.keys()],
        value="Média (80%)",  # Padrão
        expand=True
    )

    # Área de logs
    log_text = ft.Text(value="📜 Logs da conversão aparecerão aqui...", size=12, selectable=True)

    def otimizar_imagens(e):
        """Processa as imagens e exibe os logs."""
        input_path = input_folder.value.strip()
        output_path = output_folder.value.strip() or DEFAULT_OUTPUT_FOLDER  # Se não passar, usa a pasta da Área de Trabalho

        # Verifica se a pasta de entrada existe
        if not os.path.exists(input_path):
            log_text.value = f"❌ A pasta de entrada '{input_path}' não existe. Verifique o caminho."
            page.update()
            return

        if not name_prefix.value.strip():
            log_text.value = "⚠️ Defina um nome base para os arquivos!"
            page.update()
            return

        if not output_format.value:
            log_text.value = "⚠️ Selecione um formato de saída!"
            page.update()
            return

        if not quality_level.value:
            log_text.value = "⚠️ Selecione um nível de qualidade!"
            page.update()
            return

        quality = QUALITY_LEVELS[quality_level.value]  # Define a qualidade com base na escolha do usuário

        # Criar pasta de saída se não existir
        os.makedirs(output_path, exist_ok=True)

        imagens = [f for f in os.listdir(input_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if not imagens:
            log_text.value = "⚠️ Nenhuma imagem encontrada na pasta selecionada!"
            page.update()
            return

        log_text.value = f"🔄 Iniciando a conversão para {output_format.value.upper()} com qualidade {quality_level.value}..."
        page.update()

        erros = []
        for index, filename in enumerate(imagens, start=1):
            try:
                img = Image.open(os.path.join(input_path, filename))
                img.verify()
                img = Image.open(os.path.join(input_path, filename)).convert("RGB")

                # Redimensionamento se necessário
                if img.width > MAX_WIDTH:
                    img.thumbnail((MAX_WIDTH, img.height * MAX_WIDTH // img.width))

                # Criar nome único para a imagem com o formato escolhido
                new_name = f"{name_prefix.value.strip()}-{index}.{output_format.value}"
                output_file = os.path.join(output_path, new_name)

                # Salvar imagem no formato escolhido com a qualidade definida
                img.save(output_file, output_format.value.upper(), quality=quality)
                log_text.value += f"\n✅ {filename} → {new_name} ({quality_level.value})"
                page.update()
            except Exception as err:
                erros.append(filename)
                log_text.value += f"\n❌ Erro ao processar {filename}: {err}"
                page.update()

        if erros:
            log_text.value += f"\n⚠️ {len(erros)} imagens apresentaram erros."

        log_text.value += f"\n🚀 Conversão concluída! Arquivos salvos em '{output_path}'."
        page.update()

    # Botão para iniciar conversão (MAIOR E MAIS ESTILIZADO)
    btn_iniciar = ft.ElevatedButton(
        text="🚀 INICIAR CONVERSÃO",
        on_click=otimizar_imagens,
        bgcolor=ft.colors.GREEN,
        color=ft.colors.WHITE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),  # Borda arredondada
            padding=20,  # Maior área de clique
            text_style=ft.TextStyle(size=18, weight="bold")  # Texto maior e negrito
        ),
        width=300,  # Largura maior para destacar o botão
        height=60  # Altura maior para tornar mais visível
    )

    # Organização do layout
    page.add(
        ft.Text("💡 Otimizador de Imagens", size=24, weight="bold"),
        ft.Row([input_folder, output_folder], spacing=20),
        ft.Row([name_prefix, output_format, quality_level], spacing=20),
        ft.Row([btn_iniciar], alignment="center"),
        ft.Text("📜 Logs:", size=18, weight="bold"),
        log_text
    )

ft.app(target=main)
