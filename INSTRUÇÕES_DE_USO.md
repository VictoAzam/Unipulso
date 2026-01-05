# 📋 Instruções de Uso - Gerador de Pulseiras Hospitalares

## 📖 Índice
1. [Visão Geral](#visão-geral)
2. [Iniciando o Programa](#iniciando-o-programa)
3. [Interface Principal](#interface-principal)
4. [Importando Pacientes](#importando-pacientes)
5. [Adicionando Paciente Manualmente](#adicionando-paciente-manualmente)
6. [Gerenciando Pacientes](#gerenciando-pacientes)
7. [Configurando Logo](#configurando-logo)
8. [Gerando Pulseiras](#gerando-pulseiras)
9. [Exportando para PDF](#exportando-para-pdf)
10. [Imprimindo Pulseiras](#imprimindo-pulseiras)
11. [Solução de Problemas](#solução-de-problemas)

---

## 🎯 Visão Geral

O **Gerador de Pulseiras Hospitalares** é um sistema completo para criar, gerenciar e imprimir pulseiras de identificação para pacientes hospitalares. Cada pulseira contém:

- ✅ QR Code com ID do paciente
- ✅ Nome completo do paciente
- ✅ Observações especiais (campo OBS)
- ✅ Informações principais: Sexo, Data de Admissão, Hora
- ✅ Informações ao lado do QR: Data de Nascimento, Nome da Mãe, Convênio
- ✅ Rodapé: Médico Responsável + Data/Hora de geração
- ✅ Logo personalizado (opcional)

**Dimensões da Pulseira:** 29,5 cm × 2 cm (área imprimível: 10 cm)

---

## 🚀 Iniciando o Programa

### No Linux (ambiente de desenvolvimento):
```bash
cd "/home/vprimo/Área de trabalho/Unipulso"
source .venv/bin/activate
python app.py
```

### No Windows (após compilar o .exe):
1. Localize o arquivo `GeradorPulseiras.exe` na pasta `dist/`
2. Dê um duplo clique no arquivo
3. O programa abrirá automaticamente

---

## 🖥️ Interface Principal

A interface é dividida em 4 seções principais:

### 1. **Barra Superior - Importação e Logo**
- **Botão "Upload Logotipo"**: Importa uma imagem de logo institucional
  - Após selecionar a imagem, você pode salvá-la como logo padrão
  - Logo padrão é carregado automaticamente nas próximas sessões
- **Botão "Remover Logo"**: Remove o logo atual da sessão
  - Se houver logo padrão configurado, oferece opção de removê-lo também
- **Botão "Baixar Modelo CSV"**: Baixa arquivo de exemplo para preenchimento
- **Botão "Baixar CSV Vazio"**: Baixa modelo em branco
- **Botão "Importar CSV"**: Importa múltiplos pacientes de um arquivo

### 2. **Formulário de Cadastro - Adicionar Paciente Individual**
Campos obrigatórios:
- Nome completo
- Sexo (M/F)
- Data de Admissão (DD/MM/AAAA)
- Hora (HH:MM)

Campos opcionais:
- Data de Nascimento
- Nome da Mãe
- Convênio
- Médico Responsável
- **OBS (Observações)**: Campo especial em vermelho para alertas importantes

### 3. **Lista de Pacientes**
- Mostra todos os pacientes cadastrados
- Exibe: ID, Nome, Sexo, Admissão
- Permite seleção múltipla (Ctrl+Click ou Shift+Click)

### 4. **Ações - Botões de Controle**
- **Gerar Pulseiras**: Gera arquivos PNG das pulseiras selecionadas
- **Exportar para PDF**: Cria PDF com múltiplas pulseiras
- **Exportar PDF A4**: Cria PDF em formato A4 paisagem
- **Imprimir**: Envia para impressora
- **Remover Selecionados**: Exclui pacientes da lista
- **Limpar Todos**: Remove todos os pacientes

---

## 📥 Importando Pacientes

### Passo 1: Preparar o arquivo CSV

#### Opção A - Usar o modelo fornecido:
1. Clique em **"Baixar Modelo CSV"** para ver um exemplo preenchido
2. OU clique em **"Baixar CSV Vazio"** para começar do zero

#### Opção B - Criar manualmente:
Crie um arquivo `.csv` com as seguintes colunas **obrigatórias**:

```csv
Nome,Sexo,Data de Admissão,Hora,Data de Nascimento,Nome da Mãe,Convênio,Médico,OBS
```

**Exemplo de linha:**
```csv
João Silva Santos,M,15/10/2025,14:30,12/03/1985,Maria Silva,Unimed,Dr. Carlos Oliveira,Alergia a dipirona
```

### Passo 2: Formato dos Dados

| Campo | Formato | Exemplo | Obrigatório |
|-------|---------|---------|-------------|
| Nome | Texto livre | João Silva Santos | ✅ Sim |
| Sexo | M ou F | M | ✅ Sim |
| Data de Admissão | DD/MM/AAAA | 15/10/2025 | ✅ Sim |
| Hora | HH:MM | 14:30 | ✅ Sim |
| Data de Nascimento | DD/MM/AAAA | 12/03/1985 | ❌ Não |
| Nome da Mãe | Texto livre | Maria Silva | ❌ Não |
| Convênio | Texto livre | Unimed | ❌ Não |
| Médico | Texto livre | Dr. Carlos Oliveira | ❌ Não |
| OBS | Texto livre | Alergia a dipirona | ❌ Não |

⚠️ **Importante:**
- Use sempre vírgula (,) como separador
- Datas devem estar no formato DD/MM/AAAA
- Hora deve estar no formato HH:MM (24 horas)
- Sexo aceita apenas: M, F, Masculino, Feminino
- Campo OBS aparece em **vermelho** na pulseira

### Passo 3: Importar
1. Clique no botão **"Importar CSV"**
2. Selecione o arquivo `.csv` preparado
3. O sistema validará os dados automaticamente
4. Pacientes válidos serão adicionados à lista
5. Erros serão exibidos em mensagens de alerta

---

## ➕ Adicionando Paciente Manualmente

### Passo a passo:

1. **Preencha os campos obrigatórios:**
   - Nome completo do paciente
   - Sexo (selecione M ou F no dropdown)
   - Data de Admissão (clique no calendário ou digite DD/MM/AAAA)
   - Hora da admissão (formato HH:MM)

2. **Preencha os campos opcionais** (se necessário):
   - Data de Nascimento
   - Nome da Mãe
   - Convênio
   - Médico Responsável
   - **OBS**: Use para alertas importantes (ex: "Alergia a penicilina", "Diabético", etc.)

3. **Clique em "Adicionar Paciente"**

4. O paciente aparecerá na lista com um ID único gerado automaticamente

### 💡 Dicas:
- IDs são gerados no formato: `PAC-YYYYMMDD-NNNN` (ex: PAC-20251015-0001)
- Campos com * são obrigatórios
- O campo OBS é destacado em **vermelho** na pulseira para chamar atenção

---

## 📝 Gerenciando Pacientes

### Visualizar Lista
- Todos os pacientes aparecem na tabela central
- Rolagem automática se houver muitos registros

### Selecionar Pacientes
- **Clique simples**: Seleciona um paciente
- **Ctrl + Clique**: Seleciona múltiplos pacientes individuais
- **Shift + Clique**: Seleciona intervalo de pacientes

### Remover Pacientes
1. Selecione os pacientes desejados na lista
2. Clique em **"Remover Selecionados"**
3. Confirme a ação

### Limpar Tudo
- Clique em **"Limpar Todos"** para remover toda a lista
- ⚠️ Esta ação não pode ser desfeita!

---

## 🎨 Configurando Logo

### Adicionar Logo:
1. Clique em **"Upload Logotipo"**
2. Selecione uma imagem (formatos aceitos: PNG, JPG, JPEG, GIF, BMP)
3. Uma janela de confirmação aparecerá com o nome do arquivo selecionado
4. **Opcional**: Marque a opção **"☑ Salvar como logo padrão"** se desejar que o logo seja carregado automaticamente toda vez que o programa iniciar
5. Clique em **"✓ Confirmar"** para aplicar o logo
6. O logo aparecerá no canto superior esquerdo de todas as pulseiras

### Recomendações:
- ✅ Use imagens com fundo transparente (PNG)
- ✅ Proporção ideal: quadrada ou horizontal
- ✅ Resolução mínima: 200x200 pixels
- ✅ Tamanho máximo recomendado: 2 MB
- ⚠️ O logo será redimensionado automaticamente para 1,5cm de altura

### Logo Padrão (Novo!):
- ✅ Salve um logo como padrão para não precisar carregar toda vez
- ✅ O logo padrão é carregado automaticamente quando o programa inicia
- ✅ O caminho do logo é salvo nas suas preferências
- ⚠️ Se mover ou deletar o arquivo de imagem, o logo padrão não será carregado

### Remover Logo:
1. Clique em **"Remover Logo"** para remover o logo atual
2. Se você tiver um logo padrão configurado, uma janela perguntará se deseja remover também o logo padrão
3. **Opções:**
   - **☑ Remover também o logo padrão** (marcado por padrão) - Remove completamente, não carregará na próxima vez
   - **☐ Remover também o logo padrão** (desmarcado) - Remove apenas desta sessão, voltará na próxima inicialização
4. Clique em **"🗑 Remover"** para confirmar

---

## 🖨️ Gerando Pulseiras

### Gerar Arquivos PNG (imagens individuais):

1. **Selecione os pacientes** na lista (ou deixe todos selecionados)
2. Clique em **"Gerar Pulseiras"**
3. Escolha a pasta de destino
4. O sistema criará um arquivo PNG para cada paciente

**Formato dos arquivos:**
- Nome: `Pulseira_[Nome do Paciente]_[ID].png`
- Exemplo: `Pulseira_João Silva Santos_PAC-20251015-0001.png`
- Resolução: 300 DPI (alta qualidade para impressão)
- Dimensões: 3484 × 236 pixels (29,5 cm × 2 cm)

### Características das Pulseiras Geradas:

#### Layout:
```
┌─────────────────────────────────────────────────────────────────────┐
│ [LOGO]  NOME DO PACIENTE                                           │
│         OBS: Observações em vermelho (se houver)                    │
│                                                                      │
│ ┌────┐  │ Sexo:        M          │ Data Nasc:   12/03/1985   │
│ │ QR │  │ Admissão:    15/10/2025 │ Nome da Mãe: Maria Silva  │
│ │CODE│  │ Hora:        14:30      │ Convênio:    Unimed       │
│ └────┘  │                         │                            │
│                                                                      │
│                          Médico: Dr. Carlos  │ 15/10/2025 14:30    │
└─────────────────────────────────────────────────────────────────────┘
```

#### Detalhes técnicos:
- **QR Code**: Contém o ID único do paciente
- **OBS**: Em vermelho (RGB: 180, 0, 0), fonte 15% menor
- **Colunas principais**: Sexo, Admissão, Hora
- **Ao lado do QR**: Data de Nascimento, Nome da Mãe, Convênio
- **Rodapé azul**: Médico + Data/Hora de geração (RGB: 10, 30, 120)

---

## 📄 Exportando para PDF

### PDF Padrão (múltiplas pulseiras):

1. Selecione os pacientes desejados
2. Clique em **"Exportar para PDF"**
3. Escolha o nome e local do arquivo
4. O PDF conterá todas as pulseiras selecionadas, uma por página

**Formato:**
- Cada pulseira em uma página individual
- Dimensões originais preservadas (29,5 cm × 2 cm)
- Resolução de impressão: 300 DPI

### PDF A4 Paisagem:

1. Selecione os pacientes
2. Clique em **"Exportar PDF A4"**
3. Salve o arquivo

**Formato:**
- Layout: A4 paisagem (297 mm × 210 mm)
- **Múltiplas pulseiras por página** (até 10 por folha)
- Espaçamento otimizado para corte
- Ideal para impressão em lote

---

## 🖨️ Imprimindo Pulseiras

### Windows:
1. Selecione os pacientes na lista
2. Clique em **"Imprimir"**
3. Uma janela de seleção de impressora abrirá
4. Escolha a impressora de etiquetas
5. Configure as propriedades (se necessário):
   - Tamanho do papel: Personalizado (29,5 cm × 2 cm)
   - Orientação: Paisagem
   - Qualidade: Máxima
6. Confirme a impressão

### Linux:
1. Certifique-se de que o CUPS está instalado e configurado
2. Configure uma impressora com `lpstat -p`
3. Use o botão **"Imprimir"** no programa
4. ⚠️ Se houver erro, o arquivo PNG será aberto automaticamente
5. Imprima manualmente através do visualizador de imagens

### Configurações Recomendadas da Impressora:
- **Tipo de papel**: Etiqueta/Pulseira
- **Tamanho**: Personalizado 29,5 cm × 2 cm
- **Margem**: 0 mm (sem margens)
- **Resolução**: Máxima disponível (mínimo 300 DPI)
- **Modo de cor**: Colorido
- **Qualidade**: Alta/Fotográfica

---

## 🔧 Solução de Problemas

### ❌ Erro ao importar CSV

**Problema:** "Erro ao processar linha X"

**Soluções:**
- Verifique o formato das datas (DD/MM/AAAA)
- Verifique o formato da hora (HH:MM)
- Certifique-se que o campo Sexo contém apenas M ou F
- Verifique se há vírgulas extras dentro dos dados
- Use aspas duplas para textos com vírgulas: `"Silva, João"`

### ❌ Campos obrigatórios faltando

**Problema:** "Os seguintes campos são obrigatórios: Nome, Sexo..."

**Solução:**
- Preencha TODOS os campos marcados com * (asterisco)
- Nome não pode estar vazio
- Sexo deve ser selecionado (M ou F)
- Data e hora devem estar no formato correto

### ❌ Logo não aparece

**Problema:** Logo não é exibido nas pulseiras

**Soluções:**
- Verifique se o arquivo de imagem não está corrompido
- Tente usar formato PNG com fundo transparente
- Reduza o tamanho do arquivo (máx. 5 MB)
- Clique em "Remover Logo" e carregue novamente

### ❌ QR Code não é lido

**Problema:** Scanner não reconhece o QR Code

**Soluções:**
- Certifique-se de imprimir em alta resolução (300 DPI)
- Use impressora de qualidade fotográfica
- Evite impressoras térmicas de baixa resolução
- Teste o QR Code com aplicativo de celular antes de imprimir

### ❌ Texto cortado ou sobreposto

**Problema:** Informações não aparecem completas

**Soluções:**
- Este problema foi corrigido no sistema atual
- Se persistir, reporte com screenshot
- Nomes muito longos (>50 caracteres) podem precisar abreviação

### ❌ Erro ao imprimir no Linux

**Problema:** "Command 'lpr' returned non-zero exit status 1"

**Soluções:**
1. Instale CUPS: `sudo dnf install cups` (Fedora) ou `sudo apt install cups` (Ubuntu)
2. Verifique impressoras: `lpstat -p`
3. Configure impressora padrão: `lpoptions -d NomeDaImpressora`
4. **Alternativa**: O arquivo PNG será aberto automaticamente - imprima manualmente

### ❌ Erro ao gerar PDF

**Problema:** "Erro ao exportar para PDF"

**Soluções:**
- Verifique permissões de escrita na pasta de destino
- Certifique-se de ter espaço em disco
- Feche o PDF se ele já estiver aberto em outro programa
- Tente salvar em outra pasta (ex: Documentos)

### 🆘 Precisa de mais ajuda?

**Logs de erro:**
- Erros detalhados aparecem no console/terminal
- No Windows: execute via terminal para ver logs
- No Linux: erros aparecem automaticamente no terminal

**Informações úteis para suporte:**
- Sistema operacional (Windows/Linux/macOS)
- Versão do Python (se aplicável)
- Mensagem de erro completa
- Arquivo CSV problemático (se aplicável)

---

## 📚 Recursos Adicionais

### Arquivos de Exemplo:
- `exemplo.csv` - CSV com dados de exemplo
- `modelo_vazio.csv` - Modelo em branco para preenchimento

### Documentação Técnica:
- `BUILD_README.md` - Instruções para compilar o executável
- `requeriments.txt` - Lista de dependências Python

### Requisitos do Sistema:
- **Windows**: 7, 8, 10, 11 (64-bit)
- **Linux**: Qualquer distribuição moderna
- **Memória RAM**: Mínimo 2 GB
- **Espaço em disco**: 100 MB + espaço para pulseiras geradas
- **Impressora**: Compatível com etiquetas/pulseiras

---

## 📞 Contato e Suporte

Para dúvidas, sugestões ou problemas:
- 📧 Entre em contato com o administrador do sistema
- 🐛 Reporte bugs com descrição detalhada e screenshots
- 💡 Sugestões de melhorias são bem-vindas!

---

## 📝 Changelog

### Versão Atual (Outubro 2025)
- ✅ Sistema de containers para evitar sobreposições
- ✅ Campo OBS em vermelho para alertas
- ✅ Suporte a CSV com 9 colunas (incluindo OBS)
- ✅ Reorganização do layout (campos ao lado do QR)
- ✅ Rodapé com médico + data/hora em azul
- ✅ Tratamento de erros de impressão aprimorado
- ✅ Suporte multiplataforma (Windows/Linux/macOS)
- ✅ **NOVO: Sistema de logo padrão**
  - Salvar logo para carregar automaticamente
  - Gerenciamento inteligente de logo padrão
  - Interface melhorada com diálogos informativos
  - Confirmação com botões "✓ Confirmar" e "✗ Cancelar"
  - Opção de remover logo mantendo ou excluindo o padrão

---

**© 2025 - Gerador de Pulseiras Hospitalares**  
*Desenvolvido para facilitar a identificação segura de pacientes*

