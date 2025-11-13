# 📍 POSIÇÕES NO CÓDIGO - NOME E OBSERVAÇÃO

## 📂 Arquivo: `app.py`

## 🎯 LOCALIZAÇÃO NO CÓDIGO

### **NOME DO PACIENTE**

**Local**: Linhas 375-387 do arquivo `app.py`

```python
# ========== INFORMAÇÕES DO PACIENTE (LADO DIREITO) ==========
# Começam após o QR Code, ainda dentro da área imprimível
info_x_start = qr_x + qr_size + cm_to_px(0.3)  # Gap de 0.3cm após QR
info_available_width = printable_area_end - info_x_start - cm_to_px(0.1)  # Até fim da imprimível - margem
info_center_x = info_x_start + (info_available_width // 2)  # Centro da área de informações

# Nome (grande, centralizado)
items.append(
    asdict(TextItem(
        id='nome',                                    # ← ID do elemento
        x=info_center_x,                             # ← POSIÇÃO HORIZONTAL (CENTER)
        y=cm_to_px(0.1),                             # ← POSIÇÃO VERTICAL (0.1cm do topo)
        width=info_available_width,                  # ← LARGURA
        text='{Nome do paciente}',                   # ← TEXTO (vinculado ao CSV)
        font_size=32,                                # ← TAMANHO DA FONTE
        bold=True,                                   # ← NEGRITO
        align='center'                               # ← ALINHAMENTO
    ))
)
```

### **RESUMO DAS POSIÇÕES DO NOME**

```
Propriedade          │ Valor              │ Significado
─────────────────────┼────────────────────┼──────────────────────────────
id                   │ 'nome'             │ Identificador único
x (horizontal)       │ info_center_x      │ Centralizado (8.54cm)
y (vertical)         │ cm_to_px(0.1)      │ 0.1cm do topo = 12px
width                │ info_available_... │ 7.70cm de largura
text                 │ {Nome do paciente} │ Vem do CSV
font_size            │ 32                 │ Grande (32pt)
bold                 │ True               │ Em negrito
align                │ 'center'           │ Centralizado
```

---

### **CARTEIRINHA**

**Local**: Linhas 389-401 do arquivo `app.py`

```python
# Carteirinha
items.append(
    asdict(TextItem(
        id='carteirinha',
        x=info_center_x,                             # ← MESMO CENTER QUE O NOME
        y=cm_to_px(0.1) + 38,  # 0.3cm abaixo do nome (~38px)  # ← POSIÇÃO VERTICAL
        width=info_available_width,
        text='Carteirinha: {Número da carteirinha}',
        font_size=20,
        bold=True,
        align='center'
    ))
)
```

**Y = 38px abaixo do nome** (aproximadamente 0.3cm)

---

### **OBSERVAÇÃO**

**Local**: Linhas 503-515 do arquivo `app.py`

```python
# Observação (linha separada, mais abaixo)
obs_y = col_y_start + cm_to_px(1.2)  # Bem abaixo das 3 colunas

items.append(
    asdict(TextItem(
        id='observacao',                             # ← ID do elemento
        x=info_x_start,                              # ← ALINHADO À ESQUERDA (4.69cm)
        y=obs_y,                                     # ← POSIÇÃO VERTICAL (calculada acima)
        width=info_available_width,                  # ← MESMA LARGURA DO NOME (7.70cm)
        text='{Observação}',                         # ← TEXTO (vinculado ao CSV)
        font_size=14,                                # ← TAMANHO DA FONTE
        bold=False,                                  # ← SEM NEGRITO
        align='left'                                 # ← ALINHADO À ESQUERDA
    ))
)
```

### **RESUMO DAS POSIÇÕES DA OBSERVAÇÃO**

```
Propriedade          │ Valor              │ Significado
─────────────────────┼────────────────────┼──────────────────────────────
id                   │ 'observacao'       │ Identificador único
x (horizontal)       │ info_x_start       │ Alinhado à esquerda (4.69cm)
y (vertical)         │ obs_y              │ 1.2cm abaixo das colunas
width                │ info_available_... │ 7.70cm de largura
text                 │ {Observação}       │ Vem do CSV
font_size            │ 14                 │ Menor (14pt)
bold                 │ False              │ Sem negrito
align                │ 'left'             │ Alinhado à esquerda
```

---

## 📐 CÁLCULOS DAS POSIÇÕES

### **Para o NOME:**

```python
# Passo 1: Calcular onde começa a área de informações
info_x_start = qr_x + qr_size + cm_to_px(0.3)
# Resultado: 554px = 4.69cm

# Passo 2: Calcular quanto espaço tem
info_available_width = printable_area_end - info_x_start - cm_to_px(0.1)
# Resultado: 910px = 7.70cm

# Passo 3: Encontrar o CENTER
info_center_x = info_x_start + (info_available_width // 2)
# info_center_x = 554 + (910 // 2) = 554 + 455 = 1009px = 8.54cm

# Passo 4: Posição Y do nome
y_nome = cm_to_px(0.1)  # = 12px = 0.1cm
```

### **Para a OBSERVAÇÃO:**

```python
# Passo 1: Y começa onde os campos terminam
col_y_start = cm_to_px(0.8)  # = 94px
line_height = cm_to_px(0.3)  # = 35px

# Passo 2: Há 3 linhas de campos (0.8cm + 0.3cm + 0.3cm + 0.3cm = 1.7cm)
# Adicionar mais 1.2cm de espaço
obs_y = col_y_start + cm_to_px(1.2)
# obs_y = 94 + 141 = 235px (aproximadamente 2.0cm - quase no final)

# Passo 3: X da observação começa no início da área
x_obs = info_x_start  # = 554px = 4.69cm
```

---

## 🎨 VISUAL DAS POSIÇÕES

```
PULSEIRA COMPLETA (29.5cm × 2.0cm)
├─ 0.0cm até 2.5cm: Área NÃO imprimível
│
└─ 2.5cm até 12.5cm: ÁREA IMPRIMÍVEL (onde tudo fica)
   │
   ├─ 2.60cm: Início do QR Code
   │   └─ Tamanho: 1.79cm
   │
   ├─ 4.69cm: INÍCIO DA ÁREA DE INFORMAÇÕES ← info_x_start
   │   │
   │   ├─ Y = 0.1cm: ⭐ NOME (centralizado em 8.54cm)
   │   │             "João Silva"
   │   │
   │   ├─ Y = 0.42cm: ⭐ CARTEIRINHA (centralizado em 8.54cm)
   │   │             "Carteirinha: 12345678"
   │   │
   │   ├─ Y = 0.80cm: CAMPOS EM 3 COLUNAS
   │   │   └─ Nasc: 15/03  │ Med: Dr. C... │ Hora: 14:30
   │   │
   │   ├─ Y = 1.09cm:
   │   │   └─ Mãe: Maria   │ Sex: Masc     │
   │   │
   │   ├─ Y = 1.39cm:
   │   │   └─ Conv: Unimed │ Adm: 11/11    │
   │   │
   │   └─ Y = 2.00cm: ⭐ OBSERVAÇÃO (alinhado à esquerda em 4.69cm)
   │                  "Alergia a penicilina"
   │
   └─ 12.50cm: FIM DA ÁREA IMPRIMÍVEL
```

---

## 🔧 COMO MODIFICAR NO CÓDIGO

### **Para mudar a posição do NOME:**

No arquivo `app.py`, linha ~376:

```python
# ANTES:
x=info_center_x,    # ← Centralizado
y=cm_to_px(0.1),    # ← 0.1cm do topo

# DEPOIS (para mover para cima):
x=info_center_x,    # ← Mantém centralizado
y=cm_to_px(0.05),   # ← Mais para cima (0.05cm)
```

### **Para mudar a posição da OBSERVAÇÃO:**

No arquivo `app.py`, linha ~504:

```python
# ANTES:
obs_y = col_y_start + cm_to_px(1.2)  # ← 1.2cm abaixo dos campos

# DEPOIS (para mover para cima):
obs_y = col_y_start + cm_to_px(1.0)  # ← 1.0cm abaixo dos campos
```

### **Para mudar tamanho do NOME:**

No arquivo `app.py`, linha ~381:

```python
# ANTES:
font_size=32,  # ← Tamanho atual

# DEPOIS (para aumentar):
font_size=36,  # ← Mais grande
```

---

## 📊 TABELA COMPLETA DE POSIÇÕES

| Elemento | X (cm) | Y (cm) | Largura (cm) | Font Size | Align |
|----------|--------|--------|--------------|-----------|-------|
| **QR Code** | 2.60 | 0.1 | 1.79 | - | - |
| **Nome** | 8.54 (CENTER) | 0.1 | 7.70 | 32pt | center |
| **Carteirinha** | 8.54 (CENTER) | 0.42 | 7.70 | 20pt | center |
| **Nasc** | 4.69 | 0.80 | 2.50 | 16pt | left |
| **Mãe** | 4.69 | 1.09 | 2.50 | 16pt | left |
| **Conv** | 4.69 | 1.39 | 2.50 | 16pt | left |
| **Med** | 7.34 | 0.80 | 2.50 | 16pt | left |
| **Sex** | 7.34 | 1.09 | 2.50 | 16pt | left |
| **Adm** | 7.34 | 1.39 | 2.50 | 16pt | left |
| **Hora** | 9.99 | 0.80 | 2.50 | 16pt | left |
| **Observação** | 4.69 | 2.00 | 7.70 | 14pt | left |

---

**Tudo está no método `_default_layout()` da classe `PulseiraApp` em `app.py`!**
