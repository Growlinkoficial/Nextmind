# NextMind UI

Interface desktop do NextMind construída com Electron + React + TypeScript + Vite.

## 🛠️ Stack Tecnológico

- **Framework Desktop**: Electron 30
- **Frontend**: React 18 + TypeScript
- **Build Tool**: Vite 5
- **Styling**: TailwindCSS + shadcn/ui
- **Icons**: Lucide React

## 📁 Estrutura

```
ui/
├── electron/           # Processo principal do Electron
│   ├── main.ts        # Entry point do Electron
│   └── preload.ts     # Script de preload (bridge)
├── src/               # Frontend React
│   ├── components/    # Componentes React
│   ├── lib/          # Utilitários
│   ├── App.tsx       # Componente principal
│   └── main.tsx      # Entry point React
├── public/           # Assets estáticos
├── dist/             # Build do frontend (Vite)
├── dist-electron/    # Build do Electron
└── release/          # Binários empacotados
```

## 🚀 Desenvolvimento

```bash
# Instalar dependências
npm install

# Modo desenvolvimento (hot reload)
npm run dev

# Build de produção
npm run build

# Lint
npm run lint
```

## 🏗️ Build e Distribuição

O projeto usa `electron-builder` para criar binários distribuíveis:

```bash
npm run build
```

Isso irá:
1. Compilar TypeScript
2. Build do Vite (frontend)
3. Empacotar com electron-builder

Os binários estarão em `release/`.

## 🎨 Design System

Utilizamos **shadcn/ui** para componentes base:
- Componentes configurados em `components.json`
- Estilização com TailwindCSS
- Variantes com `class-variance-authority`

### Adicionar novos componentes shadcn

```bash
npx shadcn-ui@latest add [component-name]
```

## 🔧 Configuração

- **Vite**: `vite.config.ts`
- **TypeScript**: `tsconfig.json`, `tsconfig.node.json`
- **TailwindCSS**: `tailwind.config.js`
- **Electron Builder**: `electron-builder.json5`
- **ESLint**: `.eslintrc.cjs`

## 🔌 IPC (Inter-Process Communication)

A comunicação entre o processo principal (Electron) e o renderer (React) é feita via IPC:

```typescript
// No preload.ts
contextBridge.exposeInMainWorld('api', {
  // Expor APIs seguras
})

// No React
window.api.someMethod()
```

## 📦 Dependências Principais

### Produção
- `react`, `react-dom`: Framework UI
- `@radix-ui/*`: Primitivos de UI (base do shadcn)
- `lucide-react`: Ícones
- `tailwind-merge`, `clsx`: Utilitários CSS

### Desenvolvimento
- `electron`: Runtime desktop
- `vite`: Build tool
- `typescript`: Type safety
- `electron-builder`: Empacotamento

## 🎯 Próximos Passos

- [ ] Implementar sidebar de projetos
- [ ] Componente de chat com Markdown
- [ ] Integração com backend Python (IPC)
- [ ] Gerenciamento de estado (Zustand/Jotai)
- [ ] Temas (dark/light mode)
