# 🚀 QUICKSTART - Primeiros Passos

## 1️⃣ Instalação

```bash
# Clonar/entrar no projeto
cd Unipulso

# Ativar virtual environment
.\venv\Scripts\activate      # Windows PowerShell
# ou
.\venv\Scripts\activate.bat  # Windows CMD

# Instalar dependências
pip install -r requirements.txt
```

## 2️⃣ Executar a Aplicação

```bash
python main.py    # Modo legado (se existir)
# ou
python app.py     # Modo refatorado (RECOMENDADO)
```

## 3️⃣ Estrutura de Arquivos

```
Unipulso/
├── config.py              ← Configurações globais
├── models.py              ← Estruturas de dados
├── utils.py               ← Funções reutilizáveis
├── render.py              ← Renderização de imagens
├── io_manager.py          ← Import/Export (CSV, PNG, PDF)
├── layout_editor.py       ← Editor visual
├── app.py                 ← Interface principal ⭐ COMECE AQUI
├── requirements.txt       ← Dependências
├── templates/             ← Modelos JSON salvos
├── MODULAR_GUIDE.md       ← Guia de uso
├── ARCHITECTURE.md        ← Documentação técnica
└── REFACTORING_SUMMARY.md ← Resumo da refatoração
```

## 4️⃣ Usando os Módulos

### Opção A: GUI (Recomendado para iniciante)

```bash
python app.py
```

Funcionalidades:
- 📤 Upload de logotipo
- 📥 Importar CSV
- ✏️ Editor de layout visual
- 💾 Salvar/carregar modelos
- 📊 Pré-visualização ao vivo
- 🖼️ Exportar PNG
- 📄 Exportar PDF

### Opção B: Script Programático

```python
# script_processamento.py
from io_manager import IOManager
from render import render_layout_to_image
from models import LayoutModel
from utils import list_system_fonts
import json

# 1. Carregar dados
io = IOManager()
patients = io.import_csv('dados.csv')

# 2. Carregar layout
with open('templates/modelo.json') as f:
    layout = LayoutModel.from_dict(json.load(f))

# 3. Preparar fontes
fonts_map = list_system_fonts()

# 4. Renderizar
for patient in patients:
    img = render_layout_to_image(layout, patient, fonts_map)
    filename = f"saida/pulseira_{patient['Número da carteirinha']}.png"
    img.save(filename)

print(f"✅ {len(patients)} pulseiras geradas!")
```

## 5️⃣ Arquivos de Entrada Esperados

### CSV (dados_exemplo.csv)
```csv
Número da carteirinha,Nome do paciente,Data de nascimento,Nome da mãe,Convênio,Médico responsável,Sexo,Data de admissão,Hora de admissão,Observação
123456,João Silva,1990-05-12,Maria Silva,SUS,Dra. Aline,M,2025-10-15,14:30,Alergia: Penicilina
987654,Ana Pereira,1985-08-01,Clara Pereira,Particular,Dr. Bruno,F,2025-10-15,15:10,Uso contínuo: Losartana
```

### Modelo JSON (templates/modelo.json)
```json
{
  "width": 8860,
  "height": 472,
  "items": [
    {
      "type": "qr",
      "id": "qr1",
      "x": 708,
      "y": 29,
      "size": 414,
      "binding": "Número da carteirinha"
    },
    {
      "type": "text",
      "id": "nome",
      "x": 3543,
      "y": 29,
      "text": "{Nome do paciente}",
      "font_size": 48,
      "bold": true,
      "align": "center"
    }
  ]
}
```

## 6️⃣ Referência Rápida de Funções

### config.py
```python
from config import P_WIDTH, P_HEIGHT, DPI, cm_to_px
width_px = cm_to_px(29.5)  # Converter cm para pixels
```

### utils.py
```python
from utils import generate_qr_image, list_system_fonts

qr = generate_qr_image("123456", 100)
fonts = list_system_fonts()
```

### models.py
```python
from models import TextItem, QRItem, LayoutModel

item = TextItem(id='text1', x=100, y=50, text='Olá!')
layout = LayoutModel()
layout.items.append(item.to_dict())
```

### render.py
```python
from render import render_layout_to_image

img = render_layout_to_image(layout, patient_data, fonts_map)
img.save('pulseira.png', dpi=(300, 300))
```

### io_manager.py
```python
from io_manager import IOManager

io = IOManager()
patients = io.import_csv('dados.csv')
io.export_png(patients, layout, fonts_map)
```

## 7️⃣ Solução de Problemas

### Erro: "Import PIL could not be resolved"
```bash
# Pillow não está instalado
pip install Pillow
```

### Erro: "No Python at..."
```bash
# Recriado ambiente virtual
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Erro: "Module not found: 'models'"
```bash
# Certifique-se de estar no diretório correto
cd Unipulso
python app.py
```

## 8️⃣ Personalizações Comuns

### Mudar tamanho padrão de fonte
**Em:** `app.py`
```python
self.font_size = 50  # Aumentar de 32 para 50
```

### Mudar cores do layout
**Em:** `models.py` / Editor Visual
```python
TextItem(color='#FF0000')  # Vermelho
```

### Adicionar novo campo CSV
1. Adicionar coluna em `EXPECTED_COLUMNS` (config.py)
2. Usar em items: `{Novo Campo}`
3. Pronto!

## 9️⃣ Recursos Adicionais

📖 **Leitura:**
- `MODULAR_GUIDE.md` - Guia completo de uso
- `ARCHITECTURE.md` - Documentação técnica
- `REFACTORING_SUMMARY.md` - Resumo da refatoração

💻 **Código:**
- Exemplos em cada módulo (docstrings)
- Scripts de teste em cada arquivo

🎓 **Aprendizado:**
- Padrões de design SOLID
- Arquitetura modular
- Type hints em Python
- Dataclasses

## 🔟 Checklist para Começar

- ✅ Python 3.8+ instalado
- ✅ Virtual environment ativado
- ✅ Dependências instaladas (`pip install -r requirements.txt`)
- ✅ Arquivo CSV preparado
- ✅ Logotipo em PNG (opcional)
- ✅ Pronto para `python app.py`!

---

## 📞 Próximos Passos

1. **Explorar a GUI**
   - Fazer upload de logotipo
   - Importar CSV
   - Abrir editor de layout
   - Exportar PNG/PDF

2. **Entender os módulos**
   - Ler docstrings
   - Estudar exemplos
   - Modificar um parâmetro

3. **Criar novo recurso**
   - Adicionar função em `utils.py`
   - Integrar em `render.py`
   - Usar em `app.py`

---

**Tudo pronto! Boa sorte! 🚀**
