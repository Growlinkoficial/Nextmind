import { create } from 'zustand'

interface AppState {
    isSidebarOpen: boolean
    selectedId: string | null
    toggleSidebar: () => void
    setSelectedId: (id: string | null) => void
}

export const useAppStore = create<AppState>((set) => ({
    isSidebarOpen: true,
    selectedId: null,
    toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),
    setSelectedId: (id) => set({ selectedId: id }),
}))
