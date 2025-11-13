# 🚀 Guia Rápido - Impressão Zebra ZD230

## 📦 Instalação das Dependências

### 1. Instalar pywin32 (Windows)

```bash
pip install pywin32
```

**Ou instalar todas as dependências do projeto:**

```bash
pip install -r requirements.txt
```

## 🖨️ Configurar Impressora

### 1. Instalar Driver Zebra

1. Acesse: https://www.zebra.com/us/en/support-downloads.html
2. Procure por "ZD230"
3. Baixe o driver para Windows
4. Instale seguindo o assistente
5. Conecte a impressora via USB
6. Aguarde o Windows reconhecer a impressora

### 2. Verificar Instalação

1. Abra **Painel de Controle** > **Dispositivos e Impressoras**
2. Localize a impressora Zebra
3. Anote o nome exato (ex: "Zebra ZD230")
4. Clique com botão direito > **Propriedades da Impressora**
5. Em **Avançado**, verifique se está configurado como "RAW"

## ✅ Testar Conexão

### Opção 1: Pelo Terminal

```bash
cd utils
python zebra_printer.py
```

Isso irá:
- Listar todas as impressoras disponíveis
- Verificar se a Zebra ZD230 está conectada
- Perguntar se deseja imprimir uma etiqueta de teste

### Opção 2: Pela Interface Gráfica

1. Abra o aplicativo: `python app.py`
2. Menu > **Impressão** > **Status da Impressora**
3. Verifique se a impressora está listada
4. Menu > **Impressão** > **Teste de Impressão**

## 🎯 Como Usar

### Impressão de Pulseira Individual

1. Importe um CSV com dados dos pacientes
2. Navegue até a pulseira desejada
3. **Menu** > **Impressão** > **Imprimir Pulseira Atual**

OU

1. Na **Sidebar** esquerda, clique em **"🖨️ Imprimir Atual"**

### Impressão em Lote

1. Importe um CSV com dados dos pacientes
2. **Menu** > **Impressão** > **Imprimir Todas as Pulseiras**
3. Confirme a impressão
4. Aguarde o processamento

### Configurar Impressora

1. **Menu** > **Impressão** > **Configurar Impressora**
2. Selecione sua impressora na lista
3. Clique em **"Testar e Salvar"**

## 🔧 Troubleshooting

### ❌ "Impressora não encontrada"

**Causa:** Nome da impressora não corresponde

**Solução:**
1. Abra "Dispositivos e Impressoras"
2. Anote o nome exato
3. Configure em: Menu > Impressão > Configurar Impressora

### ❌ "Módulo win32print não encontrado"

**Causa:** Dependência não instalada

**Solução:**
```bash
pip install pywin32
```

### ❌ "Impressora não imprime"

**Possíveis causas:**
- Impressora desligada
- Sem papel/etiquetas
- Configuração incorreta

**Solução:**
1. Verifique se a impressora está ligada
2. Verifique se há etiquetas
3. Faça um teste direto pela impressora (botão físico)
4. Execute: Menu > Impressão > Teste de Impressão

### ❌ "Layout incorreto na etiqueta"

**Causa:** Tamanho da etiqueta diferente

**Solução:**
Edite o arquivo `utils/zebra_printer.py` e ajuste as posições na função `generate_bracelet_zpl()`.

## 📋 Checklist de Verificação

Antes de usar a impressão, verifique:

- [ ] Driver Zebra instalado
- [ ] Impressora conectada via USB
- [ ] Impressora aparece em "Dispositivos e Impressoras"
- [ ] Nome da impressora anotado
- [ ] pywin32 instalado (`pip install pywin32`)
- [ ] Aplicativo abre sem erros
- [ ] Status da impressora mostra "Conectada"
- [ ] Teste de impressão funcionou

## 🎉 Pronto!

Sua impressora Zebra ZD230 está configurada e pronta para uso!

Para dúvidas ou problemas, consulte o arquivo **IMPRESSAO_ZEBRA_README.md** para documentação completa.
