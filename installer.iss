; Script Inno Setup para Unipulso
; Cria instalador profissional para Windows

#define MyAppName "Unipulso"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Victor Hugo Azambuja"
#define MyAppURL "https://github.com/seu-usuario/unipulso"
#define MyAppExeName "Unipulso.exe"
#define MyAppDescription "Gerador de Pulseiras Hospitalares"

[Setup]
; Informações básicas
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Diretório de instalação padrão
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}

; Saída do instalador
OutputDir=installer_output
OutputBaseFilename=Unipulso_Setup_v{#MyAppVersion}

; Compressão
Compression=lzma2/max
SolidCompression=yes

; Interface
WizardStyle=modern
SetupIconFile=logo\icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

; Privilégios
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; Arquitetura
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

; Informações de desinstalação
UninstallDisplayName={#MyAppName}
UninstallFilesDir={app}\uninstall

; Licença (opcional)
LicenseFile=LICENSE

; README (opcional - será exibido após instalação)
InfoAfterFile=README.md

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na Área de Trabalho"; GroupDescription: "Atalhos:"; Flags: unchecked
Name: "quicklaunchicon"; Description: "Criar atalho na Barra de Tarefas"; GroupDescription: "Atalhos:"; Flags: unchecked

[Files]
; Executável principal
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; Documentação (se existir)
Source: "dist\README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme skipifsourcedoesntexist
Source: "dist\LICENSE"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist
Source: "dist\GUIA_CSV.md"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist

; Criar pastas de trabalho
[Dirs]
Name: "{app}\output"; Permissions: users-modify
Name: "{app}\templates"; Permissions: users-modify
Name: "{app}\data"; Permissions: users-modify

[Icons]
; Atalho no Menu Iniciar
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Comment: "{#MyAppDescription}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{group}\README"; Filename: "{app}\README.md"

; Atalho na Área de Trabalho (opcional)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Comment: "{#MyAppDescription}"; Tasks: desktopicon

; Atalho na Barra de Tarefas (opcional)
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
; Opção de executar o programa após instalação
Filename: "{app}\{#MyAppExeName}"; Description: "Executar {#MyAppName}"; Flags: nowait postinstall skipifsilent

[Code]
// Mensagem de boas-vindas personalizada
function InitializeSetup(): Boolean;
begin
  Result := True;
  MsgBox('Bem-vindo ao instalador do ' + '{#MyAppName}' + '!' + #13#10#13#10 + 
          'Este assistente irá instalar o {#MyAppDescription} no seu computador.' + #13#10#13#10 +
          'Clique em Avançar para continuar.', 
          mbInformation, MB_OK);
end;

// Mensagem final personalizada
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    MsgBox('Instalação concluída com sucesso!' + #13#10#13#10 + 
           'O {#MyAppName} está pronto para uso.' + #13#10#13#10 +
           'Você pode encontrá-lo no Menu Iniciar ou executá-lo agora.', 
           mbInformation, MB_OK);
  end;
end;

[UninstallDelete]
; Limpar arquivos de preferências e cache ao desinstalar
Type: filesandordirs; Name: "{app}\output"
Type: filesandordirs; Name: "{app}\__pycache__"
Type: files; Name: "{app}\preferences.json"
