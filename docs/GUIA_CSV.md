# 📋 Guia: Importar CSV Corretamente

## 🔴 Problema

Você estava importando um CSV que tinha problemas na estrutura. A imagem mostrava que o app.py não estava reconhecendo as colunas corretamente.

### Causas Possíveis:

1. **Delimitador Errado** (MAIS COMUM)
   - CSV salvo com TAB (`\t`) em vez de vírgula (`,`)
   - CSV salvo com ponto-e-vírgula (`;`) 

2. **Espaços Extras**
   - Espaços no início/final dos nomes de coluna
   - Espaços no início/final dos valores

3. **Colunas Faltando ou Diferentes**
   - Nomes de coluna ligeiramente diferentes
   - Colunas em ordem diferente

---

## ✅ Solução

### 1. Formato Correto do CSV

O arquivo CSV **deve** ter **vírgulas** como delimitador:

```csv
Número da carteirinha,Nome do paciente,Data de nascimento,Nome da mãe,Convênio,Médico responsável,Sexo,Data de admissão,Hora de admissão,Observação
123456,João Silva,1990-05-12,Maria Silva,SUS,Dra. Aline,M,2025-10-15,14:30,Alergia: Penicilina
987654,Ana Pereira,1985-08-01,Clara Pereira,Particular,Dr. Bruno,F,2025-10-15,15:10,Uso contínuo: Losartana
```

### 2. As 10 Colunas Obrigatórias

Certifique-se que seu CSV tem **EXATAMENTE** estas colunas (e nessa ordem):

| # | Coluna | Tipo | Exemplo |
|---|--------|------|---------|
| 1 | `Número da carteirinha` | Texto/Número | 123456 |
| 2 | `Nome do paciente` | Texto | João Silva |
| 3 | `Data de nascimento` | Data (YYYY-MM-DD) | 1990-05-12 |
| 4 | `Nome da mãe` | Texto | Maria Silva |
| 5 | `Convênio` | Texto | SUS, Particular, etc |
| 6 | `Médico responsável` | Texto | Dra. Aline |
| 7 | `Sexo` | Letra (M/F) | M ou F |
| 8 | `Data de admissão` | Data (YYYY-MM-DD) | 2025-10-15 |
| 9 | `Hora de admissão` | Hora (HH:MM) | 14:30 |
| 10 | `Observação` | Texto livre | Alergia: Penicilina |

### 3. Como Abrir/Salvar em Excel

#### Microsoft Excel:
1. Abra Excel
2. Crie as colunas com os nomes acima
3. Preecha os dados
4. **Arquivo > Salvar Como**
5. Selecione: **CSV (delimitado por vírgula) (.csv)**
6. Salve o arquivo

#### LibreOffice Calc:
1. Abra LibreOffice Calc
2. Crie as colunas com os nomes acima
3. Preencha os dados
4. **Arquivo > Salvar Como**
5. Selecione: **CSV Text (.csv)**
6. Escolha delimitador: **,** (vírgula)

#### Google Sheets:
1. Crie a planilha
2. **Arquivo > Fazer Download > Valores separados por vírgula (.csv)**

---

## 🧪 Validar Seu CSV

Criamos uma ferramenta para testar se o CSV está correto:

### No Terminal/PowerShell:

```bash
cd c:\Users\vhaza\Desktop\Unipulso-3-\Unipulso
python test_csv_import.py seu_arquivo.csv
```

### Exemplo:

```bash
python test_csv_import.py teste_dados.csv
```

### Resultado Esperado:

```
✓ Todas as colunas obrigatórias estão presentes!
✓ Sem colunas extras desnecessárias!
...
✅ CSV VÁLIDO - Pode ser importado sem problemas!
```

---

## 🎯 Passo a Passo para Usar o App

### 1️⃣ Preparar o CSV

- Crie um arquivo com as 10 colunas obrigatórias
- Salve como **CSV com vírgula como delimitador**
- Valide com `python test_csv_import.py seu_arquivo.csv`

### 2️⃣ Abrir o App

```bash
python app.py
```

### 3️⃣ Importar o CSV

- Clique em **"Importar CSV"**
- Selecione seu arquivo `.csv`
- O app mostrará: **"X paciente(s) importado(s)."**

### 4️⃣ Visualizar Preview

- A primeira pulseira aparecerá na pré-visualização
- Se os dados estão errados, volte ao CSV e corrija

### 5️⃣ Exportar

- **Exportar PNG**: Cria arquivo(s) PNG para impressão
- **Exportar PDF**: Cria arquivo PDF com todas as pulseiras

---

## 🔧 Troubleshooting

### ❌ "Colunas obrigatórias ausentes"

**Solução:**
- Rode `python test_csv_import.py seu_arquivo.csv`
- Veja quais colunas estão faltando
- Adicione-as no Excel com os **nomes exatos**

### ❌ "CSV está vazio"

**Solução:**
- Verifique se o arquivo tem dados além do header
- Certifique-se que não está usando delimitador errado (TAB ou `;`)

### ❌ "Dados aparecem errados no app"

**Solução:**
1. Execute `python test_csv_import.py seu_arquivo.csv`
2. Veja se os dados estão sendo lidos corretamente
3. Se estão OK na ferramenta, é problema de renderização no app
4. Se não estão OK, o problema é o CSV

### ❌ Colunas aparecem como uma longa string

**Solução:**
- Seu arquivo está usando **TAB** em vez de **vírgula**
- Abra em Excel: **Arquivo > Salvar Como > CSV (delimitado por vírgula)**

---

## 💡 Dicas

### ✅ Boas Práticas

1. **Use nomes de coluna exatos** - cópia/cola dos nomes acima
2. **Não adicione espaços** no começo/fim das colunas
3. **Use datas no formato** `YYYY-MM-DD` (2025-10-15)
4. **Use horas no formato** `HH:MM` (14:30)
5. **Valide sempre** antes de usar: `python test_csv_import.py seu_arquivo.csv`

### ⚠️ Evite

1. ❌ CSVs com TAB como delimitador
2. ❌ Nomes de coluna com espaços no início/fim
3. ❌ Datas em formato DD/MM/YYYY
4. ❌ Valores vazios nas colunas obrigatórias
5. ❌ Caracteres especiais sem encoding UTF-8

---

## 📁 Arquivos de Exemplo

No diretório `Unipulso/` você encontra:

- `teste_dados.csv` - Exemplo válido com 2 pacientes
- `test_csv_import.py` - Ferramenta de validação

### Usar como Template:

```bash
# Copiar o arquivo de exemplo
Copy-Item teste_dados.csv meus_pacientes.csv

# Editar em Excel/Notepad
# ...adicionar seus pacientes...

# Validar
python test_csv_import.py meus_pacientes.csv

# Importar no app
# Abrir app.py > Importar CSV > Selecionar meus_pacientes.csv
```

---

## 🎓 O Que Melhoramos

A versão atual do `io_manager.py` agora:

✅ **Detecta automaticamente** se o CSV usa `,`, `;` ou `\t`  
✅ **Remove espaços extras** dos nomes de coluna e valores  
✅ **Tolera colunas extras** (você pode adicionar colunasadicionais)  
✅ **Colunas em qualquer ordem** (não precisa ser exatamente nessa ordem)  
✅ **Mensagens de erro claras** indicando quais colunas faltam  

---

## 📞 Próximos Passos

1. Teste o `teste_dados.csv` no app
2. Crie seu próprio CSV com seus pacientes
3. Valide com `python test_csv_import.py`
4. Importe no app e exporte as pulseiras!

**Sucesso! 🎉**
