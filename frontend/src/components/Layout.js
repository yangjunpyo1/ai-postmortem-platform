import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import useAuth from '../hooks/useAuth';

const DashboardIcon = () => (
  <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
    <rect x="3" y="3" width="7" height="9" rx="1.5" />
    <rect x="14" y="3" width="7" height="5" rx="1.5" />
    <rect x="14" y="12" width="7" height="9" rx="1.5" />
    <rect x="3" y="16" width="7" height="5" rx="1.5" />
  </svg>
);

const IncidentIcon = () => (
  <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
    <path d="M12 3 2 20h20L12 3Z" strokeLinejoin="round" />
    <path d="M12 10v4" strokeLinecap="round" />
    <path d="M12 17.5v.01" strokeLinecap="round" />
  </svg>
);

const ChartIcon = () => (
  <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
    <path d="M4 20V10" strokeLinecap="round" />
    <path d="M12 20V4" strokeLinecap="round" />
    <path d="M20 20v-7" strokeLinecap="round" />
  </svg>
);

const GrafanaIcon = () => (
  <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
    <path d="M14 4h6v6" strokeLinecap="round" strokeLinejoin="round" />
    <path d="M20 4 11 13" strokeLinecap="round" strokeLinejoin="round" />
    <path d="M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h5" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

const LogoutIcon = () => (
  <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" strokeLinecap="round" strokeLinejoin="round" />
    <path d="M16 17l5-5-5-5" strokeLinecap="round" strokeLinejoin="round" />
    <path d="M21 12H9" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

const navItems = [
  { label: '대시보드', path: '/dashboard', icon: DashboardIcon },
  { label: '장애 목록', path: '/incidents', icon: IncidentIcon },
  { label: '통계', path: '/statistics', icon: ChartIcon },
];

function Layout({ children }) {
  const navigate = useNavigate();
  const location = useLocation();
  const { logout } = useAuth();

  return (
    <div className="min-h-screen bg-gray-950">
      <aside className="fixed inset-y-0 left-0 w-60 bg-gray-900 border-r border-gray-800 flex flex-col z-40">
        <div
          className="h-16 flex items-center gap-2 px-5 border-b border-gray-800 cursor-pointer"
          onClick={() => navigate('/dashboard')}
        >
          <span className="w-2.5 h-2.5 rounded-full bg-blue-500" />
          <span className="text-sm font-bold text-gray-100 tracking-tight">AI Postmortem</span>
        </div>

        <nav className="flex-1 px-3 py-4 space-y-1">
          {navItems.map(({ label, path, icon: Icon }) => {
            const active = location.pathname.startsWith(path);
            return (
              <button
                key={path}
                onClick={() => navigate(path)}
                className={`w-full flex items-center gap-3 px-3 py-2 rounded text-sm font-medium transition-colors border-l-2 ${
                  active
                    ? 'bg-gray-800 text-blue-400 border-blue-500'
                    : 'text-gray-400 border-transparent hover:bg-gray-800/60 hover:text-gray-100'
                }`}
              >
                <Icon />
                {label}
              </button>
            );
          })}

          <a
            href="http://localhost:3000"
            target="_blank"
            rel="noopener noreferrer"
            className="w-full flex items-center gap-3 px-3 py-2 rounded text-sm font-medium text-gray-400 border-l-2 border-transparent hover:bg-gray-800/60 hover:text-gray-100 transition-colors"
          >
            <GrafanaIcon />
            Grafana
          </a>
        </nav>

        <div className="px-3 py-4 border-t border-gray-800">
          <button
            onClick={logout}
            className="w-full flex items-center gap-3 px-3 py-2 rounded text-sm font-medium text-red-400 hover:bg-red-500/10 hover:text-red-300 transition-colors"
          >
            <LogoutIcon />
            로그아웃
          </button>
        </div>
      </aside>

      <main className="ml-60 min-h-screen">{children}</main>
    </div>
  );
}

export default Layout;
