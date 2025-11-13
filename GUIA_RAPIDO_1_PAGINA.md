# 🚀 Unipulso - Guia Rápido (1 Página)

## 📦 Instalação
1. Execute `Unipulso_Setup_v1.0.0.exe`
2. Siga o assistente → "Avançar" → "Instalar"
3. Pronto! Procure "Unipulso" no Menu Iniciar

---

## 💡 Uso Básico (3 Passos)

### Passo 1: Importar Dados
```
Menu: 📁 Arquivo → Importar CSV
```
- Selecione seu arquivo `.csv` com dados dos pacientes
- Formato esperado:
  ```
  nome,data_nascimento,mae,prontuario,leito
  João Silva,15/01/1980,Maria Silva,12345,101A
  ```

### Passo 2: Visualizar
- Use **◀ Anterior** | **Próximo ▶** para navegar
- Veja pré-visualização em tempo real
- Edite campos se necessário

### Passo 3: Exportar/Imprimir
**Exportar PDF/PNG:**
```
Aba: 💾 Exportação → Exportar Atual (ou Exportar Todos)
```

**Imprimir (Zebra ZD230):**
```
Aba: 🖨️ Impressão → Imprimir Atual (ou Imprimir Todos)
```

---

## 🖨️ Configurar Impressora Zebra (Primeira Vez)

1. **Conecte** a Zebra ZD230 via USB
2. **No Unipulso**: Menu `🖨️ Impressão → ⚙️ Configurar`
3. **Digite** nome da impressora (ex: `ZDesigner ZD230-203dpi ZPL`)
   - *Dica: Veja o nome em* **Configurações do Windows → Impressoras**
4. **Teste** → Salvou? OK!

---

## 📋 Formato CSV Aceito

**Colunas suportadas** (apenas `nome` é obrigatório):

| Coluna | Exemplo | Obrigatório? |
|--------|---------|--------------|
| `nome` | João Silva | ✅ Sim |
| `data_nascimento` | 15/01/1980 | ❌ Não |
| `mae` | Maria Silva | ❌ Não |
| `pai` | José Silva | ❌ Não |
| `responsavel` | Ana Costa | ❌ Não |
| `prontuario` | 12345 | ❌ Não |
| `leito` | 101A | ❌ Não |
| `observacao` | Alergia penicilina | ❌ Não |

**Salvando CSV no Excel:**
- `Arquivo → Salvar Como → CSV UTF-8 (delimitado por vírgulas)`

---

## ❓ Problemas Comuns

### ❌ "Erro ao importar CSV"
**Solução**: Salve o Excel como **CSV UTF-8** (não "CSV" normal)

### ❌ "Impressora não encontrada"
**Soluções**:
1. Verifique se está ligada e conectada (USB)
2. Instale drivers Zebra: [zebra.com/drivers](https://www.zebra.com/drivers)
3. Digite nome EXATO da impressora (copie de "Impressoras e Scanners")

### ❌ Caracteres estranhos (�, ã, ç)
**Solução**: CSV deve estar em **UTF-8**
- Excel: `Salvar Como → CSV UTF-8`

---

## 📞 Suporte

- 📧 **Email**: seu-email@exemplo.com
- 📚 **Documentação completa**: Pasta do programa → `README.md`
- 🐛 **Reportar bug**: [GitHub Issues](https://github.com/seu-usuario/unipulso/issues)

---

## 🎯 Atalhos Úteis

| Ação | Como fazer |
|------|------------|
| Importar CSV | `Ctrl+O` ou menu 📁 |
| Exportar PDF | Aba 💾 → Exportar Todos |
| Navegar pacientes | Botões ◀ ▶ |
| Ver fonte/logo atual | Sidebar (painel lateral) |

---

**Versão**: 1.0.0 | **Desenvolvido por**: Victor Hugo Azambuja

*Este é um guia resumido. Para documentação completa, consulte README.md na pasta do programa.*
