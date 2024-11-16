import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios'; // Импортируем axios для работы с HTTP-запросами
import './Auth.css';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://127.0.0.1:8000/login', { email, password }); // Отправляем данные на сервер
      const user = response.data; // Предполагаем, что сервер возвращает информацию о пользователе

      // Сохраняем пользователя в локальном хранилище
      localStorage.setItem('user', JSON.stringify(user));
      
      // Перенаправление в зависимости от роли
      if (user.role === 'hr') {
        navigate('/swiper'); // Перенаправление для HR
      } else if (user.role === 'candidate') {
        navigate('/home'); // Перенаправление для кандидата
      }
    } catch (err) {
      if (err.response && err.response.data) {
        setError(err.response.data.message || 'Неверные учетные данные. Пожалуйста, попробуйте снова.');
      } else {
        setError('Произошла ошибка при входе. Пожалуйста, попробуйте снова.');
      }
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