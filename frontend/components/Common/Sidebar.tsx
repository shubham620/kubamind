import React from 'react';
import Link from 'next/link';
import { useUIStore } from '@/store/uiStore';

interface NavItem {
  name: string;
  path: string;
  icon: string;
}

const navItems: NavItem[] = [
  { name: 'Dashboard', path: '/', icon: '📊' },
  { name: 'Insights', path: '/insights', icon: '💡' },
  { name: 'Predictions', path: '/predictions', icon: '🔮' },
  { name: 'Topology', path: '/topology', icon: '🕸️' },
  { name: 'Chat', path: '/chat', icon: '💬' },
  { name: 'Logs', path: '/logs', icon: '📝' },
];

export const Sidebar: React.FC = () => {
  const { sidebarOpen, activeTab, setActiveTab } = useUIStore();

  return (
    <aside
      className={`fixed left-0 top-0 h-screen bg-gray-900 border-r border-gray-800 transition-all duration-300 ${
        sidebarOpen ? 'w-64' : 'w-20'
      }`}
    >
      <div className="p-6 flex items-center gap-3">
        <div className="text-2xl">🤖</div>
        {sidebarOpen && <div className="text-lg font-bold text-white">KubeMind</div>}
      </div>

      <nav className="mt-8 space-y-2 px-3">
        {navItems.map((item) => (
          <Link key={item.path} href={item.path}>
            <a
              onClick={() => setActiveTab(item.path)}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                activeTab === item.path
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-400 hover:bg-gray-800'
              }`}
            >
              <span className="text-xl">{item.icon}</span>
              {sidebarOpen && <span className="text-sm">{item.name}</span>}
            </a>
          </Link>
        ))}
      </nav>
    </aside>
  );
};

export default Sidebar;
