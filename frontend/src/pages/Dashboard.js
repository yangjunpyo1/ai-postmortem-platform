import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';
import useAuth from '../hooks/useAuth';

function Dashboard() {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const [stats, setStats] = useState(null);
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [statsRes, incidentsRes] = await Promise.all([
        api.get('/api/statistics'),
        api.get('/api/incidents')
      ]);
      setStats(statsRes.data);
      setIncidents(incidentsRes.data.slice(0, 5));
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="min-h-screen bg-gray-900 p-8 text-center text-gray-400">로딩 중...</div>;

  return (
    <div className="min-h-screen bg-gray-900">
      <nav className="bg-gray-800 border-b border-gray-700 px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-gray-100 cursor-pointer" onClick={() => navigate('/dashboard')}>AI Postmortem Platform</h1>
        <div className="flex gap-4">
          <button onClick={() => navigate('/incidents')} className="text-gray-400 hover:text-blue-400 transition-colors">장애 목록</button>
          <button onClick={() => navigate('/statistics')} className="text-gray-400 hover:text-blue-400 transition-colors">통계</button>
          <button onClick={logout} className="text-red-400 hover:text-red-300 transition-colors">로그아웃</button>
        </div>
      </nav>

      <div className="max-w-6xl mx-auto p-6">
        <div className="grid grid-cols-2 gap-6 mb-6">
          <div className="bg-gray-800 border border-gray-700 rounded-lg p-6 text-center">
            <p className="text-gray-400 text-sm mb-2">전체 장애 건수</p>
            <p className="text-4xl font-bold text-blue-500">{stats?.total_incidents || 0}</p>
          </div>
          <div className="bg-gray-800 border border-gray-700 rounded-lg p-6 text-center">
            <p className="text-gray-400 text-sm mb-2">평균 다운타임</p>
            <p className="text-4xl font-bold text-red-400">{stats?.average_downtime ? `${Math.round(stats.average_downtime)}분` : '-'}</p>
          </div>
        </div>

        <div className="bg-gray-800 border border-gray-700 rounded-lg p-6 mb-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold text-gray-100">최근 장애</h2>
            <button onClick={() => navigate('/incidents')} className="text-blue-500 hover:text-blue-400 text-sm">전체 보기</button>
          </div>
          {incidents.length === 0 ? (
            <p className="text-gray-400 text-center py-4">장애 내역이 없습니다.</p>
          ) : (
            <div className="space-y-3">
              {incidents.map(inc => (
                <div
                  key={inc.id}
                  onClick={() => navigate(`/incidents/${inc.id}/postmortem`)}
                  className="border border-gray-700 rounded p-3 hover:bg-gray-700/50 cursor-pointer flex justify-between items-center transition-colors"
                >
                  <div>
                    <p className="font-medium text-gray-100">{inc.title}</p>
                    <p className="text-sm text-gray-400">{inc.severity} · {inc.category} · {new Date(inc.started_at).toLocaleDateString('ko-KR')}</p>
                  </div>
                  <span className={`text-xs px-2 py-1 rounded ${inc.status === '발생중' ? 'bg-red-500/20 text-red-400' : 'bg-green-500/20 text-green-400'}`}>
                    {inc.status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
          <h2 className="text-xl font-bold text-gray-100 mb-4">모니터링 대시보드</h2>
          <div className="bg-gray-900/60 border border-gray-700 rounded p-4 text-center text-gray-400">
            <p className="mb-2">Grafana 모니터링은 SSM 포트 포워딩으로 접근 가능합니다.</p>
            <a href="http://localhost:3000" target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:text-blue-400 underline">Grafana 대시보드 열기 (localhost:3000)</a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;