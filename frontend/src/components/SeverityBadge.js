import React from 'react';

const STYLES = {
  Critical: { dot: 'bg-red-500', text: 'text-red-400', bg: 'bg-red-500/10' },
  Warning: { dot: 'bg-yellow-500', text: 'text-yellow-400', bg: 'bg-yellow-500/10' },
  Info: { dot: 'bg-green-500', text: 'text-green-400', bg: 'bg-green-500/10' },
};

function SeverityBadge({ severity }) {
  const s = STYLES[severity] || { dot: 'bg-gray-500', text: 'text-gray-400', bg: 'bg-gray-500/10' };
  return (
    <span className={`inline-flex items-center gap-1.5 px-2 py-1 rounded text-xs font-medium ${s.bg} ${s.text}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${s.dot}`} />
      {severity}
    </span>
  );
}

export default SeverityBadge;
