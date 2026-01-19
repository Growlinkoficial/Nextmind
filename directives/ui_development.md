---
priority: medium
domain: ui_development
dependencies: []
conflicts_with: []
last_updated: 2026-01-19
---

# Diretiva: Desenvolvimento da Interface (UI)

## Objetivo
Desenvolver e manter a interface gráfica do NextMind utilizando Electron, React, TypeScript e TailwindCSS, garantindo uma experiência "Power User" fluida e responsiva.

## Stack Tecnológico
- **Runtime**: Electron (versão mais recente estável)
- **Frontend Framework**: React 18+
- **Linguagem**: TypeScript (Strict Mode)
- **Build Tool**: Vite
- **Estilização**: TailwindCSS + shadcn/ui
- **Ícones**: Lucide React

## Estrutura de Diretórios (`ui/`)
```
ui/
├── electron/           # Código do processo principal (Main Process)
│   ├── main.ts        # Entry point, gerenciamento de janelas
│   └── preload.ts     # ContextBridge, exposição de APIs seguras
├── src/               # Código do processo de renderização (Renderer)
│   ├── components/    # Componentes React reutilizáveis (shadcn)
│   ├── layouts/       # Layouts de página (Sidebar, Main)
│   ├── pages/         # Componentes de página (rotas)
│   ├── hooks/         # Custom React Hooks
│   ├── lib/          # Utilitários e configurações (utils.ts)
│   ├── types/        # Definições de tipos TypeScript globais
│   ├── App.tsx       # Componente raiz
│   └── main.tsx      # Entry point do React
└── ...configs         # (vite.config.ts, tailwind.config.js, etc.)
```

## Padrões de Desenvolvimento

### 1. Componentes
- Use **Functional Components** com Hooks.
- Priorize a composição de componentes do **shadcn/ui**.
- Nomeie arquivos em `PascalCase.tsx`.
- Coloque componentes complexos em pastas próprias com `index.ts`.

### 2. Estilização
- Use classes utilitárias do **TailwindCSS** para a maioria dos estilos.
- Utilize `clsx` e `tailwind-merge` (via `cn()` helper) para classes condicionais.
- Mantenha o arquivo `index.css` apenas para diretivas globais e variáveis CSS (temas).

### 3. Gerenciamento de Estado
- Use **React Context** ou **Zustand** para estado global leve.
- Evite Prop Drilling excessivo.
- Mantenha o estado da UI (ex: abas abertas, sidebar colapsada) persistente quando possível via `localStorage`.

### 4. Performance
- Implemente **Virtualization** para listas longas de mensagens (milhares de itens).
- Utilize `React.memo` e `useMemo` criteriosamente para evitar re-renderizações desnecessárias.
- Carregamento "Lazy" de rotas ou componentes pesados.

## Workflow
1. **Instalação**: `npm install` na pasta `ui/`.
2. **Desenvolvimento**: `npm run dev` para iniciar o servidor Vite e a janela Electron com Hot Module Replacement (HMR).
3. **Build**: `npm run build` para gerar os arquivos de produção em `dist/` e `dist-electron/`.
4. **Linting**: Execute `npm run lint` antes de commitar.

## Critérios de Aceite
- Interface deve carregar em < 200ms.
- Responsividade ao redimensionar a janela.
- Tema escuro/claro funcionando corretamente (preferência do sistema ou manual).
- Sem erros de TypeScript (`noImplicitAny`).
- Acessibilidade básica (navegação por teclado).

## Edge Cases
- **Redimensionamento**: Sidebar deve ter largura mínima e máxima.
- **Falha no Backend**: UI deve exibir estado de erro amigável se o processo Python não responder.
- **Contexto Perdido**: Recarregamento da janela (F5) deve restaurar o estado anterior.
