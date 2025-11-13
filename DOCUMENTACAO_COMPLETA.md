# 📚 Documentação Completa - Unipulso

> **Sistema de Geração de Pulseiras Hospitalares**

---

## 📖 Índice

1. [Início Rápido](#início-rápido)
2. [Guia de Uso](#guia-de-uso)
3. [Impressão Zebra ZD230](#impressão-zebra-zd230)
4. [Importação de CSV](#importação-de-csv)
5. [Arquitetura do Sistema](#arquitetura-do-sistema)
6. [Histórico de Melhorias](#histórico-de-melhorias)

---

## 🚀 Início Rápido

### Instalação

```bash
# 1. Clonar/baixar o projeto
cd Unipulso

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar aplicativo
python app.py
```

### Primeiro Uso

1. **Importar CSV**: Menu > Arquivo > Importar CSV
2. **Visualizar**: Navegar entre pulseiras na aba "Pré-visualização"
3. **Exportar**: Menu > Exportar > PNG ou PDF
4. **Imprimir**: Menu > Impressão > Imprimir (requer Zebra ZD230)

---

## 📋 Guia de Uso

### Interface Gráfica

A interface é dividida em:

#### **Barra de Menu**
- **📁 Arquivo**: Importar CSV, Baixar exemplos, Sair
- **💾 Exportar**: PNG e PDF
- **🖨️ Impressão**: Imprimir, Configurar impressora, Teste
- **🎨 Layout**: Editor, Configurar fonte, Modelos
- **⚙️ Configurações**: Upload de logotipo

#### **Sidebar Esquerda**
Mostra informações em tempo real:
- 📊 **CSV**: Quantidade de pacientes
- 🖼️ **Logotipo**: Status da logo
- 🔤 **Fonte**: Família e tamanho
- 🖨️ **Impressora**: Status de conexão

**Ações Rápidas:**
- 🏥 Novo Atendimento
- 📥 Importar CSV
- 🎨 Editor Layout
- 🖨️ Imprimir Atual

#### **Abas Principais**
1. **👁️ Pré-visualização**: Navegação entre pulseiras
2. **💾 Exportação**: Exportar PNG/PDF
3. **🖨️ Impressão**: Configuração e impressão Zebra

### Funcionalidades

#### **1. Novo Atendimento**
Formulário para cadastro individual de paciente:
- Campos: Nome, Carteirinha, Data nasc., Mãe, Convênio, Médico, Sexo, Data/Hora admissão, Observação
- Botões:
  - **Salvar**: Salva e fecha
  - **Salvar e Adicionar Outro**: Salva e limpa formulário
  - **Cancelar**: Fecha sem salvar

#### **2. Importação CSV**
Formato esperado (com cabeçalho):
```csv
Número da carteirinha,Nome do paciente,Data de nascimento,Nome da mãe,Convênio,Médico responsável,Sexo,Data de admissão,Hora de admissão,Observação
```

**Exemplos:**
- Menu > Arquivo > Baixar Exemplo CSV (com dados)
- Menu > Arquivo > Baixar Modelo CSV (vazio, só cabeçalho)

#### **3. Configuração de Fonte**
Menu > Layout > Configurar Fonte Global

- Família de fonte
- Tamanho base (campos gerais)
- Tamanho do nome (independente)
- Negrito/Itálico
- Auto-fit (ajuste automático)

#### **4. Editor de Layout**
Menu > Layout > Editor de Layout

- Arrastar e soltar elementos
- Propriedades: posição, tamanho, rotação, cor, alinhamento
- Salvar/Carregar modelos

---

## 🖨️ Impressão Zebra ZD230

### Configuração Inicial

#### 1. Instalar Driver Zebra
- Download: https://www.zebra.com/
- Instalar driver oficial
- Conectar impressora via USB

#### 2. Instalar Dependência Python
```bash
pip install pywin32
```

#### 3. Configurar no Aplicativo
- Menu > Impressão > Configurar Impressora
- Selecionar "Zebra ZD230" na lista
- Testar conexão

### Uso

#### **Imprimir Pulseira Atual**
- Menu > Impressão > Imprimir Pulseira Atual
- OU: Botão "🖨️ Imprimir Atual" na sidebar
- OU: Aba Impressão > Botão "Imprimir Pulseira Atual"

#### **Imprimir Todas as Pulseiras**
- Menu > Impressão > Imprimir Todas as Pulseiras
- OU: Aba Impressão > Botão "Imprimir Todas"
- Confirma quantidade e imprime em lote

#### **Teste de Impressão**
- Menu > Impressão > Teste de Impressão
- Imprime etiqueta de teste simples

### Especificações Técnicas

**Impressora:** Zebra ZD230  
**Protocolo:** ZPL (Zebra Programming Language)  
**Comunicação:** RAW via USB  
**DPI:** 203 (8 dots/mm)  
**Largura da etiqueta:** 11cm (880 dots)  
**Altura da etiqueta:** 2cm (160 dots)

**Layout da Pulseira:**
- QR Code (esquerda): Número da carteirinha
- Nome do paciente (topo, negrito, 24pt)
- Informações em colunas:
  - Carteirinha, Data nasc., Mãe
  - Convênio, Médico, Sexo
  - Data/Hora admissão
  - Observações

### Troubleshooting

**Problema:** Impressora não encontrada  
**Solução:** Verificar nome exato em "Dispositivos e Impressoras" do Windows

**Problema:** Não imprime  
**Solução:** Verificar se há papel/etiquetas e se impressora está online

**Problema:** Layout incorreto  
**Solução:** Ajustar largura da etiqueta nas configurações da impressora

---

## 📊 Importação de CSV

### Formato Esperado

**Colunas obrigatórias:**
1. Número da carteirinha
2. Nome do paciente
3. Data de nascimento
4. Nome da mãe
5. Convênio
6. Médico responsável
7. Sexo
8. Data de admissão
9. Hora de admissão
10. Observação

### Exemplo de CSV

```csv
Número da carteirinha,Nome do paciente,Data de nascimento,Nome da mãe,Convênio,Médico responsável,Sexo,Data de admissão,Hora de admissão,Observação
123456,João Silva,15/03/1985,Maria Silva,UNIMED,Dr. Carlos,Masculino,12/11/2025,14:30,Alergia a dipirona
789012,Ana Santos,22/07/1990,Rosa Santos,SUS,Dra. Fernanda,Feminino,12/11/2025,15:45,
```

### Dicas

- Use **UTF-8 com BOM** para evitar problemas com acentos
- Dados vazios são permitidos (deixar campo vazio após vírgula)
- Não incluir vírgulas dentro dos dados
- Formato de data: DD/MM/AAAA
- Formato de hora: HH:MM

---

## 🏗️ Arquitetura do Sistema

### Estrutura de Pastas

```
Unipulso/
├── app.py                 # Interface gráfica principal
├── core/                  # Núcleo do sistema
│   ├── config.py         # Configurações e constantes
│   ├── models.py         # Modelos de dados
│   ├── render.py         # Renderização de pulseiras
│   └── io_manager.py     # Importação/Exportação
├── ui/                    # Componentes de interface
│   ├── layout_editor.py  # Editor visual
│   └── atendimento_form.py # Formulário de atendimento
├── utils/                 # Utilitários
│   ├── helpers.py        # Funções auxiliares
│   └── zebra_printer.py  # Impressão Zebra
├── data/                  # Dados
├── output/                # Saídas (PNG, PDF)
├── templates/             # Modelos de layout
├── logo/                  # Logotipos
└── fonte padrao/          # Fontes do projeto
```

### Módulos Principais

#### **core/config.py**
- Constantes (dimensões, DPI, caminhos)
- Conversão cm ↔ pixels
- Configurações padrão

#### **core/models.py**
- `LayoutModel`: Modelo de layout
- `TextItem`: Elemento de texto
- `QRItem`: Elemento QR Code

#### **core/render.py**
- `create_pulseira_image()`: Renderiza pulseira padrão
- `render_layout_to_image()`: Renderiza layout customizado

#### **core/io_manager.py**
- `import_csv()`: Importa dados CSV
- `export_png()`: Exporta PNG
- `export_pdf()`: Exporta PDF

#### **ui/layout_editor.py**
- Editor visual drag & drop
- Propriedades de elementos
- Preview em tempo real

#### **ui/atendimento_form.py**
- Formulário de cadastro
- Validação de campos
- Salvamento em CSV

#### **utils/zebra_printer.py**
- `ZebraPrinter`: Classe de impressão
- `generate_bracelet_zpl()`: Converte para ZPL
- Detecção de impressoras

### Fluxo de Dados

```
CSV/Formulário → IOManager → LayoutModel → Render → Imagem/PDF/ZPL
                                ↓
                         Layout Editor (opcional)
```

---

## 📝 Histórico de Melhorias

### ✅ Melhorias Implementadas

#### **Interface Gráfica Redesenhada**
- Sistema de abas (Pré-visualização, Exportação, Impressão)
- Sidebar com informações em tempo real
- Navegação entre pacientes (◀ Anterior | Próximo ▶)
- Menu organizado por categorias
- Ações rápidas na sidebar

#### **Sistema de Impressão Zebra ZD230**
- Impressão direta via ZPL
- Detecção automática de impressoras
- Interface completa de configuração
- Teste de impressão
- Impressão em lote com progresso

#### **Formulário de Atendimento**
- Cadastro individual de pacientes
- Validação de campos
- Data/Hora automática
- Opção "Salvar e Adicionar Outro"
- Limpeza automática de dados anteriores

#### **Layout e Posicionamento**
- Área imprimível ajustada para 11cm
- Nome e observação centralizados
- Campos organizados em colunas
- QR Code isolado à esquerda
- Fonte do nome independente

#### **Correções de Bugs**
- Formulário fecha após salvar
- Dados anteriores limpos corretamente
- Todos os campos aparecem no PNG/PDF
- Importações corrigidas
- Compatibilidade com ttkbootstrap

### 🎯 Decisões de Design

#### **Área Imprimível**
- Largura: 11cm (definida em `core/config.py`)
- Margem não-imprimível: 2.5cm (esquerda)
- Logo renderizada na área não-imprimível

#### **Layout Padrão**
- QR Code: esquerda (0.1cm margem)
- Nome: centralizado, negrito, 32px
- Carteirinha: centralizado, 20px
- Campos: 3 colunas, 16px
- Observação: centralizada, rodapé, 14px

#### **Fontes**
- Padrão: Unimed Regular/Bold
- Carregamento automático da pasta "fonte padrao"
- Tamanho do nome independente (ajustável)
- Auto-fit opcional para campos

---

## 🔧 Configurações Avançadas

### Arquivo de Preferências

Local: `unipulso_prefs.json`

Contém:
- Última família de fonte usada
- Tamanho da fonte
- Flags de negrito/itálico
- Auto-fit habilitado/desabilitado

### Modelos de Layout

Salvos em: `templates/`

Formato JSON:
```json
{
  "width": 2362,
  "height": 236,
  "items": [
    {
      "type": "text",
      "id": "nome",
      "x": 500,
      "y": 10,
      "text": "{Nome do paciente}",
      "font_size": 32,
      "bold": true,
      "align": "center"
    }
  ]
}
```

### Personalização

#### **Alterar dimensões da pulseira**
Editar `core/config.py`:
```python
PULSEIRA_W_CM = 25.0  # Largura total
PULSEIRA_H_CM = 2.0   # Altura
PRINTABLE_WIDTH_CM = 11  # Largura imprimível
```

#### **Alterar layout ZPL**
Editar `utils/zebra_printer.py`:
```python
def generate_bracelet_zpl(patient_data):
    # Ajustar posições ^FO
    # Ajustar tamanhos de fonte ^A
```

---

## 📞 Suporte

Para problemas ou dúvidas:
1. Verificar este documento
2. Verificar logs do console
3. Testar com CSV de exemplo
4. Verificar configurações de impressora

---

## 📄 Licença

Este projeto é de uso interno hospitalar.

---

**Última atualização:** 12/11/2025
