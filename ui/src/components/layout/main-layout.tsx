import { Sidebar } from "./sidebar"

interface MainLayoutProps {
    children: React.ReactNode
}

export function MainLayout({ children }: MainLayoutProps) {
    return (
        <div className="flex h-screen w-full overflow-hidden bg-background">
            <Sidebar />
            <main className="flex-1 relative flex flex-col min-w-0 overflow-hidden">
                {children}
            </main>
        </div>
    )
}
