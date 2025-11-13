# 📦 Sistema de Build e Instalador - Índice de Arquivos

> Documentação de todos os arquivos criados para o sistema de instalador do Unipulso

---

## ✅ Arquivos Criados

### 🔧 Scripts de Build

| Arquivo | Descrição | Uso |
|---------|-----------|-----|
| **unipulso.spec** | Configuração PyInstaller | Define como o .exe é criado |
| **build_exe.py** | Script de build do executável | `python build_exe.py` |
| **build_installer.py** | Script de build do instalador | `python build_installer.py` |
| **build_all.bat** | Build completo (1 clique) | `build_all.bat` |
| **installer.iss** | Script Inno Setup | Configuração do instalador Windows |
| **create_icon.py** | Gerador de ícone .ico | `python create_icon.py` |

### 📚 Documentação

| Arquivo | Conteúdo | Para quem |
|---------|----------|-----------|
| **GUIA_INSTALADOR.md** | Guia completo de build | Desenvolvedores |
| **README_INSTALADOR.md** | README para distribuição | Usuários finais |
| **GUIA_RAPIDO_1_PAGINA.md** | Guia de 1 página | Usuários finais |

### ⚙️ Configuração

| Arquivo | Modificação |
|---------|-------------|
| **requirements.txt** | Adicionado `pyinstaller>=6.0.0` |
| **.gitignore** | Adicionadas regras para build/ dist/ installer_output/ |

---

## 🚀 Fluxo de Uso

### Para Desenvolvedores

```mermaid
graph LR
    A[Código Python] --> B[build_exe.py]
    B --> C[dist/Unipulso.exe]
    C --> D[build_installer.py]
    D --> E[installer_output/Unipulso_Setup.exe]
```

**Comando único**:
```batch
build_all.bat
```

### Para Usuários Finais

```
1. Download Unipulso_Setup_v1.0.0.exe
2. Execute o instalador
3. Use o aplicativo (Menu Iniciar)
```

---

## 📂 Estrutura de Pastas Gerada

```
Unipulso/
│
├── 📄 Scripts de Build
│   ├── unipulso.spec          # Config PyInstaller
│   ├── build_exe.py           # Build executável
│   ├── build_installer.py     # Build instalador
│   ├── build_all.bat          # Build completo
│   ├── installer.iss          # Config Inno Setup
│   └── create_icon.py         # Criar ícone
│
├── 📚 Documentação
│   ├── GUIA_INSTALADOR.md     # Guia completo (devs)
│   ├── README_INSTALADOR.md   # README distribuição
│   └── GUIA_RAPIDO_1_PAGINA.md # Guia rápido (usuários)
│
├── 🔨 Build (gerado)
│   ├── build/                 # Arquivos temporários PyInstaller
│   └── dist/                  # Executável final
│       └── Unipulso.exe
│
└── 📦 Instalador (gerado)
    └── installer_output/
        └── Unipulso_Setup_v1.0.0.exe
```

---

## ✨ Recursos Implementados

### ✅ Sistema de Build

- [x] Configuração PyInstaller completa
- [x] Script automatizado de build
- [x] Coleta automática de dependências
- [x] Inclusão de recursos (logo, fontes)
- [x] Exclusão de módulos desnecessários
- [x] Suporte a ícone personalizado

### ✅ Instalador Windows

- [x] Script Inno Setup profissional
- [x] Atalhos (Desktop + Menu Iniciar)
- [x] Registro no Painel de Controle
- [x] Desinstalação completa
- [x] Compressão LZMA2/max
- [x] Interface em Português do Brasil
- [x] Mensagens personalizadas

### ✅ Automação

- [x] Script build_all.bat (1 clique)
- [x] Verificação de dependências
- [x] Limpeza automática de builds anteriores
- [x] Validação de saída
- [x] Mensagens coloridas no terminal
- [x] Tratamento de erros

### ✅ Documentação

- [x] Guia completo de build (30+ páginas)
- [x] README para distribuição
- [x] Guia rápido de 1 página
- [x] Este índice

---

## 🎯 Próximos Passos

### Antes do Primeiro Build

1. **Instalar PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **Baixar Inno Setup**
   - Download: https://jrsoftware.org/isdl.php
   - Instalar com configurações padrão

3. **Criar ícone (opcional)**
   ```bash
   python create_icon.py
   ```

### Fazer o Build

```batch
# Opção 1: Build completo (recomendado)
build_all.bat

# Opção 2: Passo a passo
python build_exe.py
python build_installer.py
```

### Distribuir

1. Testar `installer_output/Unipulso_Setup_v1.0.0.exe`
2. Upload para GitHub Releases
3. Compartilhar link com usuários

---

## 📊 Estatísticas

| Métrica | Valor |
|---------|-------|
| **Arquivos criados** | 9 |
| **Scripts Python** | 3 |
| **Scripts batch** | 1 |
| **Arquivos de config** | 2 |
| **Documentos** | 3 |
| **Linhas de código** | ~1200 |
| **Tempo de build** | ~3 min |
| **Tamanho do .exe** | ~50-80 MB |
| **Tamanho do instalador** | ~40-70 MB |

---

## 🔍 Referências Técnicas

### PyInstaller (unipulso.spec)

**Principais configurações**:
- `console=False`: Aplicação GUI (sem console)
- `onefile=True`: Executável único
- `icon='logo/icon.ico'`: Ícone customizado
- `hiddenimports`: Módulos não detectados automaticamente
- `datas`: Arquivos de recursos (logo, fontes, templates)
- `excludes`: Módulos desnecessários (reduz tamanho)

### Inno Setup (installer.iss)

**Principais seções**:
- `[Setup]`: Informações básicas do instalador
- `[Files]`: Arquivos a copiar
- `[Dirs]`: Diretórios a criar
- `[Icons]`: Atalhos
- `[Run]`: Executar após instalação
- `[Code]`: Scripts Pascal customizados

---

## 🐛 Troubleshooting

### Build falha com "Módulo não encontrado"

**Solução**: Adicionar ao `hiddenimports` em `unipulso.spec`

### Instalador não inclui recursos (logo, fontes)

**Solução**: Verificar seção `[Files]` em `installer.iss`

### Executável muito grande (>100 MB)

**Solução**: Adicionar mais módulos ao `excludes` em `unipulso.spec`

### Inno Setup não encontrado

**Solução**: Editar `build_installer.py` com caminho correto

---

## 📞 Suporte ao Desenvolvedor

Se precisar de ajuda com o sistema de build:

1. Consulte **GUIA_INSTALADOR.md** (documentação completa)
2. Verifique logs de build em `build/` e `dist/`
3. Teste executável diretamente: `dist/Unipulso.exe`

---

**Criado em**: 12/11/2025  
**Sistema**: Windows 10/11  
**Python**: 3.14.0  
**PyInstaller**: 6.0.0+  
**Inno Setup**: 6.x
