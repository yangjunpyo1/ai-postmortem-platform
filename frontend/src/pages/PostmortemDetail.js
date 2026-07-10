import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api/axios';
import SeverityBadge from '../components/SeverityBadge';
import StatusBadge from '../components/StatusBadge';

const Field = ({ label, field, multiline, editing, editData, setEditData, postmortem }) => (
  <div className="mb-4">
    <label className="block text-sm font-semibold text-gray-400 mb-1">{label}</label>
    {editing ? (
      multiline ? (
        <textarea
          value={editData[field] || ''}
          onChange={(e) => setEditData(prev => ({ ...prev, [field]: e.target.value }))}
          className="w-full bg-gray-950 border border-gray-700 text-gray-100 rounded px-3 py-2 text-sm h-32 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      ) : (
        <input
          type="text"
          value={editData[field] || ''}
          onChange={(e) => setEditData(prev => ({ ...prev, [field]: e.target.value }))}
          className="w-full bg-gray-950 border border-gray-700 text-gray-100 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      )
    ) : (
      <p className="text-sm text-gray-100 whitespace-pre-wrap">{postmortem?.[field] || '-'}</p>
    )}
  </div>
);

function PostmortemDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
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
      const [incRes, simRes] = await Promise.all([
        api.get(`/api/incidents/${id}`),
        api.get(`/api/incidents/${id}/similar`)
      ]);
      setIncident(incRes.data);
      setSimilar(simRes.data);

      try {
        const postRes = await api.get(`/api/incidents/${id}/postmortem`);
        setPostmortem(postRes.data);
        setEditData(postRes.data);
      } catch (postErr) {
        setPostmortem(null);
        setEditData({});
      }
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

  if (loading) return <div className="p-8 text-center text-gray-400">로딩 중...</div>;

  return (
    <div className="max-w-6xl mx-auto p-6 grid grid-cols-3 gap-6 items-start">
        {/* 왼쪽: 장애 메타정보 */}
        <div className="col-span-1 space-y-6 sticky top-6">
          {incident && (
            <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
              <h2 className="text-lg font-bold text-gray-100 mb-4">{incident.title}</h2>
              <div className="flex gap-2 mb-4">
                <SeverityBadge severity={incident.severity} />
                <StatusBadge status={incident.status} />
              </div>
              <dl className="space-y-3 text-sm">
                <div>
                  <dt className="text-gray-400">발생 시각</dt>
                  <dd className="text-gray-100">{new Date(incident.started_at).toLocaleString('ko-KR')}</dd>
                </div>
                <div>
                  <dt className="text-gray-400">종료 시각</dt>
                  <dd className="text-gray-100">{incident.ended_at ? new Date(incident.ended_at).toLocaleString('ko-KR') : '-'}</dd>
                </div>
                <div>
                  <dt className="text-gray-400">다운타임</dt>
                  <dd className="text-gray-100">{incident.downtime ? `${incident.downtime.toFixed(0)}분` : '-'}</dd>
                </div>
                <div>
                  <dt className="text-gray-400">카테고리</dt>
                  <dd className="text-gray-100">{incident.category}</dd>
                </div>
              </dl>
            </div>
          )}

          {similar.length > 0 && (
            <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
              <h3 className="text-sm font-bold text-gray-100 mb-4">유사 장애</h3>
              <div className="space-y-3">
                {similar.map(inc => (
                  <div
                    key={inc.id}
                    onClick={() => navigate(`/incidents/${inc.id}/postmortem`)}
                    className="border border-gray-800 rounded p-3 hover:bg-gray-800/50 cursor-pointer transition-colors"
                  >
                    <p className="font-medium text-sm text-gray-100">{inc.title}</p>
                    <p className="text-xs text-gray-400 mt-1">{inc.severity} · {inc.category} · {new Date(inc.started_at).toLocaleDateString('ko-KR')}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* 오른쪽: Postmortem 섹션 */}
        <div className="col-span-2">
          <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-bold text-gray-100">Postmortem 문서</h3>
              <div className="flex gap-2">
                {editing ? (
                  <>
                    <button
                      onClick={handleSave}
                      disabled={saving}
                      className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-500 disabled:opacity-50"
                    >
                      {saving ? '저장 중...' : '저장'}
                    </button>
                    <button
                      onClick={() => { setEditing(false); setEditData(postmortem); }}
                      className="border border-gray-700 text-gray-300 px-4 py-2 rounded hover:bg-gray-800"
                    >
                      취소
                    </button>
                  </>
                ) : (
                  <button
                    onClick={() => setEditing(true)}
                    className="bg-gray-800 text-gray-100 px-4 py-2 rounded hover:bg-gray-700"
                  >
                    수정
                  </button>
                )}
              </div>
            </div>

            {postmortem ? (
              <>
                <Field label="장애 요약" field="summary" multiline editing={editing} editData={editData} setEditData={setEditData} postmortem={postmortem} />
                <Field label="타임라인" field="timeline" multiline editing={editing} editData={editData} setEditData={setEditData} postmortem={postmortem} />
                <Field label="근본 원인 분석" field="root_cause" multiline editing={editing} editData={editData} setEditData={setEditData} postmortem={postmortem} />
                <Field label="해결 방법" field="resolution" multiline editing={editing} editData={editData} setEditData={setEditData} postmortem={postmortem} />
                <Field label="재발 방지 대책" field="prevention" multiline editing={editing} editData={editData} setEditData={setEditData} postmortem={postmortem} />
                <Field label="영향 범위" field="affected_range" multiline editing={editing} editData={editData} setEditData={setEditData} postmortem={postmortem} />
                <Field label="담당자" field="assignee" editing={editing} editData={editData} setEditData={setEditData} postmortem={postmortem} />
                <Field label="유사 장애 히스토리" field="similar_incidents" multiline editing={editing} editData={editData} setEditData={setEditData} postmortem={postmortem} />
              </>
            ) : (
              <p className="text-gray-400 text-center py-8">Postmortem 문서가 생성 중입니다. /resolve 명령어로 생성할 수 있습니다.</p>
            )}
          </div>
        </div>
    </div>
  );
}

export default PostmortemDetail;
