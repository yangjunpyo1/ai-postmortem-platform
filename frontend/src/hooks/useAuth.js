import { useNavigate } from 'react-router-dom';

function useAuth() {
  const navigate = useNavigate();

  const isAuthenticated = () => {
    return !!localStorage.getItem('access_token');
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    navigate('/login');
  };

  return { isAuthenticated, logout };
}

export default useAuth;