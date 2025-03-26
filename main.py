from core.dependecy_checker import ensure_dependencies
ensure_dependencies()

import flet as ft
from ui.app import main

ft.app(target=main)
