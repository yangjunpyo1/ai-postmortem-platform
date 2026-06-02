import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import IncidentList from './pages/IncidentList';
import PostmortemDetail from './pages/PostmortemDetail';
import Statistics from './pages/Statistics';
import PrivateRoute from './components/PrivateRoute';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
        <Route path="/incidents" element={<PrivateRoute><IncidentList /></PrivateRoute>} />
        <Route path="/incidents/:id/postmortem" element={<PrivateRoute><PostmortemDetail /></PrivateRoute>} />
        <Route path="/statistics" element={<PrivateRoute><Statistics /></PrivateRoute>} />
        <Route path="/" element={<Navigate to="/dashboard" />} />
      </Routes>
    </Router>
  );
}

export default App;