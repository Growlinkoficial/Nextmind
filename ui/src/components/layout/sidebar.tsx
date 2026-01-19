import { useAppStore } from "@/store/use-app-store"
import { cn } from "@/lib/utils"
import {
    FolderIcon,
    MessageSquareIcon,
    PlusIcon,
    Settings2Icon,
    ChevronLeftIcon,
    ChevronRightIcon
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Separator } from "@/components/ui/separator"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

export function Sidebar() {
    const { isSidebarOpen, toggleSidebar, selectedId, setSelectedId } = useAppStore()

    const projects = [
        { id: '1', name: 'Jurídico', description: 'Assuntos legais' },
        { id: '2', name: 'Desenvolvimento', description: 'Coding tasks' },
    ]

    const recentChats = [
        { id: 'c1', title: 'Refatoração do Core', time: '14:20' },
        { id: 'c2', title: 'Ideias de Produto', time: 'Ontem' },
    ]

    return (
        <div
            className={cn(
                "relative h-screen bg-card/30 backdrop-blur-xl border-r border-white/5 transition-all duration-300 flex flex-col",
                isSidebarOpen ? "w-64" : "w-16"
            )}
        >
            {/* Header */}
            <div className="p-4 flex items-center justify-between h-16">
                {isSidebarOpen && (
                    <span className="font-bold text-transparent bg-clip-text bg-gradient-to-r from-white to-white/60 truncate">
                        NextMind
                    </span>
                )}
                <Button
                    variant="ghost"
                    size="icon"
                    onClick={toggleSidebar}
                    className="hover:bg-white/5 ml-auto"
                >
                    {isSidebarOpen ? <ChevronLeftIcon size={18} /> : <ChevronRightIcon size={18} />}
                </Button>
            </div>

            <Separator className="bg-white/5" />

            {/* Main Action */}
            <div className="p-2 mt-2">
                <TooltipProvider>
                    <Tooltip delayDuration={0}>
                        <TooltipTrigger asChild>
                            <Button
                                className={cn(
                                    "w-full bg-white/5 hover:bg-white/10 text-white border-white/5 justify-start",
                                    !isSidebarOpen && "justify-center p-0"
                                )}
                                variant="outline"
                            >
                                <PlusIcon size={18} className={cn(isSidebarOpen && "mr-2")} />
                                {isSidebarOpen && <span>Novo Chat</span>}
                            </Button>
                        </TooltipTrigger>
                        {!isSidebarOpen && <TooltipContent side="right">Novo Chat</TooltipContent>}
                    </Tooltip>
                </TooltipProvider>
            </div>

            {/* Content */}
            <ScrollArea className="flex-1 px-2">
                <div className="mt-4 space-y-4">
                    {/* Projects Section */}
                    <div>
                        {isSidebarOpen && <p className="px-2 mb-2 text-xs font-semibold text-muted-foreground uppercase tracking-wider">Projetos</p>}
                        <div className="space-y-1">
                            {projects.map((p) => (
                                <SidebarItem
                                    key={p.id}
                                    icon={<FolderIcon size={18} />}
                                    label={p.name}
                                    isOpen={isSidebarOpen}
                                    isSelected={selectedId === p.id}
                                    onClick={() => setSelectedId(p.id)}
                                />
                            ))}
                        </div>
                    </div>

                    <Separator className="bg-white/5 mx-2" />

                    {/* Recent Chats Section */}
                    <div>
                        {isSidebarOpen && <p className="px-2 mb-2 text-xs font-semibold text-muted-foreground uppercase tracking-wider">Recentes</p>}
                        <div className="space-y-1">
                            {recentChats.map((c) => (
                                <SidebarItem
                                    key={c.id}
                                    icon={<MessageSquareIcon size={18} />}
                                    label={c.title}
                                    isOpen={isSidebarOpen}
                                    isSelected={selectedId === c.id}
                                    onClick={() => setSelectedId(c.id)}
                                />
                            ))}
                        </div>
                    </div>
                </div>
            </ScrollArea>

            {/* Footer */}
            <div className="p-2 border-t border-white/5">
                <SidebarItem
                    icon={<Settings2Icon size={18} />}
                    label="Configurações"
                    isOpen={isSidebarOpen}
                    onClick={() => { }}
                />
            </div>
        </div>
    )
}

interface SidebarItemProps {
    icon: React.ReactNode
    label: string
    isOpen: boolean
    isSelected?: boolean
    onClick: () => void
}

function SidebarItem({ icon, label, isOpen, isSelected, onClick }: SidebarItemProps) {
    return (
        <TooltipProvider>
            <Tooltip delayDuration={0}>
                <TooltipTrigger asChild>
                    <Button
                        variant="ghost"
                        onClick={onClick}
                        className={cn(
                            "w-full justify-start hover:bg-white/5 transition-colors",
                            isSelected ? "bg-white/10 text-white" : "text-muted-foreground",
                            !isOpen && "justify-center px-0"
                        )}
                    >
                        <div className={cn(isOpen && "mr-3")}>{icon}</div>
                        {isOpen && <span className="truncate text-sm">{label}</span>}
                    </Button>
                </TooltipTrigger>
                {!isOpen && <TooltipContent side="right">{label}</TooltipContent>}
            </Tooltip>
        </TooltipProvider>
    )
}
