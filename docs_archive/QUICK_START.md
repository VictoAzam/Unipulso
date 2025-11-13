# ⚡ QUICK START - Comece Agora Mesmo!

## 5 Passos Para Criar Sua Primeira Pulseira

### PASSO 1: Iniciar o App
```
1. Abra o PowerShell
2. Digite:
   cd "c:\Users\Victor Hugo Azambuja\Desktop\Unipulso-3-\Unipulso"
   python app.py
3. Aguarde a janela abrir (2-3 segundos)
```

### PASSO 2: Clicar em "Iniciar Atendimento"
```
Você verá uma janela com vários botões no topo
Clique no botão VERDE que diz "🏥 Iniciar Atendimento"
Uma nova janela (formulário) abrirá
```

### PASSO 3: Preencher os Dados
Preencha os campos conforme o exemplo abaixo:

| Campo | Exemplo | Automático? |
|-------|---------|-------------|
| Número da carteirinha | 12345678 | ❌ |
| Nome do paciente | João Silva | ❌ |
| Data de nascimento | 15/03/1985 | ❌ |
| Nome da mãe | Maria Silva | ❌ |
| Convênio | Unimed | ❌ |
| Médico responsável | Dr. Carlos | ❌ |
| Sexo | Masculino (selecione) | ❌ |
| Data de admissão | (deixe em branco) | ✅ Preenchido automaticamente |
| Hora de admissão | (deixe em branco) | ✅ Preenchido automaticamente |
| Observação | Alergia a penicilina | ❌ Opcional |

**Nota**: A Data e Hora de admissão são preenchidas automaticamente quando você abre o formulário!

### PASSO 4: Salvar
Clique no botão **💾 Salvar**

Você verá:
- Uma mensagem: "Atendimento iniciado com sucesso!"
- O formulário vai fechar automaticamente
- A pulseira aparecerá na tela

### PASSO 5: Exportar e Imprimir
Escolha uma opção:

**A) Exportar como PNG (recomendado para testes):**
```
1. Clique no botão "⬇️ Exportar PNG"
2. Escolha uma pasta (ex: Desktop)
3. Clique em "Salvar"
4. A imagem será salva como "pulseira_1.png"
5. Abra a imagem para visualizar
```

**B) Exportar como PDF (para imprimir):**
```
1. Clique no botão "⬇️ Exportar PDF"
2. Escolha uma pasta
3. Clique em "Salvar"
4. Abra o PDF e imprima
```

---

## ✅ Pronto!

Você criou sua primeira pulseira! 🎉

---

## 🎨 Customizações (Avançado)

Se quiser customizar cores, fontes, ou layout:

1. Clique em **🎨 Editor de Layout**
2. Arraste os elementos para repositioná-los
3. Clique em um elemento para editar:
   - Cor
   - Fonte
   - Tamanho
   - Espessura (bold)
4. Clique em **💾 Salvar Layout** para manter as alterações

---

## ⚠️ Problemas Comuns

### "A janela não abre"
- Verifique se Python está instalado: `python --version`
- Certifique-se de estar na pasta correta

### "Erro ao salvar"
- Verifique se você tem permissão de escrita na pasta
- A pasta `data/` deve existir (é criada automaticamente)

### "Campos não estão sendo preenchidos"
- Clique no campo e comece a digitar
- Se vir "DD/MM/AAAA" cinzento, é apenas um placeholder (desaparece ao digitar)

### "A pulseira saiu feita"
- Vá para o Passo 5 e exporte como PNG
- Abra a imagem para verificar
- Se estiver ok, é hora de imprimir!

---

## 📞 Suporte

Todos os dados são salvos em: `data/pacientes.csv`

Você pode editar diretamente no arquivo se necessário (abra com Excel ou Bloco de notas).

---

**Divirta-se! 🚀**
