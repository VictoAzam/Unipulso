# 📖 GUIA DE USO - APLICAÇÃO UNIPULSO

## 🚀 Como Iniciar a Aplicação

### Passo 1: Abrir o Terminal
```powershell
# Navegue até a pasta do projeto
cd "c:\Users\Victor Hugo Azambuja\Desktop\Unipulso-3-\Unipulso"
```

### Passo 2: Executar a Aplicação
```powershell
python app.py
```

**Resultado esperado**: Uma janela gráfica com a interface Unipulso será aberta.

---

## 🎯 Funcionalidades Principais

### 1️⃣ **INICIAR ATENDIMENTO** (Nova Paciente)

Este é o botão **MAIS IMPORTANTE** para você!

**Passos:**
1. Clique no botão verde **🏥 Iniciar Atendimento**
2. Uma janela de formulário abrirá
3. Preencha todos os campos obrigatórios (marcados com *):
   - ✅ **Número da carteirinha** (exemplo: 12345678)
   - ✅ **Nome do paciente** (exemplo: João Silva)
   - ✅ **Data de nascimento** (formato: DD/MM/AAAA, exemplo: 15/03/1985)
   - ✅ **Nome da mãe** (exemplo: Maria Silva)
   - ✅ **Convênio** (exemplo: Unimed)
   - ✅ **Médico responsável** (exemplo: Dr. Carlos)
   - ✅ **Sexo** (selecionar: Masculino/Feminino/Outro)
   - ✅ **Data de admissão** (será **preenchida automaticamente** com a data de hoje)
   - ✅ **Hora de admissão** (será **preenchida automaticamente** com a hora atual)
   - ❓ **Observação** (opcional - exemplo: Alergia a penicilina)

4. Clique em **💾 Salvar**
5. A pulseira será criada e salva automaticamente

**Resultado**: 
- ✅ Formulário fecha
- ✅ Dados salvos em `data/pacientes.csv`
- ✅ Pronto para exportar como PNG/PDF

---

### 2️⃣ **VISUALIZAR PULSEIRA**

Após preencher o formulário, você verá uma **prévia da pulseira** na área de visualização.

**O que você verá:**
```
┌─────────────────────────────────────────────────────────────┐
│ [QR CODE]  João Silva (Nome)                               │
│            Carteirinha: 12345678                             │
│                                                              │
│            Nasc: 15/03 │ Med: Dr. C... │ Hora: 14:30        │
│            Mãe: Maria  │ Sex: Masc     │                    │
│            Conv: Unimed│ Adm: 11/11    │                    │
│                                                              │
│            Observação: Alergia a penicilina                │
└─────────────────────────────────────────────────────────────┘
```

---

### 3️⃣ **EXPORTAR COMO PNG**

Para imprimir a pulseira como imagem:

1. Clique em **⬇️ Exportar PNG**
2. Escolha a pasta onde salvar (recomendado: `Desktop`)
3. A pulseira será salva como `pulseira_1.png`

**Resultado**: Arquivo PNG em alta qualidade (300 DPI) pronto para imprimir

---

### 4️⃣ **EXPORTAR COMO PDF**

Para gerar um documento PDF com múltiplas pulseiras:

1. Clique em **⬇️ Exportar PDF**
2. Escolha a pasta onde salvar
3. Selecione se deseja:
   - **Uma página por pulseira** (espaçadas)
   - **Todas em um documento** (compactadas)

**Resultado**: Arquivo PDF pronto para imprimir em impressora térmica

---

### 5️⃣ **IMPORTAR DO CSV** (Avançado)

Se você tiver um arquivo CSV com múltiplas pacientes:

1. Clique em **📥 Importar CSV**
2. Selecione o arquivo `.csv`
3. As pulseiras serão carregadas automaticamente

**Formato esperado do CSV:**
```
Número da carteirinha,Nome do paciente,Data de nascimento,Nome da mãe,Convênio,Médico responsável,Sexo,Data de admissão,Hora de admissão,Observação
12345678,João Silva,15/03/1985,Maria Silva,Unimed,Dr. Carlos,Masculino,11/11/2025,14:30,Alergia a penicilina
```

---

## 📋 Workflow Típico de Uso

### Cenário: Adicionar uma nova paciente

```
1. Clique em "🏥 Iniciar Atendimento"
   ↓
2. Preencha o formulário:
   - Carteirinha: 87654321
   - Nome: Roberta Silva
   - Data nasc: 20/05/1990
   - Mãe: Ana Silva
   - Convênio: Sul América
   - Médico: Dra. Paula
   - Sexo: Feminino
   - Data adm: (automático 11/11/2025)
   - Hora adm: (automático 14:35)
   - Observação: Gestante
   ↓
3. Clique em "💾 Salvar"
   ↓
4. Veja a pulseira na tela
   ↓
5. Clique em "⬇️ Exportar PNG"
   ↓
6. Salve a imagem
   ↓
7. Abra em um programa de impressão
   ↓
8. Imprima na impressora térmica
```

---

## 💡 Dicas Úteis

### ✅ Data e Hora Automáticas
- **Data de admissão** é preenchida automaticamente com a data atual
- **Hora de admissão** é preenchida automaticamente com a hora atual
- Você ainda pode editar se necessário

### ✅ Placeholders (Modelos)
Alguns campos têm placeholders (texto de exemplo):
- Data: `DD/MM/AAAA`
- Hora: `HH:MM`
- Estes desaparecem ao digitar

### ✅ Validação
O sistema valida:
- ✓ Campos obrigatórios preenchidos
- ✓ Data no formato correto (DD/MM/AAAA)
- ✓ Hora no formato correto (HH:MM)

Se houver erro, uma mensagem aparecerá pedindo correção.

### ✅ Limpeza de Campos
Clique em **🔄 Limpar** para apagar todos os campos e começar novamente.

### ✅ Cancelar
Clique em **❌ Cancelar** para fechar o formulário sem salvar.

---

## 🔧 Estrutura de Arquivos

```
Unipulso/
├── app.py                    # ← Executar este arquivo
├── data/
│   ├── pacientes.csv         # Dados salvos automaticamente
│   └── pacientes_teste.csv   # Teste
├── core/
│   ├── config.py             # Configurações
│   ├── render.py             # Renderização de pulseiras
│   └── io_manager.py         # Importar/exportar
├── ui/
│   ├── atendimento_form.py   # Formulário de atendimento
│   └── layout_editor.py      # Editor de layout
└── utils/
    └── helpers.py            # Funções utilitárias
```

---

## 📐 Dados da Pulseira

### Dimensões
- **Largura**: 29.5cm
- **Altura**: 2.0cm
- **Área imprimível**: 10.0cm (de 2.5cm a 12.5cm)

### Informações Exibidas
```
1. QR Code (com Número da carteirinha)
2. Nome do paciente (grande, centralizado)
3. Número da carteirinha (centralizado)
4. Três colunas de informações:
   - Coluna 1: Nasc, Mãe, Convênio
   - Coluna 2: Médico, Sexo, Data admissão
   - Coluna 3: Hora de admissão
5. Observação (rodapé)
```

---

## ❓ Perguntas Frequentes

### P: O que devo fazer se o formulário não abrir?
**R**: Verifique se Python 3.8+ está instalado. Execute:
```powershell
python --version
```

### P: Onde fica armazenado o arquivo CSV?
**R**: Em `data/pacientes.csv` na mesma pasta do app.

### P: Como editar dados de uma pulseira já criada?
**R**: 
1. Abra o arquivo `data/pacientes.csv` em um editor (Excel, Bloco de notas)
2. Edite a linha desejada
3. Salve o arquivo
4. Importe novamente no app

### P: Posso usar nomes com acentuação?
**R**: Sim! O sistema suporta UTF-8 completamente.

### P: Qual é o tamanho recomendado da impressora?
**R**: Impressora térmica de 58mm de largura (padrão para pulseiras hospitalares).

### P: Posso mudar as cores da pulseira?
**R**: Sim! Clique em "🎨 Editor de Layout" para customizar cores, fontes e posições.

---

## 🖨️ Como Imprimir a Pulseira

### Usando PNG:
1. Exporte como PNG
2. Abra a imagem em um programa (Paint, GIMP, etc.)
3. Imprima com as configurações:
   - Tamanho: 29.5cm × 2.0cm
   - Orientação: Paisagem
   - Sem margens

### Usando PDF:
1. Exporte como PDF
2. Abra em um leitor de PDF (Adobe Reader, etc.)
3. Imprima com as configurações:
   - Sem redimensionar
   - Sem margens

---

## 🎉 Pronto!

Agora você sabe como usar a aplicação Unipulso!

**Próximos passos:**
1. ✅ Execute `python app.py`
2. ✅ Clique em "🏥 Iniciar Atendimento"
3. ✅ Preencha os dados
4. ✅ Clique em "💾 Salvar"
5. ✅ Exporte como PNG ou PDF
6. ✅ Imprima!

**Divirta-se!** 🚀

---

**Desenvolvido com ❤️ em Novembro de 2025**
