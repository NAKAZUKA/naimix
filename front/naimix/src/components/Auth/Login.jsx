import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Auth.css';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    const existingUsers = JSON.parse(localStorage.getItem('users')) || [];

    // Проверка существующего пользователя
    const user = existingUsers.find(user => user.email === email && user.password === password);

    if (user) {
      // Сохраняем пользователя в локальном хранилище
      localStorage.setItem('user', JSON.stringify(user));
      
      // Перенаправление в зависимости от роли
      if (user.role === 'hr') {
        navigate('/swiper'); // Перенаправление для HR
      } else if (user.role === 'candidate') {
        navigate('/home'); // Перенаправление для кандидата
      }
    } else {
      setError('Неверные учетные данные. Пожалуйста, попробуйте снова.');
    }
  };

  return (
    <div>
      <h1>Вход</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form className='auth-form' onSubmit={handleLogin}>
        <input 
          className='auth-input'
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          className='auth-input'
          type="password"
          placeholder="Пароль"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Войти</button>
      </form>
    </div>
  );
};

export default Login;