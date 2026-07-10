import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';
import SeverityBadge from '../components/SeverityBadge';
import StatusBadge from '../components/StatusBadge';

function Dashboard() {
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [incidents, setIncidents] = useState([]);
  const [activeCount, setActiveCount] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [statsRes, incidentsRes, activeRes] = await Promise.all([
        api.get('/api/statistics'),
        api.get('/api/incidents'),
        api.get('/api/incidents', { params: { status: '발생중' } })
      ]);
      setStats(statsRes.data);
      setIncidents(incidentsRes.data.slice(0, 5));
      setActiveCount(activeRes.data.length);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="p-8 text-center text-gray-400">로딩 중...</div>;

  const criticalCount = stats?.by_severity?.Critical || 0;

  const metrics = [
    { label: '전체 장애 건수', value: stats?.total_incidents || 0, color: 'text-blue-500' },
    { label: '발생중', value: activeCount, color: activeCount > 0 ? 'text-red-400' : 'text-green-400' },
    { label: '평균 다운타임', value: stats?.average_downtime ? `${Math.round(stats.average_downtime)}분` : '-', color: 'text-gray-100' },
    { label: 'Critical 건수', value: criticalCount, color: 'text-red-400' },
  ];

  return (
    <div className="max-w-6xl mx-auto p-6">
        {/* 실시간 장애 현황 배너 */}
        <div
          className={`mb-6 rounded-lg border px-5 py-4 flex items-center gap-3 ${
            activeCount > 0
              ? 'bg-red-500/10 border-red-500/30 text-red-400'
              : 'bg-green-500/10 border-green-500/30 text-green-400'
          }`}
        >
          <span className={`w-2.5 h-2.5 rounded-full ${activeCount > 0 ? 'bg-red-500 animate-pulse' : 'bg-green-500'}`} />
          <p className="text-sm font-medium">
            {activeCount > 0 ? `${activeCount}건의 장애가 진행 중입니다.` : '정상 운영 중입니다. 발생중인 장애가 없습니다.'}
          </p>
        </div>

        {/* 핵심 메트릭 카드 */}
        <div className="grid grid-cols-4 gap-6 mb-6">
          {metrics.map(m => (
            <div key={m.label} className="bg-gray-900 border border-gray-800 rounded-lg p-6 text-center">
              <p className="text-gray-400 text-sm mb-2">{m.label}</p>
              <p className={`text-3xl font-bold ${m.color}`}>{m.value}</p>
            </div>
          ))}
        </div>

        {/* 최근 장애 테이블 */}
        <div className="bg-gray-900 border border-gray-800 rounded-lg overflow-hidden">
          <div className="flex justify-between items-center px-6 py-4 border-b border-gray-800">
            <h2 className="text-lg font-bold text-gray-100">최근 장애</h2>
            <button onClick={() => navigate('/incidents')} className="text-blue-500 hover:text-blue-400 text-sm">전체 보기</button>
          </div>
          {incidents.length === 0 ? (
            <p className="text-gray-400 text-center py-8">장애 내역이 없습니다.</p>
          ) : (
            <table className="w-full">
              <thead className="bg-black/20">
                <tr>
                  <th className="px-6 py-3 text-left text-sm font-medium text-gray-400">발생일</th>
                  <th className="px-6 py-3 text-left text-sm font-medium text-gray-400">제목</th>
                  <th className="px-6 py-3 text-left text-sm font-medium text-gray-400">심각도</th>
                  <th className="px-6 py-3 text-left text-sm font-medium text-gray-400">상태</th>
                </tr>
              </thead>
              <tbody>
                {incidents.map(inc => (
                  <tr
                    key={inc.id}
                    onClick={() => navigate(`/incidents/${inc.id}/postmortem`)}
                    className="border-t border-gray-800 hover:bg-gray-800/50 cursor-pointer transition-colors"
                  >
                    <td className="px-6 py-3 text-sm text-gray-300">{new Date(inc.started_at).toLocaleDateString('ko-KR')}</td>
                    <td className="px-6 py-3 text-sm font-medium text-gray-100">{inc.title}</td>
                    <td className="px-6 py-3"><SeverityBadge severity={inc.severity} /></td>
                    <td className="px-6 py-3"><StatusBadge status={inc.status} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
    </div>
  );
}

export default Dashboard;
