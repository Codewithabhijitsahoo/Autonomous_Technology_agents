import { ExternalLink } from 'lucide-react';
import type { Source } from '../store/useChatStore';

export function SourceCard({ source }: { source: Source }) {
  return (
    <a 
      href={source.url}
      target="_blank"
      rel="noopener noreferrer"
      className="block group bg-background border border-border rounded-lg p-3 hover:border-primary/50 hover:bg-card transition-all duration-200 transform hover:-translate-y-1"
    >
      <div className="flex justify-between items-start mb-2">
        <div className="flex items-center gap-2">
          {source.favicon ? (
            <img src={source.favicon} alt={source.name} className="w-4 h-4 rounded-sm" />
          ) : (
            <div className="w-4 h-4 rounded-sm bg-muted flex-shrink-0" />
          )}
          <span className="text-xs font-medium text-muted line-clamp-1 group-hover:text-foreground transition-colors">{source.name}</span>
        </div>
        <ExternalLink className="w-3 h-3 text-muted opacity-0 group-hover:opacity-100 transition-opacity" />
      </div>
      <h4 className="text-sm font-semibold text-foreground mb-1 line-clamp-2 group-hover:text-primary transition-colors">{source.title}</h4>
      <p className="text-xs text-muted line-clamp-2">{source.description}</p>
    </a>
  );
}
