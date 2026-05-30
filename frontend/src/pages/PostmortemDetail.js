import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api/axios';
import useAuth from '../hooks/useAuth';

function PostmortemDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { logout } = useAuth();
  const [incident, setIncident] = useState(null);
  const [postmortem, setPostmortem] = useState(null);
  const [similar, setSimilar] = useState([]);
  const [editing, setEditing] = useState(false);
  const [editData, setEditData] = useState({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    fetchData();
  }, [id]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [incRes, postRes, simRes] = await Promise.all([
        api.get(`/api/incidents/${id}`),
        api.get(`/api/incidents/${id}/postmortem`),
        api.get(`/api/incidents/${id}/similar`)
      ]);
      setIncident(incRes.data);
      setPostmortem(postRes.data);
      setEditData(postRes.data);
      setSimilar(simRes.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await api.put(`/api/incidents/${id}/postmortem`, editData);
      setPostmortem(editData);
      setEditing(false);
    } catch (err) {
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  const Field = ({ label, field, multiline }) => (
    <div className="mb-4">
      <label className="block text-sm font-semibold text-gray-600 mb-1">{label}</label>
      {editing ? (
        multiline ? (
          <textarea
            value={editData[field] || ''}
            onChange={(e) => setEditData({ ...editData, [field]: e.target.value })}
            className="w-full border rounded px-3 py-2 text-sm h-32 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        ) : (
          <input
            type="text"
            value={editData[field] || ''}
            onChange={(e) => setEditData({ ...editData, [field]: e.target.value })}
            className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        )
      ) : (
        <p className="text-sm text-gray-800 whitespace-pre-wrap">{postmortem?.[field] || '-'}</p>
      )}
    </div>
  );

  if (loading) return <div className="p-8 text-center">로딩 중...</div>;

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-bold">AI Postmortem Platform</h1>
        <div className="flex gap-4">
          <button onClick={() => navigate('/incidents')} className="text-gray-600 hover:text-blue-600">장애 목록</button>
          <button onClick={() => navigate('/statistics')} className="text-gray-600 hover:text-blue-600">통계</button>
          <button onClick={logout} className="text-red-600 hover:text-red-800">로그아웃</button>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto p-6">
        {/* 장애 기본 정보 */}
        {incident && (
          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <h2 className="text-2xl font-bold mb-4">{incident.title}</h2>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div><span className="font-medium">발생 시각:</span> {new Date(incident.started_at).toLocaleString('ko-KR')}</div>
              <div><span className="font-medium">종료 시각:</span> {incident.ended_at ? new Date(incident.ended_at).toLocaleString('ko-KR') : '-'}</div>
              <div><span className="font-medium">다운타임:</span> {incident.downtime ? `${incident.downtime.toFixed(0)}분` : '-'}</div>
              <div><span className="font-medium">심각도:</span> {incident.severity}</div>
              <div><span className="font-medium">카테고리:</span> {incident.category}</div>
              <div><span className="font-medium">상태:</span> {incident.status}</div>
            </div>
          </div>
        )}

        {/* Postmortem 문서 */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-xl font-bold">Postmortem 문서</h3>
            <div className="flex gap-2">
              {editing ? (
                <>
                  <button
                    onClick={handleSave}
                    disabled={saving}
                    className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
                  >
                    {saving ? '저장 중...' : '저장'}
                  </button>
                  <button
                    onClick={() => { setEditing(false); setEditData(postmortem); }}
                    className="border px-4 py-2 rounded hover:bg-gray-100"
                  >
                    취소
                  </button>
                </>
              ) : (
                <button
                  onClick={() => setEditing(true)}
                  className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
                >
                  수정
                </button>
              )}
            </div>
          </div>

          {postmortem ? (
            <>
              <Field label="장애 요약" field="summary" multiline />
              <Field label="타임라인" field="timeline" multiline />
              <Field label="근본 원인 분석" field="root_cause" multiline />
              <Field label="해결 방법" field="resolution" multiline />
              <Field label="재발 방지 대책" field="prevention" multiline />
              <Field label="영향 범위" field="affected_range" multiline />
              <Field label="담당자" field="assignee" />
              <Field label="유사 장애 히스토리" field="similar_incidents" multiline />
            </>
          ) : (
            <p className="text-gray-500 text-center py-8">Postmortem 문서가 없습니다.</p>
          )}
        </div>

        {/* 유사 장애 */}
        {similar.length > 0 && (
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-xl font-bold mb-4">유사 장애</h3>
            <div className="space-y-3">
              {similar.map(inc => (
                <div
                  key={inc.id}
                  onClick={() => navigate(`/incidents/${inc.id}/postmortem`)}
                  className="border rounded p-3 hover:bg-gray-50 cursor-pointer"
                >
                  <p className="font-medium">{inc.title}</p>
                  <p className="text-sm text-gray-500">{inc.severity} · {inc.category} · {new Date(inc.started_at).toLocaleDateString('ko-KR')}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default PostmortemDetail;