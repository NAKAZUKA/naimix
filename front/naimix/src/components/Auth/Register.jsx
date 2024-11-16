import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Auth.css';

const Register = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('');
  const [roles, setRoles] = useState([]);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const fetchRoles = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/roles/');
      setRoles(response.data);
    } catch (err) {
      setError('Не удалось получить список ролей.');
    }
  };

  useState(() => {
    fetchRoles();
  }, []);

  const handleRegister = async (e) => {
    e.preventDefault();

    try {
      // Регистрация пользователя
      await axios.post('http://127.0.0.1:8000/register', {
        username,
        email,
        password,
        role,
      });

      // Автоматический вход
      const loginResponse = await axios.post(
        'http://127.0.0.1:8000/login',
        { email, password },
        {
          withCredentials: true,
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      if (loginResponse.status === 200) {
        const user = loginResponse.data;

        if (user.role) {
          localStorage.setItem('role', user.role);
          navigate(user.role === 'hr' ? '/swiper' : user.role === 'кандидат' ? '/home' : '/');
        } else {
          throw new Error('Сервер не вернул роль пользователя.');
        }
      }
    } catch (err) {
      setError(
        err.response?.data?.detail || 'Ошибка при регистрации/авторизации. Попробуйте снова.'
      );
    }
  };

  return (
    <div>
      <h1>Регистрация</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form className="auth-form" onSubmit={handleRegister}>
        <input
          className="auth-input"
          type="text"
          placeholder="Имя пользователя"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
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
        <select
          className="auth-select"
          value={role}
          onChange={(e) => setRole(e.target.value)}
          required
        >
          <option value="">Выберите роль</option>
          {roles.map((roleOption) => (
            <option key={roleOption.id} value={roleOption.name}>
              {roleOption.name}
            </option>
          ))}
        </select>
        <button type="submit">Зарегистрироваться</button>
      </form>
    </div>
  );
};

export default Register;