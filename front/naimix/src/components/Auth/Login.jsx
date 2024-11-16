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

    // Валидация email
    if (!email.includes('@')) {
      setError('Введите корректный email.');
      return;
    }

    try {
      const response = await axios.post(
        'http://127.0.0.1:8000/login',
        { email, password },
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      // Проверяем успешный ответ
      if (response.status === 200) {
        const user = response.data;

        // Сохраняем токен в localStorage
        localStorage.setItem('token', user.token); // Рекомендуется сохранять только токен

        // Переход на страницу в зависимости от роли
        if (user.role === 'hr') {
          navigate('/swiper'); // Для HR
        } else if (user.role === 'candidate') {
          navigate('/home'); // Для кандидата
        } else {
          navigate('/'); // Дефолтное перенаправление
        }
      }
    } catch (err) {
      console.error(err.response  err.message  'Unknown error'); // Логируем ошибку
      if (err.response && err.response.data) {
        setError(err.response.data.detail || 'Неверные учетные данные. Пожалуйста, попробуйте снова.');
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