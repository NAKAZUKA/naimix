import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Auth.css'; // Подключение стилей

const AuthPage = () => {
  const navigate = useNavigate();

  return (
    <div className="auth-container">
      <h1 className="auth-title">NAIMIX FREELANCE</h1>
      <p className="auth-description">войдите или зарегистрируйтесь</p>
      <div className="auth-buttons">
        <button className="auth-button" onClick={() => navigate('/login')}>Вход</button>
        <button className="auth-button" onClick={() => navigate('/register')}>Регистрация</button>
      </div>
    </div>
  );
};

export default AuthPage;