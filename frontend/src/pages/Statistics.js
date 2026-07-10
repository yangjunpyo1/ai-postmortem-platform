import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import api from '../api/axios';
import useAuth from '../hooks/useAuth';

const COLORS = ['#ef4444', '#f59e0b', '#22c55e', '#3b82f6', '#8b5cf6'];

function Statistics() {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    setLoading(true);
    try {
      const res = await api.get('/api/statistics');
      setStats(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const severityData = stats ? Object.entries(stats.by_severity).map(([name, value]) => ({ name, value })) : [];
  const categoryData = stats ? Object.entries(stats.by_category).map(([name, value]) => ({ name, value })) : [];

  if (loading) return <div className="min-h-screen bg-gray-900 p-8 text-center text-gray-400">로딩 중...</div>;

  const chartTooltipStyle = { backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '6px', color: '#f3f4f6' };
  const chartLegendStyle = { color: '#9ca3af' };

  return (
    <div className="min-h-screen bg-gray-900">
      <nav className="bg-gray-800 border-b border-gray-700 px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-gray-100 cursor-pointer" onClick={() => navigate('/dashboard')}>AI Postmortem Platform</h1>
        <div className="flex gap-4">
          <button onClick={() => navigate('/dashboard')} className="text-gray-400 hover:text-blue-400 transition-colors">대시보드</button>
          <button onClick={() => navigate('/incidents')} className="text-gray-400 hover:text-blue-400 transition-colors">장애 목록</button>
          <button onClick={logout} className="text-red-400 hover:text-red-300 transition-colors">로그아웃</button>
        </div>
      </nav>

      <div className="max-w-6xl mx-auto p-6">
        <h2 className="text-2xl font-bold text-gray-100 mb-6">통계</h2>

        <div className="grid grid-cols-2 gap-6 mb-6">
          <div className="bg-gray-800 border border-gray-700 rounded-lg p-6 text-center">
            <p className="text-gray-400 text-sm mb-2">전체 장애 건수</p>
            <p className="text-4xl font-bold text-blue-500">{stats?.total_incidents || 0}</p>
          </div>
          <div className="bg-gray-800 border border-gray-700 rounded-lg p-6 text-center">
            <p className="text-gray-400 text-sm mb-2">평균 다운타임</p>
            <p className="text-4xl font-bold text-red-400">
              {stats?.average_downtime ? `${stats.average_downtime.toFixed(0)}분` : '-'}
            </p>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-6">
          <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-gray-100 mb-4">심각도별 장애 건수</h3>
            {severityData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie data={severityData} cx="50%" cy="50%" outerRadius={100} dataKey="value" label={({ name, value }) => `${name}: ${value}`}>
                    {severityData.map((entry, index) => (
                      <Cell key={index} fill={COLORS[index % COLORS.length]} stroke="#1f2937" />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={chartTooltipStyle} itemStyle={{ color: '#f3f4f6' }} />
                  <Legend wrapperStyle={chartLegendStyle} />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-center text-gray-400 py-8">데이터 없음</p>
            )}
          </div>

          <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-gray-100 mb-4">카테고리별 장애 건수</h3>
            {categoryData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={categoryData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="name" tick={{ fill: '#9ca3af' }} />
                  <YAxis tick={{ fill: '#9ca3af' }} />
                  <Tooltip contentStyle={chartTooltipStyle} itemStyle={{ color: '#f3f4f6' }} cursor={{ fill: 'rgba(255,255,255,0.05)' }} />
                  <Legend wrapperStyle={chartLegendStyle} />
                  <Bar dataKey="value" fill="#3b82f6" name="장애 건수" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-center text-gray-400 py-8">데이터 없음</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Statistics;