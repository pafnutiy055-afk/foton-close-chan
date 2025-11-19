
import React, { useState, useEffect, useRef } from 'react';
import { createRoot } from 'react-dom/client';
import { 
  Send, 
  FileText, 
  Play, 
  CheckCircle, 
  Bot, 
  User, 
  Download, 
  Clock,
  ArrowRight
} from 'lucide-react';

// --- Types ---

type MessageType = 'bot' | 'user' | 'system';

interface Message {
  id: number;
  type: MessageType;
  content: string;
  attachment?: {
    type: 'file' | 'video';
    title: string;
    url?: string;
  };
}

interface QuizData {
  niche?: string;
  goal?: string;
  experience?: string;
  platform?: string;
}

// --- Texts (From your Python Code) ---

const TEXTS = {
  WELCOME: "👋 **Привет! Это Артём и команда Foton Plus.**\n\nМы не льем воду, мы даем инструменты, которые приносят деньги. 💸\nЯ подготовил для тебя пошаговую систему по маркетингу.\n\nГотов забрать первый инструмент и усилить свой бизнес? 👇",
  MANUAL_SENT: "📘 **Твой Мануал по маркетингу**\n\nИзучи его, чтобы понимать базу. Но теория без цифр — ничто.\nГотов взять под контроль показатели своего бизнеса?",
  KPI_SENT: "📊 **Таблица KPI (Метрика)**\n\nТеперь ты видишь цифры. Но уверен ли ты, что твоя реклама настроена без ошибок?\nДержи чек-лист, который спас тысячи бюджетов от слива. 👇",
  CHECKLIST_SENT: "📑 **Чек-лист «Проверка кампании»**\n\nТеперь ты защищен от глупых ошибок. \n🔥 А сейчас — самое главное. **Секретный видеоурок**, где я разбираю реальные стратегии.",
  VIDEO_SENT: "🎥 **ДОСТУП ОТКРЫТ!**\n\nВ этом видео — концентрат опыта. Смотри внимательно, инсайты гарантированы.\n\n⏳ *Через 2 часа я вернусь с важным предложением.*",
  QUIZ_OFFER: "🚀 **Прошло 2 часа! Как впечатления?**\n\nМатериалы — это круто, но результат дает только **индивидуальная стратегия**.\n\nДавай я помогу адаптировать эти знания под ТВОЙ бизнес. \nОтветь на 4 простых вопроса, и мы составим план действий конкретно для тебя. 👇",
  QUIZ_Q1: "1️⃣ **Вопрос 1:** В какой нише вы работаете?",
  QUIZ_Q2: "2️⃣ **Вопрос 2:** Какая ГЛАВНАЯ цель вашей рекламы сейчас?",
  QUIZ_Q3: "3️⃣ **Вопрос 3:** Какой у вас опыт в рекламе? (Новичок / Сливал бюджет / Профи)",
  QUIZ_Q4: "4️⃣ **Вопрос 4:** На какой площадке планируете запускаться? (VK / Яндекс / Telegram / Другое)",
  QUIZ_FINAL: "🔥 **Спасибо! Я проанализировал твои ответы.**\n\nМы подготовили стратегию специально под твою нишу.\nНажми кнопку ниже, напиши менеджеру **«РАЗБОР»**, и мы бесплатно обсудим твой запуск! 👇"
};

// --- Components ---

const ChatBubble = ({ message }: { message: Message }) => {
  const isBot = message.type === 'bot';
  
  return (
    <div className={`flex w-full mb-4 ${isBot ? 'justify-start' : 'justify-end'} fade-in-up`}>
      <div className={`flex max-w-[85%] md:max-w-[70%] ${isBot ? 'flex-row' : 'flex-row-reverse'}`}>
        
        {/* Avatar */}
        <div className={`flex-shrink-0 h-8 w-8 rounded-full flex items-center justify-center ${isBot ? 'bg-blue-600 mr-2' : 'bg-emerald-600 ml-2'}`}>
          {isBot ? <Bot size={18} className="text-white" /> : <User size={18} className="text-white" />}
        </div>

        {/* Bubble */}
        <div className={`p-3 rounded-2xl text-sm md:text-base shadow-sm whitespace-pre-wrap ${
          isBot 
            ? 'bg-slate-800 text-slate-100 rounded-tl-none border border-slate-700' 
            : 'bg-blue-600 text-white rounded-tr-none'
        }`}>
          {/* Markdown-like parsing for bold text */}
          <div dangerouslySetInnerHTML={{ 
            __html: message.content
              .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') 
              .replace(/\n/g, '<br/>')
          }} />

          {/* Attachments */}
          {message.attachment && (
            <div className="mt-3 p-3 bg-slate-900/50 rounded-xl border border-slate-700/50 flex items-center gap-3 hover:bg-slate-900 transition-colors cursor-pointer">
              {message.attachment.type === 'video' ? (
                <div className="h-10 w-10 bg-red-600 rounded-lg flex items-center justify-center flex-shrink-0">
                  <Play size={20} fill="white" className="text-white ml-1" />
                </div>
              ) : (
                <div className="h-10 w-10 bg-blue-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                  <FileText size={20} className="text-blue-400" />
                </div>
              )}
              <div className="flex-1 min-w-0">
                <div className="font-medium text-slate-200 truncate">{message.attachment.title}</div>
                <div className="text-xs text-slate-400">
                  {message.attachment.type === 'video' ? 'YouTube • 15:00' : 'PDF Document • 2.4 MB'}
                </div>
              </div>
              <Download size={16} className="text-slate-500" />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const TypingIndicator = () => (
  <div className="flex w-full mb-4 justify-start fade-in-up">
    <div className="flex items-end">
       <div className="flex-shrink-0 h-8 w-8 rounded-full bg-blue-600 mr-2 flex items-center justify-center">
          <Bot size={18} className="text-white" />
       </div>
       <div className="bg-slate-800 border border-slate-700 p-3 rounded-2xl rounded-tl-none">
         <div className="flex gap-1 h-4 items-center">
           <div className="w-2 h-2 bg-slate-400 rounded-full typing-dot"></div>
           <div className="w-2 h-2 bg-slate-400 rounded-full typing-dot"></div>
           <div className="w-2 h-2 bg-slate-400 rounded-full typing-dot"></div>
         </div>
       </div>
    </div>
  </div>
);

// --- Main App ---

const App = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const [step, setStep] = useState('start'); // start, manual_wait, kpi_wait, checklist_wait, video_wait, waiting_quiz, quiz_niche, quiz_goal, quiz_exp, quiz_platform, finished
  const [quizData, setQuizData] = useState<QuizData>({});
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  // Initial Message
  useEffect(() => {
    addBotMessage(TEXTS.WELCOME);
  }, []);

  const addBotMessage = (text: string, attachment?: Message['attachment'], delay = 800) => {
    setIsTyping(true);
    setTimeout(() => {
      setIsTyping(false);
      setMessages(prev => [...prev, {
        id: Date.now(),
        type: 'bot',
        content: text,
        attachment
      }]);
    }, delay);
  };

  const addUserMessage = (text: string) => {
    setMessages(prev => [...prev, {
      id: Date.now(),
      type: 'user',
      content: text
    }]);
  };

  const handleButtonClick = (action: string) => {
    if (action === 'get_manual') {
      addUserMessage("📘 Скачать мануал");
      setStep('sending_manual');
      setTimeout(() => {
        addBotMessage(TEXTS.MANUAL_SENT, { type: 'file', title: 'Marketing_Manual.pdf' });
        setStep('kpi_wait');
      }, 1500);
    }
    else if (action === 'get_kpi') {
      addUserMessage("📊 Забрать таблицу KPI");
      setStep('sending_kpi');
      setTimeout(() => {
        addBotMessage(TEXTS.KPI_SENT, { type: 'file', title: 'Metrika_KPI.pdf' });
        setStep('checklist_wait');
      }, 1500);
    }
    else if (action === 'get_checklist') {
      addUserMessage("📑 Получить чек-лист");
      setStep('sending_checklist');
      setTimeout(() => {
        addBotMessage(TEXTS.CHECKLIST_SENT, { type: 'file', title: 'Check_List.pdf' });
        setStep('video_wait');
      }, 1500);
    }
    else if (action === 'get_video') {
      addUserMessage("🎥 Смотреть видеоурок");
      setStep('watching_video');
      setTimeout(() => {
        addBotMessage(TEXTS.VIDEO_SENT, { type: 'video', title: 'Секретный Урок • Youtube', url: 'https://youtu.be/P-3NZnicpbk' });
        setStep('waiting_timer');
      }, 1500);
    }
    else if (action === 'simulate_2h') {
      // Simulate the 2 hour wait
      setStep('timer_done');
      addBotMessage(TEXTS.QUIZ_OFFER);
      setStep('quiz_offer_wait');
    }
    else if (action === 'start_quiz') {
      addUserMessage("🧠 ПРОЙТИ РАЗБОР");
      setStep('quiz_niche');
      addBotMessage(TEXTS.QUIZ_Q1);
    }
  };

  const handleInputSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const text = inputValue;
    setInputValue('');
    addUserMessage(text);

    if (step === 'quiz_niche') {
      setQuizData({ ...quizData, niche: text });
      setStep('quiz_goal');
      addBotMessage(TEXTS.QUIZ_Q2);
    } else if (step === 'quiz_goal') {
      setQuizData({ ...quizData, goal: text });
      setStep('quiz_exp');
      addBotMessage(TEXTS.QUIZ_Q3);
    } else if (step === 'quiz_exp') {
      setQuizData({ ...quizData, experience: text });
      setStep('quiz_platform');
      addBotMessage(TEXTS.QUIZ_Q4);
    } else if (step === 'quiz_platform') {
      setQuizData({ ...quizData, platform: text });
      setStep('finished');
      addBotMessage(TEXTS.QUIZ_FINAL);
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-md mx-auto bg-slate-950 shadow-2xl border-x border-slate-800">
      {/* Header */}
      <header className="bg-slate-900 border-b border-slate-800 p-4 flex items-center gap-3 sticky top-0 z-10">
        <div className="relative">
          <div className="h-10 w-10 bg-blue-600 rounded-full flex items-center justify-center">
            <Bot size={24} className="text-white" />
          </div>
          <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-500 rounded-full border-2 border-slate-900"></div>
        </div>
        <div>
          <h1 className="font-bold text-slate-100">Artem | Foton Plus</h1>
          <p className="text-xs text-blue-400 font-medium">Marketing Bot • Online</p>
        </div>
      </header>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2 bg-[#0b1121]">
        {messages.map(msg => (
          <ChatBubble key={msg.id} message={msg} />
        ))}
        {isTyping && <TypingIndicator />}
        <div ref={messagesEndRef} />
        
        {/* Contextual Actions inside chat flow if needed, usually bottom is better */}
      </div>

      {/* Input / Action Area */}
      <div className="p-4 bg-slate-900 border-t border-slate-800">
        
        {/* Step: Start */}
        {step === 'start' && !isTyping && (
          <button 
            onClick={() => handleButtonClick('get_manual')}
            className="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold py-3 px-4 rounded-xl flex items-center justify-center gap-2 transition-all transform hover:scale-[1.02] active:scale-95"
          >
            <FileText size={20} />
            📘 Скачать мануал
          </button>
        )}

        {/* Step: KPI Wait */}
        {step === 'kpi_wait' && !isTyping && (
          <button 
            onClick={() => handleButtonClick('get_kpi')}
            className="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-semibold py-3 px-4 rounded-xl flex items-center justify-center gap-2 transition-all transform hover:scale-[1.02] active:scale-95"
          >
            <CheckCircle size={20} />
            📊 Забрать таблицу KPI
          </button>
        )}

        {/* Step: Checklist Wait */}
        {step === 'checklist_wait' && !isTyping && (
          <button 
            onClick={() => handleButtonClick('get_checklist')}
            className="w-full bg-violet-600 hover:bg-violet-500 text-white font-semibold py-3 px-4 rounded-xl flex items-center justify-center gap-2 transition-all transform hover:scale-[1.02] active:scale-95"
          >
            <FileText size={20} />
            📑 Получить чек-лист
          </button>
        )}

        {/* Step: Video Wait */}
        {step === 'video_wait' && !isTyping && (
          <button 
            onClick={() => handleButtonClick('get_video')}
            className="w-full bg-red-600 hover:bg-red-500 text-white font-semibold py-3 px-4 rounded-xl flex items-center justify-center gap-2 transition-all transform hover:scale-[1.02] active:scale-95"
          >
            <Play size={20} fill="currentColor" />
            🎥 Смотреть видеоурок
          </button>
        )}

        {/* Step: Waiting Timer (Simulation) */}
        {step === 'waiting_timer' && !isTyping && (
          <div className="space-y-3 text-center">
            <div className="text-xs text-slate-500">Waiting 2 hours... (Simulated)</div>
            <button 
              onClick={() => handleButtonClick('simulate_2h')}
              className="w-full border border-slate-700 hover:bg-slate-800 text-slate-300 font-semibold py-3 px-4 rounded-xl flex items-center justify-center gap-2 transition-all"
            >
              <Clock size={20} />
              ⚡ Fast Forward 2 Hours
            </button>
          </div>
        )}

         {/* Step: Quiz Offer Wait */}
         {step === 'quiz_offer_wait' && !isTyping && (
          <button 
            onClick={() => handleButtonClick('start_quiz')}
            className="w-full bg-amber-500 hover:bg-amber-400 text-black font-bold py-3 px-4 rounded-xl flex items-center justify-center gap-2 transition-all transform hover:scale-[1.02] active:scale-95 animate-pulse"
          >
            🧠 ПРОЙТИ РАЗБОР
          </button>
        )}

        {/* Step: Quiz Input */}
        {['quiz_niche', 'quiz_goal', 'quiz_exp', 'quiz_platform'].includes(step) && (
          <form onSubmit={handleInputSubmit} className="flex gap-2">
            <input 
              type="text" 
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Введите ваш ответ..." 
              className="flex-1 bg-slate-800 text-slate-100 border border-slate-700 rounded-xl px-4 py-3 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
              autoFocus
            />
            <button 
              type="submit"
              disabled={!inputValue.trim()}
              className="bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 disabled:text-slate-500 text-white p-3 rounded-xl transition-colors"
            >
              <ArrowRight size={24} />
            </button>
          </form>
        )}

        {/* Step: Finished */}
        {step === 'finished' && !isTyping && (
           <a 
           href="https://t.me/bery_lydu" 
           target="_blank"
           className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-bold py-4 px-4 rounded-xl flex items-center justify-center gap-2 transition-all transform hover:scale-[1.02] shadow-lg shadow-blue-900/50"
         >
           <Send size={20} />
           📩 ЗАБРАТЬ РАЗБОР У МЕНЕДЖЕРА
         </a>
        )}

        {/* Disabled state for transitions */}
        {isTyping && (
          <div className="text-center text-slate-500 text-sm py-3">
            Artem печатает...
          </div>
        )}

      </div>
    </div>
  );
};

const root = createRoot(document.getElementById('root')!);
root.render(<App />);
