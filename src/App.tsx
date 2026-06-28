/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState } from 'react';
import { LayoutDashboard, BedDouble, CalendarDays, Users, Receipt, BotMessageSquare, Moon, Sun } from 'lucide-react';
import DashboardView from './views/DashboardView.js';
import RoomsView from './views/RoomsView.js';
import BookingsView from './views/BookingsView.js';
import GuestsView from './views/GuestsView.js';
import InvoicesView from './views/InvoicesView.js';
import ChatbotView from './views/ChatbotView.js';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isDark, setIsDark] = useState(true);

  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'rooms', label: 'Rooms', icon: BedDouble },
    { id: 'bookings', label: 'Bookings', icon: CalendarDays },
    { id: 'guests', label: 'Guests', icon: Users },
    { id: 'invoices', label: 'Invoices', icon: Receipt },
    { id: 'chatbot', label: 'AI Receptionist', icon: BotMessageSquare },
  ];

  return (
    <div className={`flex h-screen w-full overflow-hidden ${isDark ? 'dark bg-gray-900 text-white' : 'bg-gray-50 text-gray-900'}`}>
      
      {/* Sidebar */}
      <div className="w-64 border-r border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-950 flex flex-col">
        <div className="p-6">
          <h1 className="text-2xl font-bold tracking-tight text-blue-600 dark:text-blue-400">Grand Vista</h1>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Hotel Management</p>
        </div>
        
        <nav className="flex-1 px-4 space-y-1 mt-4">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors ${
                  isActive 
                    ? 'bg-blue-50 text-blue-700 dark:bg-blue-900/50 dark:text-blue-300' 
                    : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
                }`}
              >
                <Icon size={18} />
                <span className="font-medium text-sm">{tab.label}</span>
              </button>
            );
          })}
        </nav>

        <div className="p-4 border-t border-gray-200 dark:border-gray-800">
          <button 
            onClick={() => setIsDark(!isDark)}
            className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white"
          >
            {isDark ? <Sun size={16} /> : <Moon size={16} />}
            {isDark ? 'Light Mode' : 'Dark Mode'}
          </button>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col h-full overflow-hidden">
        {/* Topbar */}
        <header className="h-16 border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-950 flex items-center justify-between px-8 shrink-0">
          <h2 className="text-lg font-semibold capitalize">{activeTab.replace('-', ' ')}</h2>
          <div className="text-sm font-medium text-gray-500 dark:text-gray-400">
            {new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
          </div>
        </header>

        {/* View Container */}
        <main className="flex-1 overflow-auto p-8">
          {activeTab === 'dashboard' && <DashboardView />}
          {activeTab === 'rooms' && <RoomsView />}
          {activeTab === 'bookings' && <BookingsView />}
          {activeTab === 'guests' && <GuestsView />}
          {activeTab === 'invoices' && <InvoicesView />}
          {activeTab === 'chatbot' && <ChatbotView />}
        </main>
      </div>

    </div>
  );
}
