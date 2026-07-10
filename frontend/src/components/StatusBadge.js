import React from 'react';

function StatusBadge({ status }) {
  const active = status === '발생중';
  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2 py-1 rounded text-xs font-medium ${
        active ? 'bg-red-500/10 text-red-400' : 'bg-green-500/10 text-green-400'
      }`}
    >
      <span className={`w-1.5 h-1.5 rounded-full ${active ? 'bg-red-500 animate-pulse' : 'bg-green-500'}`} />
      {status}
    </span>
  );
}

export default StatusBadge;
