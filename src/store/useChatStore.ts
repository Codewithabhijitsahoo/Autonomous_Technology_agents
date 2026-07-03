import { create } from 'zustand';

export interface Source {
  name: string;
  title: string;
  description: string;
  url: string;
  favicon: string;
}

export interface ResearchStage {
  id: string;
  label: string;
  status: 'waiting' | 'running' | 'completed';
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: Source[];
  researchProgress?: ResearchStage[];
  isStreaming?: boolean;
}

interface ChatState {
  messages: Message[];
  isGenerating: boolean;
  theme: 'light' | 'dark';
  addMessage: (msg: Omit<Message, 'id'>) => string;
  updateMessage: (id: string, partial: Partial<Message>) => void;
  setGenerating: (generating: boolean) => void;
  clearChat: () => void;
  toggleTheme: () => void;
}

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  isGenerating: false,
  theme: 'dark',
  toggleTheme: () => set((state) => ({ theme: state.theme === 'light' ? 'dark' : 'light' })),
  addMessage: (msg) => {
    const id = crypto.randomUUID();
    set((state) => ({
      messages: [...state.messages, { ...msg, id }],
    }));
    return id;
  },
  updateMessage: (id, partial) =>
    set((state) => ({
      messages: state.messages.map((m) =>
        m.id === id ? { ...m, ...partial } : m
      ),
    })),
  setGenerating: (isGenerating) => set({ isGenerating }),
  clearChat: () => set({ messages: [], isGenerating: false }),
}));
