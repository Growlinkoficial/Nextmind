import { ScrollArea } from "@/components/ui/scroll-area"
import { Button } from "@/components/ui/button"
import { PlusIcon, SendIcon, SparklesIcon } from "lucide-react"

export function ChatWindow() {
    return (
        <div className="flex flex-col h-full bg-transparent">
            {/* Chat Header */}
            <div className="h-16 border-b border-white/5 flex items-center px-6 justify-between bg-card/10 backdrop-blur-md">
                <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center border border-primary/30">
                        <SparklesIcon size={16} className="text-primary" />
                    </div>
                    <div>
                        <h2 className="text-sm font-semibold text-white">Novo Chat</h2>
                        <p className="text-[10px] text-muted-foreground uppercase tracking-widest">Sem Projeto</p>
                    </div>
                </div>
            </div>

            {/* Messages area */}
            <ScrollArea className="flex-1 p-6">
                <div className="max-w-3xl mx-auto space-y-6">
                    <div className="flex flex-col items-center justify-center py-20 text-center space-y-4">
                        <div className="w-16 h-16 rounded-3xl bg-white/5 flex items-center justify-center border border-white/5 shadow-2xl">
                            <SparklesIcon size={32} className="text-white/20" />
                        </div>
                        <div className="space-y-2">
                            <h1 className="text-3xl font-bold bg-gradient-to-br from-white to-white/40 bg-clip-text text-transparent">Como posso ajudar hoje?</h1>
                            <p className="text-muted-foreground max-w-sm">Dê o primeiro passo para sua inteligência aumentada escolhendo um modelo ou digitando abaixo.</p>
                        </div>

                        <div className="grid grid-cols-2 gap-3 mt-8 max-w-lg w-full">
                            {['Analisar Código', 'Gerar Documentação', 'Explicar Conceito', 'Resumo de Texto'].map(action => (
                                <Button key={action} variant="outline" className="bg-white/5 border-white/5 hover:bg-white/10 text-xs py-6">
                                    {action}
                                </Button>
                            ))}
                        </div>
                    </div>
                </div>
            </ScrollArea>

            {/* Input area */}
            <div className="p-6">
                <div className="max-w-3xl mx-auto relative group">
                    <div className="absolute inset-0 bg-primary/20 blur-2xl opacity-0 group-focus-within:opacity-100 transition-opacity duration-500 rounded-2xl" />
                    <div className="relative bg-card/50 backdrop-blur-2xl border border-white/10 rounded-2xl p-2 focus-within:border-primary/50 transition-all shadow-2xl">
                        <textarea
                            placeholder="Digite aqui... (use / para comandos)"
                            className="w-full bg-transparent border-none focus:ring-0 text-sm p-3 min-h-[100px] resize-none text-white placeholder:text-muted-foreground/50"
                        />
                        <div className="flex items-center justify-between p-2">
                            <div className="flex gap-2">
                                <Button variant="ghost" size="icon" className="w-8 h-8 text-muted-foreground hover:text-white hover:bg-white/5">
                                    <PlusIcon size={16} />
                                </Button>
                            </div>
                            <Button size="icon" className="w-8 h-8 bg-white text-black hover:bg-white/90 rounded-xl transition-all shadow-lg active:scale-95">
                                <SendIcon size={14} />
                            </Button>
                        </div>
                    </div>
                    <p className="mt-2 text-[10px] text-center text-muted-foreground/50">NextMind pode cometer erros. Verifique informações importantes.</p>
                </div>
            </div>
        </div>
    )
}
