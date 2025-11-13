# 📝 Módulo de Formulário de Atendimento

## Descrição

O módulo `AtendimentoForm` substitui a funcionalidade de importação de CSV por um formulário interativo para captura de dados de pacientes. Os dados capturados são automaticamente salvos em um arquivo CSV mantendo compatibilidade com o resto do sistema.

## Arquivos Envolvidos

- `ui/atendimento_form.py` - Classe principal do formulário
- `app.py` - Integração com a aplicação principal

## Características

### ✨ Formulário Interativo
- Campos com validação em tempo real
- Placeholders inteligentes
- Indicação visual de campos obrigatórios (*)
- Suporte a diferentes tipos de entrada (text, entry, combobox)

### ✅ Validações
- Validação de campos obrigatórios
- Validação de formato de datas (DD/MM/AAAA)
- Validação de formato de hora (HH:MM)
- Mensagens de erro amigáveis

### 💾 Armazenamento
- Salva automaticamente em `data/pacientes.csv`
- Cria arquivo CSV com cabeçalho se não existir
- Compatível com formato existente de importação

## Campos do Formulário

| Campo | Obrigatório | Tipo | Formato |
|-------|-------------|------|---------|
| Número da carteirinha | ✓ | Texto | Livre |
| Nome do paciente | ✓ | Texto | Livre |
| Data de nascimento | ✓ | Data | DD/MM/AAAA |
| Nome da mãe | ✓ | Texto | Livre |
| Convênio | ✓ | Texto | Livre |
| Médico responsável | ✓ | Texto | Livre |
| Sexo | ✓ | Seleção | Masculino/Feminino/Outro |
| Data de admissão | ✓ | Data | DD/MM/AAAA |
| Hora de admissão | ✓ | Hora | HH:MM |
| Observação | ✗ | Texto longo | Livre |

## Como Usar

### Na Aplicação Principal

```python
from ui import AtendimentoForm

# Inicializar
atendimento = AtendimentoForm(root, diretorio_dados='data')

# Abrir formulário
atendimento.abrir_formulario()

# Obter dados
dados = atendimento.obter_dados_csv()

# Exportar
atendimento.exportar_csv('caminho/destino.csv')
```

### Fluxo de Uso

1. Usuário clica em "🏥 Iniciar Atendimento"
2. Formulário abre em janela modal
3. Usuário preenche os campos
4. Sistema valida dados
5. Se válido, salva em CSV
6. Exibe mensagem de sucesso
7. Carrega dados automaticamente

## Estrutura de Dados

O arquivo `data/pacientes.csv` mantém a seguinte estrutura:

```csv
Número da carteirinha,Nome do paciente,Data de nascimento,Nome da mãe,Convênio,Médico responsável,Sexo,Data de admissão,Hora de admissão,Observação
12345,João Silva,15/03/1990,Maria Silva,UNIMED,Dr. Carlos,Masculino,11/11/2025,14:30,Paciente com histórico de alergia
```

## Métodos Disponíveis

### `abrir_formulario()`
Abre a janela modal do formulário

```python
atendimento.abrir_formulario()
```

### `obter_dados_csv()`
Retorna lista com todos os pacientes registrados

```python
dados = atendimento.obter_dados_csv()
# Retorna: [{'Número da carteirinha': '12345', ...}, ...]
```

### `exportar_csv(destino: str = None)`
Exporta dados para arquivo CSV

```python
# Com diálogo de seleção
atendimento.exportar_csv()

# Com caminho específico
atendimento.exportar_csv('export/pacientes_backup.csv')
```

## Validações e Tratamento de Erros

### Validações Implementadas

1. **Campos Obrigatórios**
   - Verifica se todos os campos marcados com * estão preenchidos
   - Ignora placeholders

2. **Formato de Datas**
   - Espera DD/MM/AAAA
   - Valida se é uma data válida

3. **Formato de Hora**
   - Espera HH:MM (24h)
   - Valida se é uma hora válida

4. **Arquivo CSV**
   - Cria automaticamente se não existir
   - Cria diretório `data/` se não existir

## Mensagens de Feedback

| Situação | Mensagem |
|----------|----------|
| Sucesso | "Atendimento iniciado com sucesso!" |
| Campo vazio | "Preencha o campo: [nome do campo]" |
| Data inválida | "Formato de data/hora inválido..." |
| Erro arquivo | "Erro ao salvar atendimento..." |
| Exportação OK | "Dados exportados para: [caminho]" |

## Arquitetura

```
AtendimentoForm
├── __init__(parent_root, diretorio_dados)
├── abrir_formulario()
├── _criar_campos()
├── _validar_campos()
├── _validar_datas()
├── _coletar_dados()
├── _salvar_atendimento()
├── _gerar_csv()
├── _limpar_campos()
├── obter_dados_csv()
└── exportar_csv()
```

## Integração com app.py

```python
# No __init__ da PulseiraApp
self.atendimento_form = AtendimentoForm(root, diretorio_dados='data')

# Botão na interface
self.btn_iniciar_atendimento = tb.Button(
    ctrl_frame, 
    text='🏥 Iniciar Atendimento', 
    command=self.iniciar_atendimento,
    bootstyle='success'
)

# Método para chamar
def iniciar_atendimento(self):
    self.atendimento_form.abrir_formulario()
    self.root.after(500, self._carrega_dados_atendimento)

def _carrega_dados_atendimento(self):
    dados = self.atendimento_form.obter_dados_csv()
    if dados:
        self.patients = dados
        self.status_var.set(f'✓ {len(dados)} paciente(s) carregado(s)')
        self.update_preview()
```

## Exemplo de Uso Completo

```python
import ttkbootstrap as tb
from ui import AtendimentoForm

root = tb.Window(themename="darkly")

# Criar formulário
form = AtendimentoForm(root)

# Botão para abrir
def abrir():
    form.abrir_formulario()

btn = tb.Button(root, text="Abrir Formulário", command=abrir)
btn.pack()

root.mainloop()
```

## Benefícios

✅ **Interface Amigável** - Formulário intuitivo e responsivo  
✅ **Validação Automática** - Evita dados inválidos  
✅ **Compatibilidade** - Mantém formato de CSV existente  
✅ **Facilidade de Uso** - Não requer importação de arquivo  
✅ **Segurança** - Validações em cliente  
✅ **Escalabilidade** - Fácil adicionar novos campos  

## Futuras Melhorias

- [ ] Integração com banco de dados
- [ ] Busca e edição de pacientes existentes
- [ ] Impressão de etiquetas direto
- [ ] Sincronização em nuvem
- [ ] Backup automático
- [ ] Histórico de atendimentos

---

**Status:** ✅ Implementado e Testado  
**Última Atualização:** 11 de Novembro de 2025
