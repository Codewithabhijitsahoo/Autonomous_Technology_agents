import { Search, Settings, Moon, Sun, Plus } from 'lucide-react';
import { useChatStore } from '../store/useChatStore';

export function Header() {
  const { clearChat, theme, toggleTheme } = useChatStore();

  return (
    <header className="sticky top-0 z-50 w-full backdrop-blur-xl bg-background/80 border-b border-border/50">
      <div className="flex items-center justify-between h-16 px-4 md:px-6 max-w-6xl mx-auto">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-primary/20 flex items-center justify-center border border-primary/30 shadow-sm shadow-primary/20">
            <Search className="w-4.5 h-4.5 text-primary" />
          </div>
          <span className="font-semibold text-lg text-foreground tracking-tight hidden sm:inline-block">Deep Research</span>
        </div>

        <div className="flex items-center gap-2 sm:gap-4">
          <button 
            onClick={clearChat}
            className="hidden sm:flex items-center gap-2 px-4 py-2 text-sm font-medium bg-card border border-border rounded-full hover:bg-black/5 dark:hover:bg-white/5 transition-colors text-foreground shadow-sm"
          >
            <Plus className="w-4 h-4" />
            New Chat
          </button>
          
          <div className="flex items-center gap-1 border-l border-border/50 pl-2 sm:pl-4">
            <button 
              onClick={toggleTheme}
              className="p-2 text-muted hover:text-foreground transition-colors hover:bg-black/5 dark:hover:bg-white/5 rounded-full"
            >
              {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>
            <button className="p-2 text-muted hover:text-foreground transition-colors hover:bg-black/5 dark:hover:bg-white/5 rounded-full">
              <Settings className="w-5 h-5" />
            </button>
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-primary to-blue-500 border-2 border-background cursor-pointer hover:opacity-80 transition-opacity ml-2" />
          </div>
        </div>
      </div>
    </header>
  );
}
