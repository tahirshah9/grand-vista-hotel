import { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Trash2 } from 'lucide-react';

export default function ChatbotView() {
  const [messages, setMessages] = useState<{role: 'user'|'model', text: string}[]>([
    { role: 'model', text: 'Hello! I am Aria, the receptionist at Grand Vista. How can I help you today?' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, loading]);

  const handleSend = async (e: any) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg = input.trim();
    setMessages(prev => [...prev, { role: 'user', text: userMsg }]);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg })
      });
      const data = await res.json();
      setMessages(prev => [...prev, { role: 'model', text: data.response || data.error }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'model', text: "Network error communicating with AI." }]);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = async () => {
    await fetch('/api/chat/reset', { method: 'POST' });
    setMessages([{ role: 'model', text: 'Hello! I am Aria, the receptionist at Grand Vista. How can I help you today?' }]);
  };

  return (
    <div className="flex flex-col h-full bg-white dark:bg-gray-950 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm overflow-hidden">
      
      <div className="p-4 border-b border-gray-200 dark:border-gray-800 flex justify-between items-center bg-gray-50 dark:bg-gray-900">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white">
            <Bot size={18} />
          </div>
          <div>
            <h3 className="font-semibold text-sm">Aria</h3>
            <p className="text-xs text-green-600 dark:text-green-400">Online • AI Receptionist</p>
          </div>
        </div>
        <button onClick={handleReset} className="text-gray-500 hover:text-red-500 transition-colors p-2" title="Clear Chat">
          <Trash2 size={18} />
        </button>
      </div>

      <div ref={scrollRef} className="flex-1 p-4 overflow-y-auto space-y-6">
        {messages.map((msg, i) => (
          <div key={i} className={`flex gap-4 max-w-[80%] ${msg.role === 'user' ? 'ml-auto flex-row-reverse' : ''}`}>
            <div className={`w-8 h-8 shrink-0 rounded-full flex items-center justify-center text-white ${msg.role === 'user' ? 'bg-gray-800' : 'bg-blue-600'}`}>
              {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
            </div>
            <div className={`p-4 rounded-2xl text-sm leading-relaxed ${
              msg.role === 'user' 
                ? 'bg-blue-600 text-white rounded-tr-none' 
                : 'bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100 rounded-tl-none border border-gray-200 dark:border-gray-800'
            }`}>
              {msg.text}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex gap-4 max-w-[80%]">
            <div className="w-8 h-8 shrink-0 rounded-full bg-blue-600 flex items-center justify-center text-white">
              <Bot size={16} />
            </div>
            <div className="p-4 rounded-2xl bg-gray-100 dark:bg-gray-900 rounded-tl-none border border-gray-200 dark:border-gray-800 text-sm text-gray-500 flex gap-1 items-center">
              <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
              <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
              <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
            </div>
          </div>
        )}
      </div>

      <form onSubmit={handleSend} className="p-4 border-t border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-900 flex gap-2">
        <input 
          type="text" 
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Ask Aria about rooms, bookings, or hotel policies..." 
          className="flex-1 bg-white dark:bg-gray-950 border border-gray-200 dark:border-gray-700 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button 
          type="submit" 
          disabled={!input.trim() || loading}
          className="bg-blue-600 text-white p-2.5 rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
        >
          <Send size={20} />
        </button>
      </form>

    </div>
  );
}
