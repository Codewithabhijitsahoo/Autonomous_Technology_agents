import { User, Copy, Check, RefreshCw } from 'lucide-react';
import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';
import 'highlight.js/styles/github-dark.css';
import { ResearchProgress } from './ResearchProgress';
import { SourcesSection } from './SourcesSection';
import type { Message } from '../store/useChatStore';
import { cn } from '../lib/utils';
import { motion } from 'framer-motion';

export function ChatMessage({ message }: { message: Message }) {
  const [copied, setCopied] = useState(false);
  const isUser = message.role === 'user';

  const copyToClipboard = () => {
    navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={cn("flex gap-4 w-full py-6 group", isUser ? "justify-end" : "justify-start")}
    >
      {!isUser && (
        <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0 mt-1 shadow-sm shadow-primary/20">
          <div className="w-4 h-4 bg-primary rounded-sm" /> 
        </div>
      )}
      
      <div className={cn(
        "max-w-[92%] md:max-w-[85%] flex flex-col gap-2 relative",
        isUser ? "items-end" : "items-start"
      )}>
        {isUser ? (
          <div className="bg-card text-foreground px-5 py-3 rounded-2xl rounded-tr-sm shadow-sm border border-border">
            <p className="text-sm md:text-base leading-relaxed whitespace-pre-wrap">{message.content}</p>
          </div>
        ) : (
          <div className="w-full">
            {message.researchProgress && <ResearchProgress stages={message.researchProgress} />}
            
            <div className="prose prose-invert max-w-none markdown-body text-foreground text-sm md:text-base">
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                rehypePlugins={[rehypeHighlight]}
              >
                {message.content + (message.isStreaming ? ' ▍' : '')}
              </ReactMarkdown>
            </div>
            
            {message.sources && <SourcesSection sources={message.sources} />}
            
            {!message.isStreaming && (
              <div className="flex items-center gap-2 mt-4 opacity-0 group-hover:opacity-100 transition-opacity">
                <button 
                  onClick={copyToClipboard}
                  className="p-1.5 text-muted hover:text-foreground transition-colors rounded-md hover:bg-black/5 dark:hover:bg-white/5"
                  title="Copy message"
                >
                  {copied ? <Check className="w-4 h-4 text-success" /> : <Copy className="w-4 h-4" />}
                </button>
                <button 
                  className="p-1.5 text-muted hover:text-foreground transition-colors rounded-md hover:bg-black/5 dark:hover:bg-white/5"
                  title="Regenerate"
                >
                  <RefreshCw className="w-4 h-4" />
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {isUser && (
        <div className="w-8 h-8 rounded-full bg-border flex items-center justify-center flex-shrink-0 mt-1">
          <User className="w-5 h-5 text-muted" />
        </div>
      )}
    </motion.div>
  );
}
