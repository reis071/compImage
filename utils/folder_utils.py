import os
import webbrowser
from utils.filename_utils import format_path

def open_folder(input_folder_value, output_folder_value):
    output_path = format_path(output_folder_value.strip())
    if not output_path:
        output_path = f"{format_path(input_folder_value.strip())}-otimizada"
    webbrowser.open(f"file://{os.path.abspath(output_path)}")
