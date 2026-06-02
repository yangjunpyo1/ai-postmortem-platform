import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';
import useAuth from '../hooks/useAuth';

function IncidentList() {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [severity, setSeverity] = useState('');
  const [category, setCategory] = useState('');
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [newIncident, setNewIncident] = useState({
    title: '',
    severity: 'Critical',
    category: '서버',
    started_at: new Date().toISOString().slice(0, 16)
  });
  const [submitting, setSubmitting] = useState(false);

  const fetchIncidents = async () => {
    setLoading(true);
    try {
      const params = { page };
      if (severity) params.severity = severity;
      if (category) params.category = category;
      const res = await api.get('/api/incidents', { params });
      setIncidents(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchIncidents();
  }, [page, severity, category]);

  const handleSubmit = async () => {
    setSubmitting(true);
    try {
      await api.post('/api/incidents', {
        ...newIncident,
        started_at: new Date(newIncident.started_at).toISOString()
      });
      setShowModal(false);
      setNewIncident({
        title: '',
        severity: 'Critical',
        category: '서버',
        started_at: new Date().toISOString().slice(0, 16)
      });
      fetchIncidents();
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  const getSeverityBadge = (sev) => {
    const styles = {
      Critical: 'bg-red-100 text-red-800',
      Warning: 'bg-yellow-100 text-yellow-800',
      Info: 'bg-green-100 text-green-800',
    };
    const icons = { Critical: '🔴', Warning: '🟡', Info: '🟢' };
    return (
      <span className={`px-2 py-1 rounded text-xs font-medium ${styles[sev] || 'bg-gray-100'}`}>
        {icons[sev]} {sev}
      </span>
    );
  };

  const filteredIncidents = incidents.filter(inc =>
    search ? inc.title.toLowerCase().includes(search.toLowerCase()) : true
  );

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-bold">AI Postmortem Platform</h1>
        <div className="flex gap-4">
          <button onClick={() => navigate('/dashboard')} className="text-gray-600 hover:text-blue-600">대시보드</button>
          <button onClick={() => navigate('/statistics')} className="text-gray-600 hover:text-blue-600">통계</button>
          <button onClick={logout} className="text-red-600 hover:text-red-800">로그아웃</button>
        </div>
      </nav>

      <div className="max-w-6xl mx-auto p-6">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold">장애 목록</h2>
          <button
            onClick={() => setShowModal(true)}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            장애 등록
          </button>
        </div>

        {/* 장애 등록 모달 */}
        {showModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg shadow-lg p-6 w-full max-w-md">
              <h3 className="text-xl font-bold mb-4">장애 등록</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">장애 제목</label>
                  <input
                    type="text"
                    value={newIncident.title}
                    onChange={(e) => setNewIncident({...newIncident, title: e.target.value})}
                    className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="장애 제목 입력"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">심각도</label>
                  <select
                    value={newIncident.severity}
                    onChange={(e) => setNewIncident({...newIncident, severity: e.target.value})}
                    className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="Critical">🔴 Critical</option>
                    <option value="Warning">🟡 Warning</option>
                    <option value="Info">🟢 Info</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">카테고리</label>
                  <select
                    value={newIncident.category}
                    onChange={(e) => setNewIncident({...newIncident, category: e.target.value})}
                    className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="서버">서버</option>
                    <option value="DB">DB</option>
                    <option value="네트워크">네트워크</option>
                    <option value="애플리케이션">애플리케이션</option>
                    <option value="기타">기타</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">발생 시각</label>
                  <input
                    type="datetime-local"
                    value={newIncident.started_at}
                    onChange={(e) => setNewIncident({...newIncident, started_at: e.target.value})}
                    className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
              <div className="flex gap-2 mt-6">
                <button
                  onClick={handleSubmit}
                  disabled={submitting || !newIncident.title}
                  className="flex-1 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
                >
                  {submitting ? '등록 중...' : '등록'}
                </button>
                <button
                  onClick={() => setShowModal(false)}
                  className="flex-1 border px-4 py-2 rounded hover:bg-gray-100"
                >
                  취소
                </button>
              </div>
            </div>
          </div>
        )}

        {/* 필터링 */}
        <div className="bg-white p-4 rounded-lg shadow mb-6 flex gap-4 flex-wrap">
          <input
            type="text"
            placeholder="장애 검색..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="border rounded px-3 py-2 flex-1 min-w-48"
          />
          <select
            value={severity}
            onChange={(e) => { setSeverity(e.target.value); setPage(1); }}
            className="border rounded px-3 py-2"
          >
            <option value="">전체 심각도</option>
            <option value="Critical">🔴 Critical</option>
            <option value="Warning">🟡 Warning</option>
            <option value="Info">🟢 Info</option>
          </select>
          <select
            value={category}
            onChange={(e) => { setCategory(e.target.value); setPage(1); }}
            className="border rounded px-3 py-2"
          >
            <option value="">전체 카테고리</option>
            <option value="DB">DB</option>
            <option value="네트워크">네트워크</option>
            <option value="서버">서버</option>
            <option value="애플리케이션">애플리케이션</option>
            <option value="기타">기타</option>
          </select>
        </div>

        {/* 목록 */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          {loading ? (
            <div className="p-8 text-center text-gray-500">로딩 중...</div>
          ) : filteredIncidents.length === 0 ? (
            <div className="p-8 text-center text-gray-500">장애 내역이 없습니다.</div>
          ) : (
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">발생일</th>
                  <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">제목</th>
                  <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">심각도</th>
                  <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">카테고리</th>
                  <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">상태</th>
                  <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">다운타임</th>
                </tr>
              </thead>
              <tbody>
                {filteredIncidents.map(inc => (
                  <tr
                    key={inc.id}
                    onClick={() => navigate(`/incidents/${inc.id}/postmortem`)}
                    className="border-t hover:bg-gray-50 cursor-pointer"
                  >
                    <td className="px-4 py-3 text-sm">{new Date(inc.started_at).toLocaleDateString('ko-KR')}</td>
                    <td className="px-4 py-3 text-sm font-medium">{inc.title}</td>
                    <td className="px-4 py-3">{getSeverityBadge(inc.severity)}</td>
                    <td className="px-4 py-3 text-sm">{inc.category}</td>
                    <td className="px-4 py-3 text-sm">{inc.status}</td>
                    <td className="px-4 py-3 text-sm">{inc.downtime ? `${inc.downtime.toFixed(0)}분` : '-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        {/* 페이지네이션 */}
        <div className="flex justify-center gap-2 mt-6">
          <button
            onClick={() => setPage(p => Math.max(1, p - 1))}
            disabled={page === 1}
            className="px-4 py-2 border rounded disabled:opacity-50 hover:bg-gray-100"
          >
            이전
          </button>
          <span className="px-4 py-2">{page}</span>
          <button
            onClick={() => setPage(p => p + 1)}
            disabled={filteredIncidents.length === 0}
            className="px-4 py-2 border rounded disabled:opacity-50 hover:bg-gray-100"
          >
            다음
          </button>
        </div>
      </div>
    </div>
  );
}

export default IncidentList;