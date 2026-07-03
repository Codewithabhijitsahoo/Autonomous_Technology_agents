import { motion } from 'framer-motion';
import { SourceCard } from './SourceCard';
import type { Source } from '../store/useChatStore';

export function SourcesSection({ sources }: { sources: Source[] }) {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-4 pt-4 border-t border-border/50">
      <h3 className="text-sm font-medium text-muted mb-3 flex items-center gap-2">
        <span className="w-4 h-4 rounded-full bg-primary/20 flex items-center justify-center">
          <span className="w-1.5 h-1.5 rounded-full bg-primary"></span>
        </span>
        Sources
      </h3>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
        {sources.map((source, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
          >
            <SourceCard source={source} />
          </motion.div>
        ))}
      </div>
    </div>
  );
}
