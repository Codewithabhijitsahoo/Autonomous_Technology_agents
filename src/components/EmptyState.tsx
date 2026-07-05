import { Search, ArrowRight } from 'lucide-react';
import { motion } from 'framer-motion';

const suggestions = [
  { title: "Explain Agentic AI", desc: "Understand the core concepts of autonomous AI agents." },
  { title: "Compare GPT vs Gemini", desc: "Analyze the differences between the leading LLMs." },
  { title: "Latest AI Research Papers", desc: "Find recent breakthroughs in machine learning." },
  { title: "Create Market Analysis Report", desc: "Generate a detailed report on a specific industry." }
];

export function EmptyState({ onSelect }: { onSelect: (text: string) => void }) {
  return (
    <div className="flex flex-col items-center justify-center h-full max-w-3xl mx-auto px-4 mt-16 md:mt-24">
      <motion.div 
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="w-16 h-16 rounded-2xl bg-primary/20 flex items-center justify-center border border-primary/30 mb-6 shadow-lg shadow-primary/20"
      >
        <Search className="w-8 h-8 text-primary" />
      </motion.div>
      
      <motion.h1 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="text-3xl md:text-4xl font-bold text-foreground mb-3 text-center tracking-tight"
      >
        Deep Technology Assistant
      </motion.h1>
      
      <motion.p 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="text-muted text-center max-w-lg mb-12"
      >
        Ask complex questions and receive comprehensive research-backed answers with citations.
      </motion.p>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full">
        {suggestions.map((suggestion, index) => (
          <motion.button
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 + index * 0.1 }}
            onClick={() => onSelect(suggestion.title)}
            className="group flex flex-col items-start p-4 bg-card border border-border rounded-xl hover:border-primary/50 hover:bg-black/5 dark:hover:bg-white/5 transition-all duration-300 text-left"
          >
            <div className="flex items-center justify-between w-full mb-1">
              <h3 className="font-medium text-foreground group-hover:text-primary transition-colors">{suggestion.title}</h3>
              <ArrowRight className="w-4 h-4 text-muted opacity-0 -translate-x-2 group-hover:opacity-100 group-hover:translate-x-0 transition-all duration-300" />
            </div>
            <p className="text-sm text-muted">{suggestion.desc}</p>
          </motion.button>
        ))}
      </div>
    </div>
  );
}
