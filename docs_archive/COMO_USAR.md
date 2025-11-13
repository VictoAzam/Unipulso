# 🚀 COMO USAR - RESUMIDO

## 1️⃣ ABRIR A APP

Abra o PowerShell e digite:

```
cd "c:\Users\Victor Hugo Azambuja\Desktop\Unipulso-3-\Unipulso"
python app.py
```

Uma janela vai abrir com botões no topo.

---

## 2️⃣ INICIAR ATENDIMENTO (OPÇÃO RECOMENDADA)

**Clique no botão verde "🏥 Iniciar Atendimento"**

Uma janela de formulário abrirá. Preencha os dados:

```
Número da carteirinha: 12345678
Nome do paciente:      João Silva
Data de nascimento:    15/03/1985
Nome da mãe:           Maria Silva
Convênio:              Unimed
Médico responsável:    Dr. Carlos
Sexo:                  Masculino
Data de admissão:      (automático!)
Hora de admissão:      (automático!)
Observação:            Alergia a penicilina (opcional)
```

Clique em **"💾 Salvar"**

Pronto! A pulseira está criada. ✅

---

## 3️⃣ VISUALIZAR A PULSEIRA

Após salvar, você verá a pulseira na tela:

```
[QR CODE]  João Silva (CENTRALIZADO)
           Carteirinha: 12345678

           Nasc: 15/03 │ Med: Dr. C... │ Hora: 14:30
           Mãe: Maria  │ Sex: Masc     │
           Conv: Unimed│ Adm: 11/11    │

           Observação: Alergia a penicilina
```

---

## 4️⃣ EXPORTAR PARA IMPRIMIR

**Opção A: PNG (para ver a imagem antes de imprimir)**

Clique em **"⬇️ Exportar PNG"**

- Escolha onde salvar
- A imagem será salva como `pulseira_1.png`
- Abra a imagem para visualizar

**Opção B: PDF (para imprimir direto)**

Clique em **"⬇️ Exportar PDF"**

- Escolha onde salvar
- Abra o PDF e imprima

---

## ✅ DADOS AUTOMATICAMENTE SALVOS

Todos os dados são salvos em: **data/pacientes.csv**

Você pode:
- ✅ Abrir o arquivo em Excel para editar
- ✅ Importar novamente se precisar de mudanças
- ✅ Fazer backup dos dados

---

## 🎨 MAIS OPÇÕES NA TELA PRINCIPAL

| Botão | O que faz |
|-------|-----------|
| 🏥 Iniciar Atendimento | Adicionar nova paciente (PRINCIPAL) |
| 📥 Importar CSV | Carregar dados de um arquivo |
| ⬇️ Exportar PNG | Salvar como imagem |
| ⬇️ Exportar PDF | Salvar como documento PDF |
| 🎨 Editor de Layout | Customizar cores e posições |
| 💾 Salvar Preferências | Guardar suas customizações |

---

## 📝 CAMPOS DO FORMULÁRIO

### Obrigatórios (devem ser preenchidos):
- ✅ Número da carteirinha
- ✅ Nome do paciente
- ✅ Data de nascimento (DD/MM/AAAA)
- ✅ Nome da mãe
- ✅ Convênio
- ✅ Médico responsável
- ✅ Sexo
- ✅ Data de admissão (automático!)
- ✅ Hora de admissão (automático!)

### Opcional:
- ❓ Observação

---

## ⚡ EXEMPLO COMPLETO

### Você está aqui:
1. ✅ Abrir app.py
2. ✅ Clicar "🏥 Iniciar Atendimento"
3. ✅ Preencher: João Silva, carteirinha 12345678, etc
4. ✅ Clicar "💾 Salvar"
5. ✅ Ver pulseira na tela
6. ✅ Clicar "⬇️ Exportar PNG"
7. ✅ Salvar imagem
8. ✅ Abrir imagem e imprimir na impressora térmica

**Pronto!** 🎉

---

## 🆘 PROBLEMAS?

**A janela não abre?**
- Certifique-se que Python 3.8+ está instalado
- Execute: `python --version`

**Mensagem de erro ao salvar?**
- Verifique se a pasta `data/` existe
- Se não existir, será criada automaticamente

**Campos desaparecendo?**
- Ao clicar em um campo, o placeholder (texto cinzento) desaparece
- Comece a digitar normalmente

---

**Tudo pronto! Comece a criar pulseiras agora!** 🚀
