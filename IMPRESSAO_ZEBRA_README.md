# 🖨️ Impressão Direta Zebra ZD230

## 📋 Visão Geral

Este módulo implementa impressão direta para impressoras Zebra ZD230 usando comandos ZPL (Zebra Programming Language). A impressão é feita via comunicação RAW, sem necessidade de drivers ou diálogos do sistema.

## ✅ Funcionalidades Implementadas

- ✅ Impressão direta via ZPL
- ✅ Detecção automática de impressoras Zebra
- ✅ Teste de conexão e impressão
- ✅ Impressão de pulseira individual
- ✅ Impressão em lote (todas as pulseiras do CSV)
- ✅ Interface gráfica integrada com:
  - Aba dedicada para impressão
  - Botão de ação rápida na sidebar
  - Menu completo de impressão
  - Configuração de impressora
  - Status em tempo real

## 📦 Dependências

### Windows

```bash
pip install pywin32
```

### Linux

```bash
pip install pycups
```

## 🔧 Instalação da Impressora

### 1. Instalar Driver Zebra

1. Baixe o driver da Zebra ZD230 do site oficial: https://www.zebra.com/
2. Instale o driver seguindo as instruções do fabricante
3. Conecte a impressora via USB
4. Verifique se a impressora aparece em "Dispositivos e Impressoras" do Windows

### 2. Configurar Nome da Impressora

Por padrão, o sistema procura por uma impressora chamada "Zebra ZD230". 

Para verificar o nome exato:
1. Abra "Dispositivos e Impressoras" no Windows
2. Localize sua impressora Zebra
3. Anote o nome exato

Para alterar no aplicativo:
1. Menu > Impressão > Configurar Impressora
2. Selecione sua impressora na lista
3. Clique em "Testar e Salvar"

## 🎯 Como Usar

### Pela Interface Gráfica

#### Opção 1: Menu Superior
```
Menu > Impressão > Imprimir Pulseira Atual
Menu > Impressão > Imprimir Todas as Pulseiras
Menu > Impressão > Teste de Impressão
Menu > Impressão > Configurar Impressora
```

#### Opção 2: Aba de Impressão
1. Clique na aba "🖨️ Impressão"
2. Verifique o status da impressora
3. Use os botões para:
   - Imprimir pulseira atual
   - Imprimir todas as pulseiras
   - Fazer teste de impressão
   - Configurar impressora

#### Opção 3: Ação Rápida (Sidebar)
- Botão "🖨️ Imprimir Atual" na sidebar esquerda

### Por Código Python

```python
from utils.zebra_printer import ZebraPrinter, generate_bracelet_zpl

# Criar instância da impressora
printer = ZebraPrinter("Zebra ZD230")

# Verificar se está disponível
if printer.is_printer_available():
    # Dados do paciente
    patient_data = {
        'Nome do paciente': 'João Silva',
        'Número da carteirinha': '123456',
        'Data de nascimento': '01/01/1990',
        # ... outros campos
    }
    
    # Gerar ZPL
    zpl = generate_bracelet_zpl(patient_data)
    
    # Imprimir
    printer.send_zpl(zpl)
```

## 🧪 Testes

### Teste Rápido de Conexão

```bash
cd utils
python zebra_printer.py
```

Isso irá:
1. Listar todas as impressoras disponíveis
2. Verificar se a Zebra ZD230 está conectada
3. Perguntar se deseja imprimir uma etiqueta de teste

### Teste de Impressão pela Interface

1. Abra o aplicativo
2. Menu > Impressão > Teste de Impressão
3. Uma etiqueta de teste será impressa

## 📐 Layout da Pulseira ZPL

O layout da pulseira em ZPL é otimizado para a Zebra ZD230:

- **DPI**: 203 (8 dots/mm)
- **Largura**: 11cm (880 dots)
- **Altura**: 2cm (160 dots)

### Elementos:

1. **QR Code** (esquerda)
   - Tamanho: automático
   - Posição: 30,30
   - Dados: Número da carteirinha

2. **Nome do Paciente** (topo)
   - Fonte: 24pt
   - Posição: 200,30
   - Limitado a 30 caracteres

3. **Informações** (corpo)
   - Carteirinha
   - Data de nascimento
   - Nome da mãe
   - Convênio
   - Médico responsável
   - Sexo
   - Data/Hora de admissão
   - Observações

## 🛠️ Troubleshooting

### Problema: "Impressora não encontrada"

**Solução:**
1. Verifique se a impressora está ligada e conectada
2. Verifique o nome exato em "Dispositivos e Impressoras"
3. Use Menu > Impressão > Configurar Impressora
4. Selecione a impressora correta na lista

### Problema: "Módulo win32print não encontrado"

**Solução:**
```bash
pip install pywin32
```

### Problema: "Impressora não imprime"

**Solução:**
1. Verifique se há papel/etiquetas na impressora
2. Execute um teste de impressão direto pela impressora
3. Verifique se a impressora está configurada como "RAW" no Windows
4. Teste com Menu > Impressão > Teste de Impressão

### Problema: "Layout da pulseira incorreto"

**Solução:**
1. Verifique se a largura das etiquetas está configurada corretamente
2. Ajuste as posições no arquivo `utils/zebra_printer.py`
3. Função `generate_bracelet_zpl()` contém todos os parâmetros de layout

## 📚 Referências

- [Documentação ZPL da Zebra](https://www.zebra.com/us/en/support-downloads/knowledge-articles/zpl-programming-guide.html)
- [Comandos ZPL](https://www.zebra.com/content/dam/zebra/manuals/printers/common/programming/zpl-zbi2-pm-en.pdf)
- [Zebra ZD230 Product Page](https://www.zebra.com/us/en/products/printers/industrial/zd200-series.html)

## 🔄 Atualizações Futuras

- [ ] Suporte para diferentes tamanhos de etiqueta
- [ ] Editor visual de layout ZPL
- [ ] Pré-visualização do ZPL
- [ ] Histórico de impressões
- [ ] Impressão por rede (IP)
- [ ] Suporte para outras impressoras Zebra

## 📝 Notas Técnicas

### Formato ZPL

Os comandos ZPL seguem este padrão:

```zpl
^XA              ; Início do formato
^FO50,50         ; Field Origin (posição X,Y)
^ADN,36,20       ; Font (tipo D, altura 36, largura 20)
^FDTexto^FS      ; Field Data
^XZ              ; Fim do formato
```

### Conversão de Unidades

- 1 cm = 10 mm
- 203 DPI = 8 dots/mm
- 11 cm = 110 mm = 880 dots
- 2 cm = 20 mm = 160 dots

## ✅ Checklist de Implementação

- [x] Criar módulo `utils/zebra_printer.py`
- [x] Implementar classe `ZebraPrinter`
- [x] Implementar função `generate_bracelet_zpl()`
- [x] Adicionar menu de impressão
- [x] Adicionar aba de impressão
- [x] Adicionar botão de ação rápida
- [x] Implementar configuração de impressora
- [x] Implementar status em tempo real
- [x] Testes de impressão
- [x] Documentação completa

## 🎉 Conclusão

A funcionalidade de impressão direta Zebra ZD230 está totalmente implementada e integrada ao aplicativo Unipulso. Basta instalar o driver da impressora e a dependência `pywin32` para começar a usar!
