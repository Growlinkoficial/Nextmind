---
priority: high
domain: integration
dependencies: [ui_development, database_management]
conflicts_with: []
last_updated: 2026-01-19
---

# Diretiva: Integração IPC (Electron <-> Python)

## Objetivo
Estabelecer um canal de comunicação seguro e eficiente entre a interface Electron (Renderer Process) e o backend Python (Execution Layer), permitindo que a UI execute comandos, consulte o banco de dados e interaja com LLMs.

## Arquitetura de Comunicação

A comunicação segue o padrão **Solicitação-Resposta** assíncrono:

1.  **Renderer (React)** solicita uma ação via `window.api`.
2.  **Main (Electron)** recebe a solicitação via `ipcMain`.
3.  **Main** invoca o script Python apropriado (Execution Layer) via `child_process.spawn` ou chamada HTTP local (futuro).
4.  **Python** processa a requisição e retorna JSON (stdout).
5.  **Main** parseia o resultado e devolve ao Renderer.

## Definição de API (preload.ts)

A API deve ser exposta via `contextBridge` para garantir isolamento de contexto.

```typescript
// Interface TypeScript para a API
interface IElectronAPI {
  // Comandos de Banco de Dados
  getProjects: () => Promise<Project[]>;
  createProject: (data: CreateProjectDTO) => Promise<string>;
  getConversations: (projectId?: string) => Promise<Conversation[]>;
  
  // Comandos de LLM
  sendMessage: (payload: MessagePayload) => Promise<StreamChunk>;
  
  // Sistema
  importData: (source: 'chatgpt' | 'claude', filePath: string) => Promise<ImportStats>;
}

// Exposição
contextBridge.exposeInMainWorld('api', { ... });
```

## Padrões de Implementação

### 1. Invocação de Python (Lado Electron Main)
- Utilize um wrapper reutilizável para chamar scripts Python.
- Passe argumentos como flags CLI ou JSON string via stdin.
- Capture `stdout` para sucesso e `stderr` para logs/erros.
- **Segurança**: Nunca passe strings brutas do usuário diretamente para o shell. Use `args` array do `spawn`.

### 2. Output dos Scripts Python
- Scripts devem imprimir o resultado final em **JSON** no `stdout` como última linha (ou única saída estruturada).
- Logs e debugs devem ir para `stderr` ou para arquivos de log (`.tmp/logs/`), nunca misturados com o JSON de resposta no stdout.

### 3. Tratamento de Erros
- **Python**: Se ocorrer exceção, o script deve sair com código != 0 e imprimir erro no stderr.
- **Electron**: Capturar código de saída. Se != 0, rejeitar a Promise do renderer com a mensagem de erro.
- **React**: Exibir Toast ou Alert amigável ao usuário.

## Exemplo de Fluxo (Importação)

1.  **React**: `const stats = await window.api.importData('chatgpt', path);`
2.  **Electron**:
    ```typescript
    // main.ts
    ipcMain.handle('import-data', async (event, source, path) => {
      const script = source === 'chatgpt' ? 'import_chatgpt.py' : 'import_claude.py';
      return runPythonScript(script, [path]);
    });
    ```
3.  **Python** (`import_chatgpt.py`):
    - Executa a lógica.
    - Usa o `ExecutionLogger`.
    - Imprime JSON no final: `print(json.dumps(stats))`
4.  **Electron**: Parseia JSON e retorna.

## Edge Cases

- **Python não encontrado**: Verificar se o Python está no PATH ou usar caminho configurável no `.env`.
- **Scripts lentos**: Para operações longas (ex: importação grande), considerar enviar eventos de progresso via `mainWindow.webContents.send` em vez de esperar uma única promessa.
- **Encoding**: Garantir que a comunicação `stdin`/`stdout` use UTF-8 para suportar emojis e caracteres especiais.

## Critérios de Aceite
- Tipagem forte (TypeScript) para todos os canais IPC.
- Nenhuma chave de API exposta no Renderer.
- Scripts Python sendo executados com sucesso a partir da UI.
- Erros de Python propagados corretamente para a UI.
