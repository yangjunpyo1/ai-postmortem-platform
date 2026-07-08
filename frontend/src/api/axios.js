import axios from 'axios';

// /config.json에서 API URL을 동적으로 로드 (배포 후 재빌드 없이 URL 변경 가능하도록)
// 로드 실패 시 REACT_APP_API_URL로 폴백
let apiUrlPromise = null;

function loadApiUrl() {
  if (!apiUrlPromise) {
    apiUrlPromise = fetch('/config.json')
      .then((res) => (res.ok ? res.json() : Promise.reject(new Error('config.json 로드 실패'))))
      .then((config) => config.REACT_APP_API_URL || process.env.REACT_APP_API_URL)
      .catch(() => process.env.REACT_APP_API_URL);
  }
  return apiUrlPromise;
}

const api = axios.create();

// 요청 인터셉터 - baseURL 동적 설정 및 JWT 토큰 자동 추가
api.interceptors.request.use(
  async (config) => {
    config.baseURL = await loadApiUrl();
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 응답 인터셉터 - 401 처리
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;