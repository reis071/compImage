import subprocess
import sys

def ensure_dependencies(requirements_file="requirements.txt"):
    try:
        with open(requirements_file, "r") as file:
            dependencies = [line.strip() for line in file if line.strip()]
        
        missing_packages = []
        for package in dependencies:
            package_name = package.split("==")[0]
            try:
                __import__(package_name)
            except ImportError:
                missing_packages.append(package)

        if missing_packages:
            print(f"📦 Instalando: {', '.join(missing_packages)}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing_packages])
            print("✅ Dependências instaladas!")

    except FileNotFoundError:
        print(f"❌ Arquivo {requirements_file} não encontrado!")
        sys.exit(1)
