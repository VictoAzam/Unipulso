# 📚 Índice Central de Documentação - Unipulso

> **Sistema completo para geração e impressão de pulseiras hospitalares**

---

## 🎯 Navegação Rápida

| Documento | Descrição | Audiência |
|-----------|-----------|-----------|
| [**Documentação Técnica Completa**](DOCUMENTACAO_TECNICA_COMPLETA.md) | Visão geral completa do sistema | Desenvolvedores |
| [**Guia de Início Rápido**](GUIA_RAPIDO_1_PAGINA.md) | Como usar o sistema em 5 minutos | Usuários Finais |
| [**Guia de CSV**](GUIA_CSV.md) | Como preparar arquivos CSV | Usuários Finais |
| [**Instruções de Uso**](INSTRUÇÕES_DE_USO.md) | Manual completo do usuário | Usuários Finais |

---

## 📖 Documentação por Módulo

### 🔧 Core (Núcleo do Sistema)

📄 [**Documentação do Módulo Core**](docs/CORE_MODULE.md)

**Conteúdo**:
- ⚙️ `config.py` - Configurações globais
- 📊 `models.py` - Modelos de dados (TextItem, QRItem, LayoutModel)
- 🎨 `render.py` - Motor de renderização
- 💾 `io_manager.py` - Importação/Exportação (CSV, PNG, PDF)

**Quando usar**:
- Modificar configurações de impressão
- Criar novos tipos de elementos
- Alterar lógica de renderização
- Adicionar novos formatos de exportação

---

### 🖥️ UI (Interface do Usuário)

📄 [**Documentação do Módulo UI**](docs/UI_MODULE.md)

**Conteúdo**:
- 📑 `tabs.py` - Gerenciamento de abas
- 📊 `sidebar.py` - Painel lateral de status
- 🎬 `preview.py` - Preview e carrossel
- ✏️ `layout_editor.py` - Editor WYSIWYG
- 📋 `menu_manager.py` - Menu e atalhos
- 📝 `atendimento_form.py` - Formulário de cadastro

**Quando usar**:
- Adicionar novas abas
- Customizar interface
- Criar novos formulários
- Modificar atalhos de teclado

---

### 🛠️ Utils (Utilitários)

📄 [**Documentação do Módulo Utils**](docs/UTILS_MODULE.md)

**Conteúdo**:
- 🔧 `helpers.py` - Funções auxiliares (fontes, QR codes, text wrapping)
- 🖨️ `zebra_printer.py` - Impressão em impressoras Zebra

**Quando usar**:
- Adicionar novas fontes
- Gerar QR codes customizados
- Configurar impressoras
- Criar utilitários reutilizáveis

---

## 🏗️ Documentação de Arquitetura

### Visão Geral do Sistema

📄 [**Architecture**](ARCHITECTURE.md)

**Tópicos**:
- Estrutura de diretórios
- Fluxo de dados
- Diagrama de componentes
- Decisões de design

---

### Build e Deployment

| Documento | Descrição |
|-----------|-----------|
| [**Build Instructions**](BUILD_INSTRUCTIONS.md) | Como compilar o executável |
| [**Build System Index**](BUILD_SYSTEM_INDEX.md) | Índice do sistema de build |
| [**Instalador Completo**](INSTALADOR_COMPLETO.md) | Como criar instalador |
| [**Guia do Instalador**](GUIA_INSTALADOR.md) | Como usar o instalador |

---

## 📚 Documentação de Funcionalidades

### Importação e Exportação

| Documento | Descrição |
|-----------|-----------|
| [**Guia CSV**](GUIA_CSV.md) | Formato e preparação de CSV |
| [**Impressão Zebra**](IMPRESSAO_ZEBRA_README.md) | Como imprimir em Zebra ZD230 |

---

### Interface e UX

| Documento | Descrição |
|-----------|-----------|
| [**UX Improvements**](docs/UX_IMPROVEMENTS.md) | Melhorias de interface |
| [**Carousel Visualization**](docs/CAROUSEL_VISUALIZATION.md) | Carrossel de pacientes |
| [**Atendimento Form**](docs/ATENDIMENTO_FORM.md) | Formulário de cadastro |

---

## 🎓 Tutoriais e Exemplos

### Para Usuários

1. **[Guia Rápido (1 Página)](GUIA_RAPIDO_1_PAGINA.md)** ⭐
   - Importar CSV
   - Gerar pulseiras
   - Exportar PNG/PDF

2. **[Instruções de Uso Completas](INSTRUÇÕES_DE_USO.md)**
   - Todas as funcionalidades
   - Passo a passo detalhado

3. **[Guia de CSV](GUIA_CSV.md)**
   - Formato correto
   - Colunas obrigatórias
   - Exemplos práticos

---

### Para Desenvolvedores

1. **[Quickstart](docs/QUICKSTART.md)**
   - Setup do ambiente
   - Executar pela primeira vez
   - Estrutura básica

2. **[Modular Guide](docs/MODULAR_GUIDE.md)**
   - Criar novos módulos
   - Integrar componentes
   - Boas práticas

3. **[Refactoring Guide](docs/README_REFACTORING.md)**
   - Como refatorar código
   - Padrões estabelecidos
   - Checklist de qualidade

---

## 🔍 Busca Rápida por Tópico

### Configurações

- **DPI e Dimensões**: [config.py](docs/CORE_MODULE.md#configpy---configurações-globais)
- **Fontes**: [helpers.py](docs/UTILS_MODULE.md#função-list_system_fonts)
- **Área Imprimível**: [config.py](docs/CORE_MODULE.md#dimensões-em-pixels-calculadas)

### Renderização

- **Criar Pulseira**: [render.py](docs/CORE_MODULE.md#função-principal-create_pulseira_image)
- **Layout Customizado**: [render.py](docs/CORE_MODULE.md#função-render_layout_to_image)
- **Ajuste de Fonte**: [render.py](docs/CORE_MODULE.md#ajuste-automático-de-fonte)

### Importação/Exportação

- **Importar CSV**: [io_manager.py](docs/CORE_MODULE.md#método-import_csv)
- **Exportar PNG**: [io_manager.py](docs/CORE_MODULE.md#método-export_png)
- **Exportar PDF**: [io_manager.py](docs/CORE_MODULE.md#método-export_pdf)

### Interface

- **Abas**: [tabs.py](docs/UI_MODULE.md#tabspy---gerenciamento-de-abas)
- **Preview**: [preview.py](docs/UI_MODULE.md#previewpy---preview-e-carrossel)
- **Editor**: [layout_editor.py](docs/UI_MODULE.md#layout_editorpy---editor-wysiwyg)
- **Formulário**: [atendimento_form.py](docs/UI_MODULE.md#atendimento_formpy---formulário-de-cadastro)

### Impressão

- **Zebra ZD230**: [zebra_printer.py](docs/UTILS_MODULE.md#zebra_printerpy---impressão-zebra)
- **Comandos ZPL**: [zebra_printer.py](docs/UTILS_MODULE.md#comandos-zpl-básicos)
- **Calibração**: [zebra_printer.py](docs/UTILS_MODULE.md#método-calibrate)

---

## 🎨 Diagramas e Visualizações

### Fluxo de Dados

```
CSV Import → Patient Data → Render Engine → Image → Export (PNG/PDF/Print)
              ↓                   ↓           ↓
           Validation         Layout     Preview
                              ↓
                          Editor
```

### Arquitetura de Camadas

```
┌─────────────────────────────────┐
│      UI Layer (ttkbootstrap)    │
│  tabs | sidebar | preview | ... │
├─────────────────────────────────┤
│      Business Logic (Core)      │
│  render | models | config | io  │
├─────────────────────────────────┤
│      Utilities (Utils)          │
│   helpers | zebra_printer       │
└─────────────────────────────────┘
```

---

## 📊 Matriz de Funcionalidades

| Funcionalidade | Módulo | Documentação |
|----------------|--------|--------------|
| Importar CSV | `io_manager.py` | [Core Module](docs/CORE_MODULE.md#método-import_csv) |
| Exportar PNG | `io_manager.py` | [Core Module](docs/CORE_MODULE.md#método-export_png) |
| Exportar PDF | `io_manager.py` | [Core Module](docs/CORE_MODULE.md#método-export_pdf) |
| Gerar QR Code | `helpers.py` | [Utils Module](docs/UTILS_MODULE.md#função-generate_qr_image) |
| Renderizar Pulseira | `render.py` | [Core Module](docs/CORE_MODULE.md#função-principal-create_pulseira_image) |
| Preview Carrossel | `preview.py` | [UI Module](docs/UI_MODULE.md#previewpy---preview-e-carrossel) |
| Editor de Layout | `layout_editor.py` | [UI Module](docs/UI_MODULE.md#layout_editorpy---editor-wysiwyg) |
| Formulário Cadastro | `atendimento_form.py` | [UI Module](docs/UI_MODULE.md#atendimento_formpy---formulário-de-cadastro) |
| Impressão Zebra | `zebra_printer.py` | [Utils Module](docs/UTILS_MODULE.md#zebra_printerpy---impressão-zebra) |

---

## 🆘 Troubleshooting

### Problemas Comuns

| Problema | Solução | Documento |
|----------|---------|-----------|
| CSV não importa | Verificar delimitador e encoding | [Guia CSV](GUIA_CSV.md) |
| Fontes não carregam | Verificar pasta `fonte padrao/` | [Utils Module](docs/UTILS_MODULE.md#problema-fontes-não-carregam) |
| Impressora não encontrada | Listar impressoras disponíveis | [Utils Module](docs/UTILS_MODULE.md#problema-impressora-zebra-não-encontrada) |
| QR Code não escaneia | Aumentar versão e correção | [Utils Module](docs/UTILS_MODULE.md#problema-qr-code-não-escaneia) |
| Texto cortado | Ajustar wrapping e tamanho | [Utils Module](docs/UTILS_MODULE.md#problema-texto-não-quebra-corretamente) |

---

## 📦 Documentos de Release

| Documento | Versão | Data |
|-----------|--------|------|
| [Release Notes v1.0.0](RELEASE_NOTES_v1.0.0.md) | 1.0.0 | Jan 2026 |
| [Resumo Executivo](RESUMO_EXECUTIVO.txt) | - | - |
| [Solução Final](SOLUCAO_FINAL.txt) | - | - |

---

## 🗂️ Documentos Arquivados

Documentos antigos ou obsoletos estão em `docs_archive/`:

- Correções antigas
- Versões anteriores de guias
- Documentação de funcionalidades removidas

---

## 🔄 Histórico de Atualizações

| Data | Versão Doc | Alterações |
|------|------------|------------|
| Jan 2026 | 1.0.0 | Documentação inicial completa |
| | | - Documentação técnica completa |
| | | - Módulos Core, UI, Utils |
| | | - Guias de usuário |
| | | - Índice centralizado |

---

## 📞 Suporte e Contato

### Para Usuários

- **Dúvidas de Uso**: Consulte [Instruções de Uso](INSTRUÇÕES_DE_USO.md)
- **Problemas com CSV**: Veja [Guia CSV](GUIA_CSV.md)
- **Guia Rápido**: [1 Página](GUIA_RAPIDO_1_PAGINA.md)

### Para Desenvolvedores

- **Documentação Técnica**: [Completa](DOCUMENTACAO_TECNICA_COMPLETA.md)
- **Arquitetura**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Build**: [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)

---

## 📝 Como Contribuir com a Documentação

1. **Identificar lacuna**: O que está faltando?
2. **Escolher documento**: Qual arquivo modificar?
3. **Seguir padrão**: Manter formatação Markdown
4. **Adicionar exemplos**: Código + explicação
5. **Atualizar índice**: Manter este arquivo atualizado

### Padrões de Documentação

- **Títulos**: Usar emojis para categorias
- **Código**: Usar code blocks com sintaxe
- **Exemplos**: Incluir input e output esperado
- **Links**: Sempre relativos ao repositório
- **Tabelas**: Para comparações e listas

---

## 🎯 Roadmap da Documentação

### ✅ Completo

- [x] Documentação técnica completa
- [x] Módulos Core, UI, Utils
- [x] Guias de usuário
- [x] Índice centralizado

### 🚧 Em Progresso

- [ ] Vídeos tutoriais
- [ ] Diagramas interativos
- [ ] API Reference automatizada

### 📋 Planejado

- [ ] Documentação em outros idiomas
- [ ] FAQ expandido
- [ ] Cookbook com receitas prontas
- [ ] Testes documentados

---

## 📄 Licença

Ver arquivo [LICENSE](LICENSE) no diretório raiz do projeto.

---

## 🎉 Conclusão

Este índice serve como ponto de partida para toda a documentação do **Unipulso**. Use os links acima para navegar para documentação específica de cada componente.

**Principais Documentos**:
- 📘 [Documentação Técnica Completa](DOCUMENTACAO_TECNICA_COMPLETA.md) - Start here!
- 🚀 [Guia Rápido](GUIA_RAPIDO_1_PAGINA.md) - Para usuários
- 🏗️ [Architecture](ARCHITECTURE.md) - Para desenvolvedores

---

**Versão**: 1.0.0  
**Última Atualização**: Janeiro 2026  
**Mantido por**: Equipe Unipulso
