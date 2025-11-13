# ✅ Checklist de Build e Release - Unipulso

> Use este checklist antes de criar e distribuir o instalador

---

## 📋 Pré-Build (Antes de Compilar)

### Código

- [ ] Todos os testes passando (`pytest` ou teste manual)
- [ ] Sem erros no console ao executar `python app.py`
- [ ] Todas as funcionalidades testadas manualmente
- [ ] Código commitado no Git (se usar controle de versão)

### Dependências

- [ ] `requirements.txt` atualizado
- [ ] PyInstaller instalado (`pip install pyinstaller`)
- [ ] Todas as bibliotecas instaladas e funcionando

### Recursos

- [ ] Logo existe em `logo/` (se houver)
- [ ] Fontes padrão em `fonte padrao/` (se houver)
- [ ] Templates em `templates/` (se houver)
- [ ] Arquivo `LICENSE` presente

### Ícone (Opcional mas Recomendado)

- [ ] Imagem de logo preparada (256x256 px ou maior)
- [ ] Executado `python create_icon.py` (se aplicável)
- [ ] Arquivo `logo/icon.ico` criado

### Versão

- [ ] Versão atualizada em `installer.iss`:
  ```ini
  #define MyAppVersion "1.0.0"  ← Atualizar aqui
  ```
- [ ] Informações do publisher atualizadas (nome, URL, email)

---

## 🔨 Build do Executável

### PyInstaller

- [ ] Executado `python build_exe.py` OU `build_all.bat`
- [ ] Build concluído sem erros
- [ ] Arquivo `dist/Unipulso.exe` criado
- [ ] Tamanho do executável razoável (50-100 MB)

### Teste do Executável

Execute `dist/Unipulso.exe` e verifique:

- [ ] Aplicativo abre sem erros
- [ ] Interface carrega corretamente (sem elementos faltando)
- [ ] Sidebar mostra informações
- [ ] Menu funciona
- [ ] Navegação entre abas funciona

### Funcionalidades Críticas

- [ ] **Importar CSV** funciona
- [ ] **Pré-visualização** renderiza corretamente
- [ ] **Exportar PDF** funciona
- [ ] **Exportar PNG** funciona
- [ ] **Impressão Zebra** detecta impressora (se disponível)
- [ ] **QR Code** é gerado corretamente
- [ ] **Fontes** carregam (incluindo fonte padrão)
- [ ] **Logo** aparece (se configurado)

### Teste de Recursos

- [ ] Logo aparece na pulseira (se configurado)
- [ ] Fonte padrão funciona
- [ ] Templates são carregados
- [ ] Preferências são salvas e carregadas

---

## 📦 Build do Instalador

### Pré-requisitos

- [ ] Inno Setup instalado
- [ ] Executável já criado (`dist/Unipulso.exe` existe)

### Criação

- [ ] Executado `python build_installer.py` OU `build_all.bat`
- [ ] Build do instalador concluído sem erros
- [ ] Arquivo criado em `installer_output/Unipulso_Setup_v1.0.0.exe`
- [ ] Tamanho do instalador razoável (40-80 MB)

---

## 🧪 Teste do Instalador (CRÍTICO!)

### Instalação

- [ ] Executado `Unipulso_Setup_v1.0.0.exe`
- [ ] Assistente de instalação aparece em português
- [ ] Instalação em `C:\Program Files\Unipulso` (ou pasta escolhida)
- [ ] Instalação concluída sem erros
- [ ] Atalho criado no Menu Iniciar
- [ ] Atalho criado no Desktop (se selecionado)

### Execução Pós-Instalação

- [ ] Aplicativo abre pelo Menu Iniciar
- [ ] Aplicativo abre pelo Desktop (se atalho criado)
- [ ] Sem erros de "arquivo não encontrado"
- [ ] Todas funcionalidades funcionam (mesmo teste do executável)

### Verificação de Arquivos

Verifique se os arquivos foram copiados:

- [ ] `C:\Program Files\Unipulso\Unipulso.exe` existe
- [ ] `C:\Program Files\Unipulso\logo\` existe (se aplicável)
- [ ] `C:\Program Files\Unipulso\fonte padrao\` existe (se aplicável)
- [ ] `C:\Program Files\Unipulso\templates\` existe
- [ ] `C:\Program Files\Unipulso\README.md` existe
- [ ] `C:\Program Files\Unipulso\LICENSE` existe

### Teste de Escrita

- [ ] Consegue importar CSV
- [ ] Consegue salvar preferências
- [ ] Consegue exportar PDF/PNG (pasta `output/` criada)
- [ ] Consegue salvar templates

### Registro no Sistema

- [ ] Aparece em "Painel de Controle → Programas e Recursos"
- [ ] Nome correto: "Unipulso"
- [ ] Versão correta (ex: 1.0.0)
- [ ] Publisher correto

### Desinstalação

- [ ] Desinstalação pelo Painel de Controle funciona
- [ ] Todos os arquivos removidos
- [ ] Atalhos removidos (Menu Iniciar + Desktop)
- [ ] Pasta `C:\Program Files\Unipulso` removida

**⚠️ IMPORTANTE**: Teste em uma máquina limpa se possível (sem Python instalado)

---

## 📄 Documentação

### Arquivos para Distribuição

- [ ] `README_INSTALADOR.md` revisado e atualizado
- [ ] `GUIA_RAPIDO_1_PAGINA.md` revisado
- [ ] Informações de versão corretas em todos os docs
- [ ] Links funcionando (se houver)

### Documentação do Desenvolvedor

- [ ] `GUIA_INSTALADOR.md` atualizado (se mudanças no processo)
- [ ] `BUILD_SYSTEM_INDEX.md` reflete estrutura atual
- [ ] Este checklist atualizado (se novos itens)

---

## 🚀 Preparação para Release

### GitHub (se usar)

- [ ] Código commitado e pushado
- [ ] Tag de versão criada (`git tag v1.0.0`)
- [ ] Release criada no GitHub
- [ ] Changelog escrito (o que mudou nesta versão)

### Arquivos para Upload

- [ ] `Unipulso_Setup_v1.0.0.exe` (OBRIGATÓRIO)
- [ ] `README_INSTALADOR.md` (RECOMENDADO)
- [ ] `GUIA_RAPIDO_1_PAGINA.md` (RECOMENDADO)
- [ ] `LICENSE` (se open source)

### Comunicação

- [ ] Notas de release escritas
- [ ] Requisitos de sistema documentados
- [ ] Instruções de instalação claras
- [ ] Link de download funcional

---

## 🔒 Segurança (Opcional mas Importante)

### Antivírus

- [ ] Executável testado com Windows Defender
- [ ] Sem falsos positivos de antivírus
- [ ] (Futuro) Assinatura digital considerada

### Backup

- [ ] Código-fonte backupeado
- [ ] Instalador backupeado em local seguro
- [ ] Documentação backupeada

---

## 📊 Qualidade Final

### Performance

- [ ] Aplicativo abre em < 5 segundos
- [ ] Interface responde rapidamente
- [ ] Exportação de PDF rápida (< 10s para 100 pulseiras)
- [ ] Importação de CSV rápida (< 5s para 1000 registros)

### Usabilidade

- [ ] Interface intuitiva
- [ ] Mensagens de erro claras
- [ ] Feedback visual para ações
- [ ] Sem travamentos ou crashes

### Compatibilidade

- [ ] Testado no Windows 10
- [ ] Testado no Windows 11 (se possível)
- [ ] Funciona sem privilégios de administrador
- [ ] Compatível com impressora Zebra ZD230 (se disponível)

---

## ✅ Aprovação Final

### Checklist Mestre

- [ ] **Código**: Tudo funcionando
- [ ] **Build**: Executável criado e testado
- [ ] **Instalador**: Criado e testado em máquina limpa
- [ ] **Documentação**: Completa e atualizada
- [ ] **Testes**: Todos passando
- [ ] **Desinstalação**: Testada e funcional
- [ ] **Release**: Preparado e documentado

### Assinatura de Aprovação

```
Data: ____/____/________
Versão: ______________
Testado por: _______________________
Status: ☐ Aprovado  ☐ Pendente  ☐ Reprovado

Observações:
_____________________________________________
_____________________________________________
_____________________________________________
```

---

## 🎉 Pós-Release

### Após Distribuição

- [ ] Monitorar feedback de usuários
- [ ] Documentar bugs reportados
- [ ] Planejar próxima versão
- [ ] Atualizar roadmap

### Manutenção

- [ ] Issues do GitHub respondidas (se aplicável)
- [ ] Perguntas de usuários respondidas
- [ ] Patches de segurança aplicados (se necessário)

---

**Use este checklist para garantir qualidade e evitar problemas na distribuição!**

**Última atualização**: 12/11/2025  
**Versão do checklist**: 1.0
