# 📦 Unipulso - Instalador Windows

> Gerador de Pulseiras Hospitalares - Versão 1.0.0

---

## ℹ️ Sobre

**Unipulso** é um sistema completo para geração de pulseiras de identificação hospitalar com:

- ✅ Interface gráfica moderna e intuitiva
- ✅ Importação de dados via CSV
- ✅ QR Code automático com informações do paciente
- ✅ Exportação em PDF e PNG
- ✅ Impressão direta em impressoras Zebra ZD230
- ✅ Editor de layout visual
- ✅ Templates personalizáveis

---

## 💾 Download e Instalação

### Requisitos do Sistema

- **Sistema Operacional**: Windows 10/11 (64-bit)
- **Espaço em Disco**: 100 MB
- **RAM**: 2 GB mínimo
- **Impressora** (opcional): Zebra ZD230 ou compatível

### Download

📥 **[Download Unipulso v1.0.0](https://github.com/seu-usuario/unipulso/releases)**

### Instalação

1. **Execute** o arquivo `Unipulso_Setup_v1.0.0.exe`
2. **Siga** o assistente de instalação
3. **Escolha** o diretório de instalação (padrão: `C:\Program Files\Unipulso`)
4. **Selecione** se deseja criar atalhos (Desktop e/ou Menu Iniciar)
5. **Clique** em "Instalar"
6. **Pronto!** O Unipulso estará disponível no Menu Iniciar

⏱️ **Tempo de instalação**: ~1 minuto

---

## 🚀 Início Rápido

### 1. Executar o Aplicativo

- **Menu Iniciar**: Procure por "Unipulso"
- **Desktop**: Clique duplo no atalho (se criado)

### 2. Importar Dados de Pacientes

1. Prepare um arquivo **CSV** com os dados dos pacientes
2. No aplicativo, clique em **📁 Arquivo → Importar CSV**
3. Selecione seu arquivo CSV
4. Confirme o mapeamento de colunas

**Formato do CSV esperado**:

```csv
nome,data_nascimento,mae,pai,responsavel,prontuario,leito,observacao
João Silva,15/01/1980,Maria Silva,José Silva,,12345,101A,Alergia a penicilina
```

### 3. Visualizar e Editar

- Use os botões **◀ Anterior** e **Próximo ▶** para navegar entre pacientes
- Edite informações diretamente nos campos
- Veja a pré-visualização em tempo real

### 4. Exportar ou Imprimir

**Exportar PDF/PNG**:
- Vá para a aba **💾 Exportação**
- Escolha formato (PDF ou PNG)
- Clique em **Exportar Atual** ou **Exportar Todos**

**Imprimir (Zebra)**:
- Vá para a aba **🖨️ Impressão**
- Configure a impressora
- Clique em **Imprimir Atual** ou **Imprimir Todos**

---

## 📋 Recursos Principais

### Interface Moderna

- Design limpo e profissional com **ttkbootstrap**
- Organização em abas para fácil navegação
- Sidebar com informações do projeto
- Menu de acesso rápido

### Importação de Dados

- Suporte a arquivos **CSV**
- Mapeamento automático de colunas
- Validação de dados
- Importação em lote

### Geração de Pulseiras

- **QR Code** com informações completas
- Layout personalizado (11cm × 2.5cm)
- Fontes do sistema disponíveis
- Rotação e alinhamento de elementos

### Exportação

- **PDF**: Documento com todas as pulseiras
- **PNG**: Imagens individuais de alta qualidade (300 DPI)
- Organização automática em pastas

### Impressão Zebra

- Impressão direta via **protocolo ZPL**
- Suporte a **Zebra ZD230** (USB)
- Teste de conexão
- Status em tempo real

---

## 🛠️ Configuração da Impressora Zebra

### Conectar Impressora

1. Conecte a **Zebra ZD230** via USB
2. Instale os drivers da impressora (se solicitado)
3. Configure como impressora padrão do Windows

### Configurar no Unipulso

1. Vá em **🖨️ Impressão → ⚙️ Configurar Impressora**
2. Digite o nome exato da impressora (ex: "ZDesigner ZD230-203dpi ZPL")
3. Clique em **Testar Conexão**
4. Se OK, clique em **Salvar**

**Dica**: Para ver o nome exato da impressora, vá em:
- **Configurações do Windows** → **Dispositivos** → **Impressoras e Scanners**

---

## 📚 Documentação Adicional

Após a instalação, consulte os arquivos na pasta do programa:

- **README.md**: Visão geral completa
- **GUIA_CSV.md**: Detalhes sobre formato CSV
- **LICENSE**: Licença do software

Ou acesse online: https://github.com/seu-usuario/unipulso

---

## ❓ Perguntas Frequentes

### O aplicativo precisa de internet?

**Não**. O Unipulso funciona completamente offline.

### Posso usar sem impressora Zebra?

**Sim**. Você pode exportar para PDF/PNG e imprimir em qualquer impressora comum.

### O arquivo CSV precisa ter todas as colunas?

**Não**. Colunas vazias são permitidas. Apenas `nome` é obrigatório.

### Posso personalizar o layout da pulseira?

**Sim**. Use o editor de layout (em desenvolvimento) ou edite os templates JSON.

### Como desinstalar?

- **Painel de Controle** → **Programas** → **Desinstalar um programa** → **Unipulso** → **Desinstalar**

---

## 🐛 Problemas Conhecidos

### Impressora não detectada

**Solução**:
1. Verifique se a impressora está ligada e conectada
2. Instale os drivers oficiais da Zebra
3. Teste imprimir algo pelo Bloco de Notas do Windows primeiro

### Erro ao importar CSV

**Solução**:
1. Verifique se o arquivo está no formato CSV correto
2. Use vírgula (`,`) como separador
3. Salve com codificação UTF-8

### Pulseira com caracteres estranhos

**Solução**:
1. O CSV deve estar em UTF-8
2. No Excel: **Salvar Como** → **CSV UTF-8**

---

## 📞 Suporte

- **Issues**: https://github.com/seu-usuario/unipulso/issues
- **Email**: seu-email@exemplo.com
- **Documentação**: https://github.com/seu-usuario/unipulso

---

## 📄 Licença

Este software é distribuído sob a licença especificada no arquivo LICENSE.

---

## 🙏 Créditos

Desenvolvido por **Victor Hugo Azambuja**

Tecnologias utilizadas:
- Python 3.14
- ttkbootstrap (GUI)
- Pillow (processamento de imagem)
- ReportLab (geração de PDF)
- PyInstaller (empacotamento)
- Inno Setup (instalador)

---

**Versão**: 1.0.0  
**Data**: 12/11/2025
