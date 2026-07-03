import { useEffect, useRef } from 'react';
import { Header } from './components/Header';
import { ChatInput } from './components/ChatInput';
import { ChatMessage } from './components/ChatMessage';
import { EmptyState } from './components/EmptyState';
import { useChatStore, type ResearchStage } from './store/useChatStore';



const chatStages: ResearchStage[] = [
  { id: '1', label: 'Understanding message', status: 'waiting' },
  { id: '2', label: 'Detecting intent', status: 'waiting' },
  { id: '3', label: 'Generating response', status: 'waiting' }
];

const knowledgeStages: ResearchStage[] = [
  { id: '1', label: 'Understanding question', status: 'waiting' },
  { id: '2', label: 'Detecting intent', status: 'waiting' },
  { id: '3', label: 'Gathering knowledge', status: 'waiting' },
  { id: '4', label: 'Generating answer', status: 'waiting' }
];

const researchStages: ResearchStage[] = [
  { id: '1', label: 'Understanding query', status: 'waiting' },
  { id: '2', label: 'Detecting research complexity', status: 'waiting' },
  { id: '3', label: 'Building research plan', status: 'waiting' },
  { id: '4', label: 'Searching Web', status: 'waiting' },
  { id: '5', label: 'Searching Wikipedia', status: 'waiting' },
  { id: '6', label: 'Searching Research Papers', status: 'waiting' },
  { id: '7', label: 'Searching News', status: 'waiting' },
  { id: '8', label: 'Reading Documentation', status: 'waiting' },
  { id: '9', label: 'Collecting Evidence', status: 'waiting' },
  { id: '10', label: 'Validating Sources', status: 'waiting' },
  { id: '11', label: 'Detecting Conflicts', status: 'waiting' },
  { id: '12', label: 'Building Knowledge', status: 'waiting' },
  { id: '13', label: 'Generating Insights', status: 'waiting' },
  { id: '14', label: 'Writing Report', status: 'waiting' },
  { id: '15', label: 'Reviewing Quality', status: 'waiting' },
  { id: '16', label: 'Formatting Citations', status: 'waiting' }
];

export default function App() {
  const { messages, addMessage, updateMessage, setGenerating, theme } = useChatStore();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [theme]);

  const handleSend = async (text: string) => {
    // Add user message
    addMessage({ role: 'user', content: text });
    setGenerating(true);
    
    // Create empty assistant message with waiting stages
    const assistantId = addMessage({ 
      role: 'assistant', 
      content: '', 
      isStreaming: true,
      researchProgress: [
        { id: '1', label: 'Understanding message', status: 'running' },
        { id: '2', label: 'Detecting intent', status: 'waiting' }
      ]
    });

    try {
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      
      // Call Backend API
      const res = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: text })
      });
      
      if (!res.ok) {
        throw new Error('Failed to fetch from backend');
      }

      const data = await res.json();
      
      // Update UI stages based on mode
      let finalStages: ResearchStage[] = [];
      if (data.mode === 'casual_chat') {
        finalStages = chatStages.map(s => ({...s, status: 'completed'}));
      } else if (data.mode === 'knowledge_answer') {
        finalStages = knowledgeStages.map(s => ({...s, status: 'completed'}));
      } else {
        finalStages = researchStages.map(s => ({...s, status: 'completed'}));
      }
      updateMessage(assistantId, { researchProgress: finalStages });

      const responseText = data.response || "No response received.";
      
      // Simulate Streaming text
      let currentText = '';
      const words = responseText.split(' ');
      
      for (let i = 0; i < words.length; i++) {
        currentText += (i === 0 ? '' : ' ') + words[i];
        updateMessage(assistantId, { content: currentText });
        await new Promise(r => setTimeout(r, 20));
      }

    } catch (error) {
      console.error(error);
      updateMessage(assistantId, { content: "Error connecting to backend API. Please ensure the server is running." });
    } finally {
      updateMessage(assistantId, { isStreaming: false });
      setGenerating(false);
    }
  };

  return (
    <div className="flex flex-col h-[100dvh] bg-background overflow-hidden text-foreground selection:bg-primary/30">
      <Header />
      
      <main className="flex-1 overflow-y-auto custom-scrollbar relative w-full overflow-x-hidden">
        {messages.length === 0 ? (
          <EmptyState onSelect={handleSend} />
        ) : (
          <div className="max-w-3xl mx-auto px-4 pb-32">
            {messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}
            <div ref={messagesEndRef} className="h-20" />
          </div>
        )}
      </main>

      <div className="absolute bottom-0 left-0 w-full bg-gradient-to-t from-background via-background/95 to-transparent pt-10">
        <ChatInput onSend={handleSend} />
      </div>
    </div>
  );
}
