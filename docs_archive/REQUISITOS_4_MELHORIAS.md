# 📋 REQUISITOS - 4 Melhorias Essenciais

## 1️⃣ Ajustar Layout: QR Code Separado das Informações

### Requisito
- Ajustar layout para que o QR Code fique separado das informações do paciente
- QR Code à esquerda, isolado
- Informações do paciente à direita e abaixo, sem sobrepor o QR

### Especificação
- QR Code: Lado esquerdo da pulseira, sem textos por cima
- Informações: Lado direito, começando após o QR
- Layout deve ser clean e legível
- Sem conflitos visuais

### Arquivos a Modificar
- `app.py` - método `_default_layout()`

### Aceitação
✅ QR Code visível e legível  
✅ Nenhuma informação sobrepõe o QR  
✅ Todas as informações ainda aparecem

---

## 2️⃣ Limpar Campos ao Iniciar Atendimento

### Requisito
- Ao clicar em "Iniciar Atendimento", limpar todos os campos para evitar dados do paciente anterior
- Garantir que cada novo atendimento comece com formulário vazio

### Especificação
- Quando `abrir_formulario()` é chamado, limpar todos os campos
- Data e hora de admissão serão preenchidas automaticamente (requisito 4)
- Sem resíduos de dados anteriores

### Arquivos a Modificar
- `ui/atendimento_form.py` - método `abrir_formulario()`

### Aceitação
✅ Formulário abre sempre vazio  
✅ Nenhum dado residual do paciente anterior  
✅ Ready para novo preenchimento

---

## 3️⃣ Histórico Local com Filtro por Data

### Requisito
- Implementar histórico local dos atendimentos, organizado por ano/mês/dia
- Dados salvos localmente no computador
- Possibilidade de filtrar/visualizar por data

### Especificação
- Criar pasta `data/historico/YYYY/MM/` para cada data
- Arquivo de índice com metadados: `data/historico/indice.json`
- Manter `data/pacientes.csv` como compatibilidade
- Novo método: `_salvar_com_historico()` que:
  - Cria estrutura de pastas por data
  - Salva em `pacientes.csv` (compatibilidade)
  - Salva em JSON no histórico (organizado por data)
  - Atualiza `indice.json` com referência

### Estrutura de Pastas
```
data/
├── pacientes.csv                    (compatibilidade)
└── historico/
    └── 2025/
        └── 11/
            └── 11/
                ├── atendimentos_2025-11-11.json
                └── indice_2025-11-11.json
└── indice.json                      (índice geral)
```

### Estrutura de Dados

**indice.json** (geral):
```json
{
  "atendimentos": [
    {
      "id": "UUID",
      "data": "2025-11-11",
      "hora": "14:30",
      "paciente": "Roberta Silva",
      "caminho": "historico/2025/11/11/atendimentos_2025-11-11.json"
    }
  ]
}
```

**atendimentos_2025-11-11.json** (por data):
```json
{
  "data": "2025-11-11",
  "atendimentos": [
    {
      "id": "UUID",
      "numero_carteirinha": "8968514265",
      "nome_paciente": "Roberta Silva",
      "data_nascimento": "18/08/2004",
      ...
    }
  ]
}
```

### Arquivos a Criar
- `utils/historico_manager.py` - Nova classe para gerenciar histórico

### Arquivos a Modificar
- `ui/atendimento_form.py` - método `_gerar_csv()` chamará `_salvar_com_historico()`
- `app.py` - Adicionar botão "Visualizar Histórico" e método para filtrar por data

### Aceitação
✅ Atendimentos salvos com data automática  
✅ Possível filtrar por data/período  
✅ Dados organizados em pastas  
✅ CSV compatível para importação

---

## 4️⃣ Data e Hora de Admissão Automáticas

### Requisito
- Data de admissão e hora de admissão devem ser preenchidas automaticamente com base no relógio do computador
- Usuário não precisa digitar (mas pode editar se necessário)

### Especificação
- Ao abrir o formulário, preencher automaticamente:
  - "Data de admissão" = data atual (DD/MM/AAAA)
  - "Hora de admissão" = hora atual (HH:MM)
- Usuário pode editar se desejar
- Validação de formato continua funcionando

### Implementação
- Usar `datetime.now()` ao abrir o formulário
- Formatar como `DD/MM/AAAA` e `HH:MM`
- Preencher nos campos após criar a UI

### Arquivos a Modificar
- `ui/atendimento_form.py` - método `abrir_formulario()`

### Aceitação
✅ Data preenchida automaticamente  
✅ Hora preenchida automaticamente  
✅ Usuário pode editar se desejar  
✅ Formato correto (DD/MM/AAAA e HH:MM)

---

## 📊 Resumo dos Requisitos

| # | Requisito | Prioridade | Complexidade | Status |
|---|-----------|-----------|--------------|--------|
| 1 | QR separado | Alta | Baixa | ⏳ Pendente |
| 2 | Limpar campos ao abrir | Alta | Baixa | ⏳ Pendente |
| 3 | Histórico por data | Média | Alta | ⏳ Pendente |
| 4 | Data/hora automáticas | Alta | Baixa | ⏳ Pendente |

---

## 🎯 Ordem de Implementação

1. ✅ **Requisito 2 (Limpar campos)** - Rápido, libera teste do 4
2. ✅ **Requisito 4 (Data/hora automáticas)** - Depende do 2
3. ✅ **Requisito 1 (QR separado)** - Requer ajuste visual
4. ✅ **Requisito 3 (Histórico)** - Mais complexo, deixar por último

---

## 📝 Notas Técnicas

### Requisito 2 - Limpar Campos
- Chamar `_limpar_campos()` logo após criar a UI
- Garantir que placeholders apareçam

### Requisito 4 - Data/Hora Automáticas
- Usar `from datetime import datetime`
- Formato: `datetime.now().strftime('%d/%m/%Y')` e `.strftime('%H:%M')`
- Inserir após criar os widgets

### Requisito 1 - QR Separado
- Aumentar espaçamento horizontal
- QR Code deve estar em área dedicada
- Informações começam após o QR

### Requisito 3 - Histórico
- Criar classe `HistoricoManager` em `utils/`
- UUID para cada atendimento (para rastreabilidade)
- JSON para facilitar filtros futuros
- Manter CSV para compatibilidade

---

## ✅ Critérios de Aceitação Geral

- [ ] Requisito 1: QR Code não sobrepõe textos
- [ ] Requisito 2: Formulário abre vazio sempre
- [ ] Requisito 3: Histórico organizável por data
- [ ] Requisito 4: Data/hora preenchidas automaticamente

---

**Data:** 11 de Novembro de 2025  
**Status:** 📋 Requisitos Documentados  
**Próxima Ação:** Iniciar implementação
