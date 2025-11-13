# 📦 Guia de Criação do Instalador Unipulso

> Documentação completa para gerar o instalador Windows do Unipulso

---

## 🎯 Visão Geral

Este guia explica como criar um instalador profissional `.exe` para Windows que:

- ✅ Empacota toda a aplicação em um único executável
- ✅ Inclui todas as dependências Python automaticamente
- ✅ Cria instalador com atalhos (Desktop + Menu Iniciar)
- ✅ Permite desinstalação pelo Painel de Controle
- ✅ Não requer Python instalado no computador destino

---

## 📋 Pré-requisitos

### 1. Python e Dependências

```powershell
# Ativar ambiente virtual
.\.venv\Scripts\Activate.ps1

# Instalar PyInstaller
pip install pyinstaller
```

### 2. Inno Setup (apenas para criar instalador)

**Download**: https://jrsoftware.org/isdl.php

**Instalação**: Execute o instalador e siga as instruções padrão.

**Localização esperada**:
- `C:\Program Files (x86)\Inno Setup 6\ISCC.exe` (padrão)

---

## 🚀 Processo de Build (2 Etapas)

### Etapa 1: Criar Executável com PyInstaller

```powershell
# Método 1: Script automatizado (RECOMENDADO)
python build_exe.py

# Método 2: Manual
pyinstaller unipulso.spec --clean
```

**Resultado**: `dist/Unipulso.exe` (executável standalone)

**Tempo estimado**: 2-5 minutos

**Tamanho esperado**: 40-80 MB (todas dependências embutidas)

---

### Etapa 2: Criar Instalador com Inno Setup

```powershell
# Script automatizado (RECOMENDADO)
python build_installer.py

# Método manual (se tiver ISCC.exe no PATH)
iscc installer.iss
```

**Resultado**: `installer_output/Unipulso_Setup_v1.0.0.exe`

**Tempo estimado**: 30 segundos - 1 minuto

**Tamanho esperado**: 35-75 MB (compactado)

---

## 📂 Estrutura de Arquivos

```
Unipulso/
├── app.py                    # Aplicação principal
├── unipulso.spec            # ✨ Configuração PyInstaller
├── build_exe.py             # ✨ Script de build executável
├── installer.iss            # ✨ Script Inno Setup
├── build_installer.py       # ✨ Script de build instalador
├── build_all.bat            # ✨ Build completo (1 clique)
│
├── core/                    # Módulos principais
├── ui/                      # Interface gráfica
├── utils/                   # Utilitários
│
├── logo/                    # Logos e ícones
│   └── icon.ico            # ⚠️ Criar ícone 256x256
│
├── fonte padrao/            # Fontes padrão
├── templates/               # Templates salvos
├── data/                    # Dados de exemplo
│
├── dist/                    # 📦 Saída PyInstaller
│   └── Unipulso.exe        # Executável gerado
│
└── installer_output/        # 📦 Saída Inno Setup
    └── Unipulso_Setup_v1.0.0.exe  # Instalador final
```

---

## 🔧 Arquivos de Configuração

### unipulso.spec (PyInstaller)

Define como o executável será criado:

- **hiddenimports**: Módulos Python que devem ser incluídos
- **datas**: Arquivos de recursos (logos, fontes, templates)
- **excludes**: Módulos desnecessários (reduz tamanho)
- **console=False**: Aplicação GUI (sem janela de console)
- **icon**: Ícone do executável

### installer.iss (Inno Setup)

Define o comportamento do instalador:

- **Diretório padrão**: `C:\Program Files\Unipulso`
- **Atalhos**: Desktop (opcional) + Menu Iniciar
- **Compressão**: LZMA2/max (melhor compactação)
- **Desinstalação**: Registro no Painel de Controle
- **Idioma**: Português do Brasil

---

## ⚡ Build Rápido (1 Clique)

Execute o script `build_all.bat`:

```batch
build_all.bat
```

Isso executa automaticamente:
1. Limpeza de builds anteriores
2. Criação do executável (PyInstaller)
3. Criação do instalador (Inno Setup)

---

## 🧪 Testes

### Testar Executável

```powershell
# Execute o executável diretamente
.\dist\Unipulso.exe
```

**Verificar**:
- ✅ Aplicação abre sem erros
- ✅ Interface carrega corretamente
- ✅ Importação de CSV funciona
- ✅ Exportação de PDF funciona
- ✅ Impressão Zebra detecta impressora

### Testar Instalador

1. **Execute** `installer_output/Unipulso_Setup_v1.0.0.exe`
2. **Siga** o assistente de instalação
3. **Verifique** atalhos criados
4. **Execute** pelo Menu Iniciar
5. **Teste** desinstalação pelo Painel de Controle

---

## 🎨 Personalização

### Criar Ícone Personalizado

**Requisitos**: Imagem 256x256 px (PNG ou SVG)

**Método 1: Online**
- Acesse: https://icoconvert.com/
- Upload sua imagem
- Download como `.ico`
- Salve em `logo/icon.ico`

**Método 2: Python (Pillow)**

```python
from PIL import Image

# Abrir imagem original
img = Image.open('logo/logo.png')

# Redimensionar para múltiplos tamanhos (ícone multi-resolução)
img.save('logo/icon.ico', format='ICO', sizes=[(16,16), (32,32), (48,48), (256,256)])
```

### Alterar Informações do Instalador

Edite `installer.iss`:

```ini
#define MyAppName "Unipulso"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Seu Nome"
#define MyAppURL "https://seu-site.com"
```

---

## 🐛 Solução de Problemas

### Erro: "PyInstaller não encontrado"

```powershell
pip install pyinstaller
```

### Erro: "Inno Setup não encontrado"

1. Instale de: https://jrsoftware.org/isdl.php
2. Verifique caminho em `build_installer.py`

### Erro: "Módulo X não encontrado" ao executar .exe

Adicione ao `hiddenimports` em `unipulso.spec`:

```python
hiddenimports = [
    # ... existentes ...
    'nome_do_modulo',
]
```

Reconstrua com `python build_exe.py`.

### Executável muito grande (>100 MB)

Adicione mais exclusões em `unipulso.spec`:

```python
excludes=[
    'matplotlib',
    'numpy',
    'pandas',
    'scipy',
    'pytest',
    'unittest',
    'tkinter.test',  # Testes do tkinter
],
```

### Erro: "Icon.ico não encontrado"

Opção 1: Crie o ícone (veja seção **Criar Ícone Personalizado**)

Opção 2: Remova referência em `unipulso.spec`:

```python
icon=None,  # Sem ícone personalizado
```

---

## 📊 Checklist de Release

Antes de distribuir o instalador:

- [ ] Testado em Windows 10/11 limpo
- [ ] Todas funcionalidades verificadas
- [ ] Sem erros no console (se abrir com --console)
- [ ] Ícone aparece corretamente
- [ ] Atalhos funcionam
- [ ] Desinstalação remove tudo
- [ ] README.md atualizado com versão
- [ ] Changelog documentado

---

## 🚀 Distribuição

### Onde hospedar o instalador?

1. **GitHub Releases** (grátis, recomendado)
   - Crie release na aba "Releases"
   - Upload do `.exe` como asset

2. **Google Drive / OneDrive** (simples)
   - Upload e compartilhe link

3. **Site próprio** (profissional)
   - Hospede em servidor web

### Informações para usuários finais

```markdown
## Download

📥 **[Download Unipulso v1.0.0](link-do-instalador)**

### Requisitos
- Windows 10/11 (64-bit)
- 100 MB de espaço em disco

### Instalação
1. Execute `Unipulso_Setup_v1.0.0.exe`
2. Siga o assistente de instalação
3. Pronto! O aplicativo está no Menu Iniciar
```

---

## 📝 Notas Técnicas

### O que PyInstaller faz?

1. Analisa `app.py` e detecta dependências
2. Coleta todos módulos Python necessários
3. Empacota Python runtime + bibliotecas
4. Inclui recursos (logos, fontes, etc.)
5. Gera executável standalone (não precisa Python instalado)

### O que Inno Setup faz?

1. Cria instalador Windows padrão
2. Copia arquivos para `C:\Program Files`
3. Cria atalhos no sistema
4. Registra no Painel de Controle (desinstalação)
5. Compacta tudo em único `.exe`

### Vantagens da abordagem PyInstaller + Inno Setup

✅ **Usuário final**: Instalação simples (clique duplo)  
✅ **Desenvolvedor**: Controle total sobre instalação  
✅ **Profissional**: Aparência nativa do Windows  
✅ **Segurança**: Assinatura digital possível (futuro)  
✅ **Updates**: Fácil distribuir novas versões  

---

## 📚 Referências

- **PyInstaller**: https://pyinstaller.org/
- **Inno Setup**: https://jrsoftware.org/isinfo.php
- **Python Packaging**: https://packaging.python.org/

---

**Última atualização**: 12/11/2025  
**Versão do guia**: 1.0
