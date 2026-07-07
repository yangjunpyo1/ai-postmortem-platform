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

  if (loading) return <div className="p-8 text-center">로딩 중...</div>;

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-bold cursor-pointer" onClick={() => navigate('/dashboard')}>AI Postmortem Platform</h1>
        <div className="flex gap-4">
          <button onClick={() => navigate('/incidents')} className="text-gray-600 hover:text-blue-600">장애 목록</button>
          <button onClick={() => navigate('/statistics')} className="text-gray-600 hover:text-blue-600">통계</button>
          <button onClick={logout} className="text-red-600 hover:text-red-800">로그아웃</button>
        </div>
      </nav>

      <div className="max-w-6xl mx-auto p-6">
        <div className="grid grid-cols-2 gap-6 mb-6">
          <div className="bg-white rounded-lg shadow p-6 text-center">
            <p className="text-gray-500 text-sm mb-2">전체 장애 건수</p>
            <p className="text-4xl font-bold text-blue-600">{stats?.total_incidents || 0}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6 text-center">
            <p className="text-gray-500 text-sm mb-2">평균 다운타임</p>
            <p className="text-4xl font-bold text-red-600">{stats?.average_downtime ? `${Math.round(stats.average_downtime)}분` : '-'}</p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold">최근 장애</h2>
            <button onClick={() => navigate('/incidents')} className="text-blue-600 hover:text-blue-800 text-sm">전체 보기</button>
          </div>
          {incidents.length === 0 ? (
            <p className="text-gray-500 text-center py-4">장애 내역이 없습니다.</p>
          ) : (
            <div className="space-y-3">
              {incidents.map(inc => (
                <div
                  key={inc.id}
                  onClick={() => navigate(`/incidents/${inc.id}/postmortem`)}
                  className="border rounded p-3 hover:bg-gray-50 cursor-pointer flex justify-between items-center"
                >
                  <div>
                    <p className="font-medium">{inc.title}</p>
                    <p className="text-sm text-gray-500">{inc.severity} · {inc.category} · {new Date(inc.started_at).toLocaleDateString('ko-KR')}</p>
                  </div>
                  <span className={`text-xs px-2 py-1 rounded ${inc.status === '발생중' ? 'bg-red-100 text-red-600' : 'bg-green-100 text-green-600'}`}>
                    {inc.status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold mb-4">모니터링 대시보드</h2>
          <div className="bg-gray-50 rounded p-4 text-center text-gray-500">
            <p className="mb-2">Grafana 모니터링은 SSM 포트 포워딩으로 접근 가능합니다.</p>
            <a href="http://localhost:3000" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-800 underline">Grafana 대시보드 열기 (localhost:3000)</a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;