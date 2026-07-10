const KST_OFFSET_MS = 9 * 60 * 60 * 1000;

function toKSTDate(dateInput) {
  return new Date(new Date(dateInput).getTime() + KST_OFFSET_MS);
}

export function formatKSTDateTime(dateInput) {
  return toKSTDate(dateInput).toLocaleString('ko-KR', { timeZone: 'UTC' });
}

export function formatKSTDate(dateInput) {
  return toKSTDate(dateInput).toLocaleDateString('ko-KR', { timeZone: 'UTC' });
}
