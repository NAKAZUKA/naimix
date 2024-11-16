import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Auth.css';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [roles, setRoles] = useState([]); // Для хранения ролей с сервера
  const navigate = useNavigate();

  // Получение ролей с сервера при загрузке компонента
  useEffect(() => {
    const fetchRoles = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/roles/');
        setRoles(response.data.map((role) => role.name)); // Сохраняем только названия ролей
      } catch (err) {
        console.error('Ошибка при получении ролей:', err.response?.data || err.message);
        setError('Не удалось загрузить роли. Попробуйте позже.');
      }
    };

    fetchRoles();
  }, []);

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
          withCredentials: true, // Для отправки cookie с сессией
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      if (response.status === 200) {
        const user = response.data;

        // Проверяем роль пользователя
        if (roles.includes(user.role)) {
          // Сохраняем роль в localStorage
          localStorage.setItem('role', user.role);

          // Перенаправление на страницу в зависимости от роли
          if (user.role === 'hr') {
            navigate('/swiper'); // Для HR
          } else if (user.role === 'кандидат') {
            navigate('/home'); // Для кандидата
          } else if (user.role === 'сотрудник') {
            navigate('/dashboard'); // Для сотрудника
          } else {
            navigate('/'); // Дефолтное перенаправление
          }
        } else {
          setError('Получена недействительная роль пользователя.');
          throw new Error('Роль пользователя не соответствует списку доступных ролей.');
        }
      }
    } catch (err) {
      console.error('Ошибка входа:', err);

      if (err.response) {
        console.error('Ответ сервера с ошибкой:', err.response.data);
        setError(err.response.data.detail || 'Неверные учетные данные. Попробуйте снова.');
      } else if (err.request) {
        console.error('Ошибка запроса:', err.request);
        setError('Сервер не отвечает. Проверьте соединение.');
      } else {
        console.error('Неизвестная ошибка:', err.message);
        setError('Произошла ошибка при входе. Попробуйте снова.');
      }
    }
  };

  return (
    <div>
      <h1>Вход</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form className="auth-form" onSubmit={handleLogin}>
        <input
          className="auth-input"
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          className="auth-input"
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