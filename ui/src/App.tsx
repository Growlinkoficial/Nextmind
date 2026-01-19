import { useState } from 'react'
import { Button } from "@/components/ui/button"

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="h-screen w-full flex flex-col items-center justify-center text-foreground p-8">
      <div className="bg-card/50 backdrop-blur-xl border border-white/10 p-12 rounded-2xl shadow-2xl flex flex-col items-center gap-6">
        <div className="space-y-2 text-center">
          <h1 className="text-5xl font-bold tracking-tight bg-gradient-to-br from-white to-white/50 bg-clip-text text-transparent">NextMind</h1>
          <p className="text-lg text-muted-foreground">Cognitive Intelligence Infrastructure</p>
        </div>

        <div className="flex gap-4">
          <Button onClick={() => setCount(count + 1)} className="shadow-lg shadow-primary/20">
            Count is {count}
          </Button>
          <Button variant="secondary" onClick={() => setCount(0)} className="bg-white/5 hover:bg-white/10 border border-white/5">
            Reset
          </Button>
        </div>
      </div>
    </div>
  )
}

export default App
