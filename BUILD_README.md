# Gerador de Pulseiras Hospitalares - Build Instructions

## 🏗️ Como gerar o executável Windows (.exe)

### No Linux (onde você está agora):

1. **Instale o PyInstaller:**
   ```bash
   pip install pyinstaller
   ```

2. **Gere o executável:**
   ```bash
   python build_exe.py
   ```
   
   OU use o script automático:
   ```bash
   chmod +x build.sh
   ./build.sh
   ```

3. **Pegue o executável:**
   - O arquivo estará em: `dist/GeradorPulseiras.exe`
   - Copie para o Windows e pronto!

### No Windows (método alternativo):

Se preferir compilar diretamente no Windows:

1. **Instale Python no Windows** (python.org)

2. **Instale as dependências:**
   ```cmd
   pip install -r requeriments.txt
   pip install pyinstaller
   ```

3. **Gere o executável:**
   ```cmd
   python build_exe.py
   ```

## 📦 O que o executável inclui?

- ✅ Todas as dependências (ttkbootstrap, Pillow, qrcode, reportlab)
- ✅ Interface gráfica completa
- ✅ Não precisa instalar Python no Windows
- ✅ Arquivo único e portátil

## 🎯 Distribuição

O arquivo `GeradorPulseiras.exe` pode ser:
- Copiado para qualquer computador Windows
- Executado diretamente sem instalação
- Distribuído para outros usuários

### 📁 Arquivos de Configuração

O aplicativo cria automaticamente um arquivo de preferências:
- **Linux/macOS**: `~/.unipulso_prefs.json`
- **Windows**: `C:\Users\[usuário]\.unipulso_prefs.json`

Este arquivo guarda:
- ✅ Configurações de fonte personalizadas
- ✅ **Caminho do logo padrão** (se configurado)
- ✅ Preferências de interface

**Importante**: Se o usuário configurar um logo padrão e depois mover ou deletar o arquivo de imagem, o logo não será carregado automaticamente (mas o programa continuará funcionando normalmente).

## 🐛 Problemas comuns

**Erro "ModuleNotFoundError":**
- Certifique-se que todas as dependências estão instaladas
- Execute: `pip install -r requeriments.txt`

**Antivírus bloqueando:**
- É normal, executáveis do PyInstaller podem ser detectados como falso positivo
- Adicione exceção no antivírus se necessário

**Ícone não aparece:**
- Crie um arquivo `icon.ico` na raiz do projeto
- O PyInstaller vai usar automaticamente

**Logo padrão não carrega:**
- Verifique se o arquivo de imagem ainda existe no caminho original
- Reconfigure o logo usando o botão "Upload Logotipo"

## 📝 Notas

- O executável tem ~50-80MB (inclui Python + todas bibliotecas)
- Primeira execução pode ser mais lenta (extraindo arquivos temporários)
- Funciona em Windows 7, 8, 10 e 11
- Logo padrão é salvo por usuário (cada usuário pode ter seu próprio logo)
