
```markdown

# CompImage - Compressor de Imagens Offline

**CompImage** é uma aplicação de interface gráfica feita com [Flet](https://flet.dev/)

Ideal para quem trabalha com marketing, e-commerce, blogs ou redes sociais

---

## 🛠 Funcionalidades

- 🗂 Seleção da pasta de entrada e saída
- 🖼️ Renomeia imagens com prefixo personalizado e nome da empresa (útil para branding)
- 🔢 Opção de numeração automática nos arquivos
- 🔄 Redimensionamento inteligente mantendo proporção
- ⚙️ Escolha da qualidade (de 40% até 100%)
- 📸 Suporte aos formatos `jpg`, `jpeg`, `png`, `webp`
- 🔋 Interface simples e intuitiva com barra de progresso
- 💻 Totalmente offline

---

## 🧰 Tecnologias utilizadas

- [Python 3](https://www.python.org/) - Linguagem de programação
- [Flet](https://flet.dev/) - Para a interface gráfica
- [Pillow (PIL)](https://python-pillow.org/) - Para manipulação das imagens
- `threading`, `os`, `subprocess`, `webbrowser` - Módulos padrão do Python

---

## 🛠️ Instalação

1. **Clone o repositório:**

```bash
git clone https://github.com/reis071/compImage.git
cd compImage


2. **Crie e ative um ambiente virtual (opcional, mas recomendado):**

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

3. **Instale as dependências:**

O próprio app instala as dependências automaticamente se você rodar direto o `main.py`.

Ou, se preferir instalar manualmente:

```bash
pip install -r requirements.txt
```

---

## ▶️ Como usar

Execute o aplicativo com:

```bash
python main.py
```

**OU** apenas apertando o botão de executar da sua IDE.

1. Escolha a pasta com as imagens que deseja otimizar.  
2. Defina as opções desejadas: nome base, tamanho, qualidade, formato, etc.  
3. Clique em **"🚀 INICIAR CONVERSÃO"**.  
4. Ao final, clique em **"📂 Abrir Pasta"** para visualizar os arquivos otimizados.

---

## 📁 Estrutura da aplicação

```
compimage/
│
├── main.py                # Código principal do app
├── requirements.txt       # Dependências do projeto
├── README.md              # Este arquivo
```

---

## 💡 Sugestões de uso

- Otimizar imagens de produtos para e-commerce (ex: `camiseta-verde-lojaXYZ.jpg`)  
- Reduzir o peso de imagens para melhorar a velocidade de sites  
- Gerar imagens padronizadas para redes sociais (ex: stories ou posts do Instagram)  
- Criar miniaturas otimizadas para YouTube, blogs, etc.

---

## 🧑‍💻 Autor

Desenvolvido por [Guilherme Reis Correia](https://github.com/reis071)
```

