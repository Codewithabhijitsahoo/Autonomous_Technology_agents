import { Paperclip, Globe, Search, ArrowUp, Square } from 'lucide-react';
import { useState, useRef, useEffect } from 'react';
import { useChatStore } from '../store/useChatStore';
import { cn } from '../lib/utils';

export function ChatInput({ onSend }: { onSend: (text: string) => void }) {
  const [input, setInput] = useState('');
  const [isDeepResearch, setIsDeepResearch] = useState(true);
  const [isWebSearch, setIsWebSearch] = useState(true);
  const { isGenerating, setGenerating } = useChatStore();
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (input.trim() && !isGenerating) {
        onSend(input);
        setInput('');
      }
    }
  };

  const handleSend = () => {
    if (input.trim() && !isGenerating) {
      onSend(input);
      setInput('');
    }
  };

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  }, [input]);

  return (
    <div className="w-full max-w-3xl mx-auto px-4 pb-4 sm:pb-6 relative z-10">
      <div className="bg-card border border-border rounded-2xl p-3 shadow-md focus-within:border-primary/50 focus-within:ring-1 focus-within:ring-primary/50 transition-all duration-200">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask anything and I'll research it thoroughly..."
          className="w-full max-h-[200px] bg-transparent text-foreground placeholder:text-muted resize-none outline-none border-none focus:ring-0 text-base py-2 min-h-[44px] overflow-y-auto"
          rows={1}
        />
        
        <div className="flex items-center justify-between mt-2 pt-2 border-t border-border/50">
          <div className="flex items-center gap-1 sm:gap-2">
            <button className="p-2 text-muted hover:text-foreground hover:bg-black/5 dark:hover:bg-white/5 rounded-full transition-colors" title="Attach file">
              <Paperclip className="w-4 h-4" />
            </button>
            <button 
              onClick={() => setIsDeepResearch(!isDeepResearch)}
              className={cn(
                "flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium transition-colors",
                isDeepResearch ? "bg-primary/20 text-primary" : "text-muted hover:bg-black/5 dark:hover:bg-white/5 hover:text-foreground"
              )}
            >
              <Search className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Deep Research</span>
            </button>
            <button 
              onClick={() => setIsWebSearch(!isWebSearch)}
              className={cn(
                "flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium transition-colors",
                isWebSearch ? "bg-primary/20 text-primary" : "text-muted hover:bg-black/5 dark:hover:bg-white/5 hover:text-foreground"
              )}
            >
              <Globe className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Web Search</span>
            </button>
          </div>
          
          {isGenerating ? (
            <button 
              onClick={() => setGenerating(false)}
              className="p-2 bg-card border border-border text-foreground hover:bg-black/5 dark:hover:bg-white/5 rounded-full transition-colors flex items-center justify-center h-10 w-10 shadow-sm"
              title="Stop generating"
            >
              <Square className="w-4 h-4 fill-current" />
            </button>
          ) : (
            <button 
              onClick={handleSend}
              disabled={!input.trim()}
              className="p-2 bg-primary text-white disabled:opacity-50 disabled:cursor-not-allowed hover:bg-primary/90 rounded-full transition-colors flex items-center justify-center h-10 w-10 shadow-sm"
              title="Send message"
            >
              <ArrowUp className="w-5 h-5" />
            </button>
          )}
        </div>
      </div>
      <div className="text-center mt-3">
        <p className="text-xs text-muted">
          Deep Research AI can make mistakes. Verify important information. • built by <a href="https://www.linkedin.com/in/abhijit-sahoo-3a2872294?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app" target="_blank" rel="noopener noreferrer" className="hover:text-primary transition-colors hover:underline">abhijit sahoo with ❤️</a>
        </p>
      </div>
    </div>
  );
}
