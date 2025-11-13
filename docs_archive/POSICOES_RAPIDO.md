# 🎯 POSIÇÕES DO NOME E OBSERVAÇÃO - RÁPIDO E DIRETO

## 📂 ARQUIVO: `app.py`

## ⭐ NOME DO PACIENTE

**Linhas: 375-387**

```python
items.append(
    asdict(TextItem(
        id='nome',
        x=info_center_x,              # ← POSIÇÃO HORIZONTAL: CENTRO (8.54cm)
        y=cm_to_px(0.1),              # ← POSIÇÃO VERTICAL: 0.1cm do topo
        width=info_available_width,   # ← LARGURA: 7.70cm
        text='{Nome do paciente}',    # ← VEM DO CSV
        font_size=32,                 # ← TAMANHO: 32pt (Grande)
        bold=True,                    # ← NEGRITO
        align='center'                # ← ALINHADO AO CENTER
    ))
)
```

### Valores Concretos:
- **X**: 1009px = 8.54cm (CENTER)
- **Y**: 12px = 0.1cm
- **Largura**: 910px = 7.70cm
- **Fonte**: 32pt, negrito, centralizado

---

## ⭐ OBSERVAÇÃO

**Linhas: 503-515**

```python
obs_y = col_y_start + cm_to_px(1.2)  # ← CALCULA Y

items.append(
    asdict(TextItem(
        id='observacao',
        x=info_x_start,               # ← POSIÇÃO HORIZONTAL: ESQUERDA (4.69cm)
        y=obs_y,                      # ← POSIÇÃO VERTICAL: 1.2cm abaixo dos campos
        width=info_available_width,   # ← LARGURA: 7.70cm (MESMA DO NOME)
        text='{Observação}',          # ← VEM DO CSV
        font_size=14,                 # ← TAMANHO: 14pt (Pequeno)
        bold=False,                   # ← SEM NEGRITO
        align='left'                  # ← ALINHADO À ESQUERDA
    ))
)
```

### Valores Concretos:
- **X**: 554px = 4.69cm (ESQUERDA)
- **Y**: 235px = 2.00cm (quase no final)
- **Largura**: 910px = 7.70cm
- **Fonte**: 14pt, normal, alinhado à esquerda

---

## 📍 MAPA VISUAL

```
PULSEIRA
│
├─ 0 a 2.5cm: Não imprimível
│
└─ 2.5 a 12.5cm: ÁREA IMPRIMÍVEL
   │
   ├─ 2.60cm: QR CODE [████████]
   │          (tamanho: 1.79cm)
   │
   ├─ 4.69cm: ┌─────────────────────────────────────────┐
   │          │                                         │
   │          │ Y=0.1cm:  João Silva (NOME AQUI)        │  ← CENTER @ 8.54cm
   │          │           Centralizado, 32pt, negrito   │
   │          │                                         │
   │          │ Y=0.42cm: Carteirinha: 12345678         │  ← CENTER @ 8.54cm
   │          │           Centralizado, 20pt, negrito   │
   │          │                                         │
   │          │ Y=0.80cm: [CAMPOS EM 3 COLUNAS]         │
   │          │ Y=1.09cm:                               │
   │          │ Y=1.39cm:                               │
   │          │                                         │
   │          │ Y=2.00cm: Alergia a penicilina (OBS)    │
   │          │           Alinhado à esquerda, 14pt     │
   │          │                                         │
   │          └─────────────────────────────────────────┘
   │           (largura: 7.70cm)
   │
   └─ 12.50cm: FIM
```

---

## 🔢 NÚMEROS EXATOS

### NOME
| Propriedade | Valor | Unidade |
|-------------|-------|---------|
| X | 1009 | pixels |
| X | 8.54 | cm |
| Y | 12 | pixels |
| Y | 0.1 | cm |
| Largura | 910 | pixels |
| Largura | 7.70 | cm |
| Font Size | 32 | pt |

### OBSERVAÇÃO
| Propriedade | Valor | Unidade |
|-------------|-------|---------|
| X | 554 | pixels |
| X | 4.69 | cm |
| Y | 235 | pixels |
| Y | 2.00 | cm |
| Largura | 910 | pixels |
| Largura | 7.70 | cm |
| Font Size | 14 | pt |

---

## 🛠️ COMO MUDAR

### Mover o NOME para cima ou para baixo:
```python
# Linha ~376
y=cm_to_px(0.1)  # ← MUDAR ESTE NÚMERO

# Exemplos:
y=cm_to_px(0.05)   # Mais para cima
y=cm_to_px(0.15)   # Mais para baixo
```

### Mover a OBSERVAÇÃO para cima ou para baixo:
```python
# Linha ~504
obs_y = col_y_start + cm_to_px(1.2)  # ← MUDAR ESTE NÚMERO

# Exemplos:
obs_y = col_y_start + cm_to_px(1.0)  # Mais para cima
obs_y = col_y_start + cm_to_px(1.5)  # Mais para baixo
```

### Aumentar o tamanho da fonte:
```python
# NOME - Linha ~381
font_size=32  # ← MUDAR ESTE NÚMERO (ex: 36, 40)

# OBS - Linha ~514
font_size=14  # ← MUDAR ESTE NÚMERO (ex: 16, 18)
```

---

## ✨ RESUMO

| Item | Posição X | Posição Y | Tamanho | Alinhamento |
|------|-----------|-----------|---------|-------------|
| **NOME** | 8.54cm (CENTER) | 0.1cm | 32pt | Centralizado |
| **OBS** | 4.69cm (ESQUERDA) | 2.0cm | 14pt | Esquerda |

---

**Tudo está no método `_default_layout()` em `app.py`!**
