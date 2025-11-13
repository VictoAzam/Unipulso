# 🏥 Unipulso - Gerador de Pulseiras Hospitalares

> Sistema profissional para geração, impressão e exportação de pulseiras de identificação hospitalar

![Versão](https://img.shields.io/badge/versão-3.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Licença](https://img.shields.io/badge/licença-Interno-orange)

---

## ✨ Características

- ✅ **Interface Gráfica Intuitiva** - Sistema de abas, sidebar informativa, navegação fácil
- ✅ **Impressão Direta Zebra ZD230** - Impressão via ZPL sem diálogos do sistema
- ✅ **Cadastro Individual** - Formulário completo de atendimento
- ✅ **Importação CSV** - Processamento em lote de pacientes
- ✅ **Exportação Múltipla** - PNG e PDF com qualidade profissional
- ✅ **Layout Customizável** - Editor visual drag & drop
- ✅ **QR Code Automático** - Geração baseada no número da carteirinha
- ✅ **Fontes Personalizadas** - Suporte a fontes do sistema e customizadas

---

## 🚀 Início Rápido

### 1. Instalação

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar aplicativo
python app.py
```

### 2. Primeiro Uso

1. **Cadastrar Paciente**: Clique em "🏥 Novo Atendimento"
2. **OU Importar CSV**: Menu > Arquivo > Importar CSV
3. **Visualizar**: Navegue entre pulseiras com ◀ ▶
4. **Exportar**: Menu > Exportar > PNG ou PDF
5. **Imprimir**: Menu > Impressão (requer Zebra ZD230)

---

## 📊 Importação de CSV

### Formato Esperado

```csv
Número da carteirinha,Nome do paciente,Data de nascimento,Nome da mãe,Convênio,Médico responsável,Sexo,Data de admissão,Hora de admissão,Observação
123456,João Silva,15/03/1985,Maria Silva,UNIMED,Dr. Carlos,Masculino,12/11/2025,14:30,Alergia a dipirona
```

**Baixar exemplos**: Menu > Arquivo > Baixar Exemplo CSV

---

## 🖨️ Impressão Zebra ZD230

### Configuração Rápida

```bash
# 1. Instalar dependência
pip install pywin32

# 2. Instalar driver Zebra
# Download: https://www.zebra.com/

# 3. Conectar impressora USB

# 4. Configurar no app
# Menu > Impressão > Configurar Impressora
```

### Impressão

- **Pulseira Atual**: Botão "🖨️ Imprimir Atual" na sidebar
- **Todas as Pulseiras**: Menu > Impressão > Imprimir Todas
- **Teste**: Menu > Impressão > Teste de Impressão

---

## 📁 Estrutura do Projeto

```
Unipulso/
├── app.py                    # Interface principal
├── DOCUMENTACAO_COMPLETA.md  # Documentação completa
├── IMPRESSAO_ZEBRA_README.md # Guia de impressão
├── GUIA_CSV.md              # Guia de importação CSV
├── core/                     # Núcleo do sistema
│   ├── config.py            # Configurações
│   ├── models.py            # Modelos de dados
│   ├── render.py            # Renderização
│   └── io_manager.py        # I/O CSV/PNG/PDF
├── ui/                       # Interface gráfica
│   ├── layout_editor.py     # Editor visual
│   └── atendimento_form.py  # Formulário de cadastro
├── utils/                    # Utilitários
│   ├── helpers.py           # Funções auxiliares
│   └── zebra_printer.py     # Impressão Zebra
├── data/                     # Dados CSV
├── output/                   # Saídas PNG/PDF
├── templates/                # Modelos de layout
├── logo/                     # Logotipos
└── fonte padrao/             # Fontes do projeto
```

---

## 📚 Documentação

- **[DOCUMENTACAO_COMPLETA.md](DOCUMENTACAO_COMPLETA.md)** - Guia completo do sistema
- **[IMPRESSAO_ZEBRA_README.md](IMPRESSAO_ZEBRA_README.md)** - Configuração e uso da impressora
- **[GUIA_CSV.md](GUIA_CSV.md)** - Formato e importação de CSV
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Arquitetura técnica
- **[MODULAR_GUIDE.md](docs/MODULAR_GUIDE.md)** - Guia de desenvolvimento

### 📦 Distribuição

- **[RESUMO_INSTALADOR.md](RESUMO_INSTALADOR.md)** - Resumo do sistema de instalador (COMECE AQUI)
- **[GUIA_INSTALADOR.md](GUIA_INSTALADOR.md)** - Guia completo de criação do instalador
- **[BUILD_SYSTEM_INDEX.md](BUILD_SYSTEM_INDEX.md)** - Índice de arquivos de build
- **[CHECKLIST_BUILD.md](CHECKLIST_BUILD.md)** - Checklist de qualidade pré-release

---

## 🎁 Criar Instalador Windows

Para distribuir o Unipulso como instalador profissional (.exe):

### Pré-requisitos

1. **PyInstaller**: `pip install pyinstaller`
2. **Inno Setup**: [Download aqui](https://jrsoftware.org/isdl.php)

### Build Rápido (1 comando)

```batch
build_all.bat
```

Isso cria:
- `dist/Unipulso.exe` (executável standalone)
- `installer_output/Unipulso_Setup_v1.0.0.exe` (instalador Windows)

### Distribuição

O instalador criado:
- ✅ Não requer Python instalado
- ✅ Instala em `C:\Program Files\Unipulso`
- ✅ Cria atalhos (Menu Iniciar + Desktop)
- ✅ Permite desinstalação pelo Painel de Controle

**Para detalhes completos**, veja **[RESUMO_INSTALADOR.md](RESUMO_INSTALADOR.md)**

---

## 🛠️ Tecnologias

- **Python 3.8+**
- **tkinter + ttkbootstrap** - Interface gráfica moderna
- **Pillow (PIL)** - Processamento de imagens
- **qrcode** - Geração de QR Codes
- **reportlab** - Exportação PDF
- **pywin32** - Impressão Zebra (Windows)

---

## ⚙️ Requisitos

### Mínimos
- Python 3.8 ou superior
- Windows 10/11 (ou Linux com CUPS para impressão)
- 2GB RAM
- 100MB espaço em disco

### Recomendados
- Python 3.10+
- 4GB RAM
- Impressora Zebra ZD230 (para impressão direta)

---

## 🎯 Funcionalidades Principais

### Interface Gráfica
- **Abas**: Pré-visualização, Exportação, Impressão
- **Sidebar**: Informações em tempo real (CSV, Logo, Fonte, Impressora)
- **Navegação**: Anterior/Próximo entre pacientes
- **Ações Rápidas**: Novo Atendimento, Importar, Editor, Imprimir

### Formulário de Atendimento
- Cadastro completo do paciente
- Data/Hora automática
- Opção "Salvar e Adicionar Outro"
- Validação de campos

### Exportação
- **PNG**: Arquivos individuais por paciente
- **PDF**: Documento único com todas as pulseiras
- Alta qualidade (300 DPI)

### Impressão
- Impressão direta via ZPL
- Detecção automática de impressoras
- Teste de impressão
- Impressão em lote com progresso

### Layout
- Editor visual drag & drop
- Elementos: Texto, QR Code
- Propriedades: Posição, tamanho, rotação, cor, fonte, alinhamento
- Salvar/Carregar modelos JSON

---

## 🆘 Troubleshooting

### Problema: Erro ao importar CSV
**Solução**: Verificar codificação UTF-8 e formato de colunas

### Problema: Impressora não encontrada
**Solução**: Menu > Impressão > Configurar Impressora > Selecionar impressora correta

### Problema: Campos não aparecem no PDF
**Solução**: Verificar se CSV possui todas as colunas obrigatórias

### Problema: Fontes não carregam
**Solução**: Verificar pasta "fonte padrao" com arquivos .ttf

---

## 📞 Suporte

Para mais informações, consulte a **[DOCUMENTACAO_COMPLETA.md](DOCUMENTACAO_COMPLETA.md)**

---

## 📝 Licença

Este projeto é de uso interno hospitalar.

---

**Desenvolvido com ❤️ para o setor de saúde**

Última atualização: 12/11/2025

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Toolkit](https://img.shields.io/badge/Toolkit-Tkinter%20%2B%20ttkbootstrap-7952B3)
![OS](https://img.shields.io/badge/OS-Linux%20%7C%20Windows-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

Aplicativo desktop para gerar pulseiras/cartõezinhos de pacientes com QR Code, dados estruturados e layout pronto para impressão. Funciona em Linux e Windows.

## Recursos principais

- Interface gráfica com ttkbootstrap (Tkinter)
- Importação de CSV com colunas padronizadas
- Upload de logotipo (renderizado maior e alinhado à esquerda da área não-imprimível)
- QR Code por número da carteirinha
- Layout de impressão com:
  - Nome do paciente centralizado, em negrito e com tamanho independente (padrão: 50px)
  - Número da carteirinha visível em texto (abaixo do nome)
  - Dados em duas colunas na área imprimível, evitando sobreposição
  - Carimbo de data/hora de geração (DD/MM/AAAA HH:MM:SS)
  - Bordas da área imprimível para referência
  - Texto adicional (se presente) com fonte ampliada para melhor legibilidade
- Exportação
  - PNG: um único PNG empilhado ou vários PNGs (um por pulseira)
  - PDF: um único PDF com páginas múltiplas ou vários PDFs (um por pulseira)
- Preferências de fonte persistentes em `~/.unipulso_prefs.json`

## Requisitos

- Python 3.8+
- Tkinter (no Windows já vem com o instalador oficial; no Linux pode ser necessário instalar o pacote `tk` da distribuição)
- Pacotes Python:
  - `ttkbootstrap`
  - `Pillow`
  - `qrcode`
  - `reportlab`

Você pode instalar tudo via `requeriments.txt` (veja a seção Instalação).

## Instalação

Recomendado usar um ambiente virtual (venv).

### Linux (Debian/Ubuntu)

```bash
# Dependências do sistema (tkinter e fontconfig para listar fontes)
sudo apt update
sudo apt install -y python3-venv python3-pip python3-tk fontconfig

# Criar e ativar o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependências do projeto
pip install -r requeriments.txt
```

### Windows (PowerShell)

```powershell
# Criar e ativar o ambiente virtual
py -m venv .venv
.\.venv\Scripts\Activate.ps1

# Instalar dependências do projeto
pip install -r requeriments.txt
```

Caso prefira, instale diretamente os pacotes:

```bash
pip install ttkbootstrap pillow qrcode reportlab
```

## Como executar

```bash
# Estando no diretório do projeto (com o venv ativo)
python app.py
```

## Como usar

1) Upload do logotipo (opcional)
- Clique em "Upload Logotipo" e escolha uma imagem (PNG/JPG). Ela é renderizada maior e mais à esquerda na área não-imprimível.

2) Baixar um CSV de exemplo (opcional)
- "Baixar Exemplo CSV" gera um arquivo com 2 registros para referência.
- "Baixar Modelo CSV (vazio)" gera apenas o cabeçalho esperado.

3) Importar CSV
- Clique em "Importar CSV" e selecione o arquivo com as colunas esperadas (ver seção "Formato do CSV").

4) Configurar fonte
- "Configurar Fonte" permite ajustar:
  - Família
  - Tamanho base (para os campos gerais)
  - Negrito/Itálico
  - Tamanho do Nome (px) — padrão 50px, independente dos demais textos
  - Auto-ajustar para caber — o app pode reduzir automaticamente os textos para evitar cortes
  - Salvar como padrão — persiste as escolhas em `~/.unipulso_prefs.json`

5) Pré-visualização
- A primeira pulseira é mostrada no painel de prévia.

6) Exportar
- PNG: o app pergunta se você deseja gerar arquivos separados (um PNG por pulseira) ou um único PNG com todas empilhadas verticalmente.
- PDF: o app pergunta se você deseja gerar vários PDFs (um por pulseira) ou um único PDF com páginas múltiplas.

## Capturas de tela

Coloque imagens em `./assets/` e referencie aqui:

![Pré-visualização](./assets/preview.png)
![Export Dialog](./assets/export_dialog.png)

## Demonstração (GIF)

Inclua um GIF curto de uso em `./assets/demo.gif` e referencie:

![Demo](./assets/demo.gif)

## Formato do CSV

Cabeçalho esperado (nesta ordem):

```csv
Número da carteirinha,Nome do paciente,Data de nascimento,Nome da mãe,Convênio,Médico responsável,Sexo,Data de admissão,Hora de admissão
```

Exemplo de conteúdo:

```csv
Número da carteirinha,Nome do paciente,Data de nascimento,Nome da mãe,Convênio,Médico responsável,Sexo,Data de admissão,Hora de admissão
123456,João Silva,1990-05-12,Maria Silva,SUS,Dra. Aline,M,2025-10-15,14:30
987654,Ana Pereira,1985-08-01,Clara Pereira,Particular,Dr. Bruno,F,2025-10-15,15:10
```

Campo extra opcional (para deixar o texto em maior destaque): `Texto adicional` (ou `Texto Adicional`).

## Notas de compatibilidade (Linux/Windows)

- Linux
  - O app usa `fc-list` (fontconfig) para localizar fontes. Se não estiver instalado, a busca cai para varredura de pastas padrão.
  - Instale o pacote `fontconfig` para melhor detecção de fontes.
  - Se o Tkinter não estiver disponível, instale o pacote `python3-tk`.

- Windows
  - As fontes são procuradas também em `C:\\Windows\\Fonts`.
  - O Tkinter vem com o instalador oficial do Python.

## Preferências salvas

As preferências são gravadas em:
- Linux: `/home/<usuario>/.unipulso_prefs.json`
- Windows: `C:\\Users\\<usuario>\\.unipulso_prefs.json`

As chaves incluem: `font_family`, `font_size`, `font_bold_flag`, `font_italic_flag`, `name_font_size`, `auto_fit_enabled`.

## Solução de problemas

- Erro de módulos ausentes (ModuleNotFoundError):
  - Ative o venv e rode `pip install -r requeriments.txt`.
- Tkinter ausente no Linux:
  - `sudo apt install python3-tk` (Debian/Ubuntu). Em outras distros, instale o pacote equivalente.
- Fontes não aparecem corretamente:
  - Instale `fontconfig` no Linux (`sudo apt install fontconfig`).
  - No Windows, verifique se a família selecionada possui variações Bold/Italic; em caso de dúvida, escolha outra família.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](./LICENSE) para mais detalhes.

## Como publicar no GitHub

```bash
# Inicializar o repositório (se ainda não estiver versionado)
git init

git add .

git commit -m "feat: primeira versão do Gerador de Pulseiras"

# Conectar ao repositório remoto (substitua pelo seu URL)
git branch -M main
git remote add origin https://github.com/<seu-usuario>/<seu-repo>.git

git push -u origin main
```
