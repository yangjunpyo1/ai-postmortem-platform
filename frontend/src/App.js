import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import IncidentList from './pages/IncidentList';
import PostmortemDetail from './pages/PostmortemDetail';
import Statistics from './pages/Statistics';
import PrivateRoute from './components/PrivateRoute';
import Layout from './components/Layout';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<PrivateRoute><Layout><Dashboard /></Layout></PrivateRoute>} />
        <Route path="/incidents" element={<PrivateRoute><Layout><IncidentList /></Layout></PrivateRoute>} />
        <Route path="/incidents/:id/postmortem" element={<PrivateRoute><Layout><PostmortemDetail /></Layout></PrivateRoute>} />
        <Route path="/statistics" element={<PrivateRoute><Layout><Statistics /></Layout></PrivateRoute>} />
        <Route path="/" element={<Navigate to="/dashboard" />} />
      </Routes>
    </Router>
  );
}

export default App;