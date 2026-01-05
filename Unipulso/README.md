# Gerador de Pulseiras Hospitalares (Unipulso)

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
