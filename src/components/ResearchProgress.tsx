import { motion } from 'framer-motion';
import { Check, Circle, Loader2, ChevronDown, ChevronUp } from 'lucide-react';
import { useState } from 'react';
import type { ResearchStage } from '../store/useChatStore';

export function ResearchProgress({ stages }: { stages: ResearchStage[] }) {
  const [expanded, setExpanded] = useState(true);
  
  if (!stages || stages.length === 0) return null;
  
  const isAllDone = stages.every(s => s.status === 'completed');

  return (
    <div className="bg-card border border-border rounded-lg mb-4 overflow-hidden">
      <button 
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between p-3 text-sm font-medium hover:bg-black/5 dark:hover:bg-white/5 transition-colors"
      >
        <div className="flex items-center gap-2 text-primary">
          {isAllDone ? <Check className="w-4 h-4" /> : <Loader2 className="w-4 h-4 animate-spin" />}
          <span>{isAllDone ? 'Research completed' : 'Researching...'}</span>
        </div>
        {expanded ? <ChevronUp className="w-4 h-4 text-muted" /> : <ChevronDown className="w-4 h-4 text-muted" />}
      </button>
      
      {expanded && (
        <div className="p-4 pt-0 border-t border-border/50">
          <div className="space-y-3 mt-3">
            {stages.map((stage, i) => (
              <motion.div 
                key={stage.id}
                initial={{ opacity: 0, y: 5 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                className="flex items-center gap-3 text-sm"
              >
                {stage.status === 'completed' ? (
                  <Check className="w-4 h-4 text-success" />
                ) : stage.status === 'running' ? (
                  <Loader2 className="w-4 h-4 text-primary animate-spin" />
                ) : (
                  <Circle className="w-4 h-4 text-muted" />
                )}
                <span className={stage.status === 'waiting' ? 'text-muted' : 'text-foreground'}>
                  {stage.label}
                </span>
              </motion.div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
