import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Auth.css';

const Register = () => {
  const [username, setUsername] = useState(''); // Поле для имени пользователя
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState(''); // Выбранная роль
  const [roles, setRoles] = useState([]); // Список ролей
  const [error, setError] = useState('');
  const navigate = useNavigate();

  // Функция для получения списка ролей
  const fetchRoles = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/roles/');
      setRoles(response.data); // Установить роли из ответа
    } catch (err) {
      setError('Не удалось получить список ролей.');
    }
  };

  useEffect(() => {
    fetchRoles(); // Загружаем роли при монтировании компонента
  }, []);

  const handleRegister = async (e) => {
    e.preventDefault();

    try {
      const userData = { username, email, password, role }; // Формируем данные для отправки
      const response = await axios.post('http://127.0.0.1:8000/register', userData);
      
      if (response.status === 201) {
        alert('Регистрация прошла успешно!');
        navigate('/login'); // Перенаправление на страницу входа после регистрации
      }
    } catch (err) {
      if (err.response && err.response.data) {
        setError(err.response.data.message || 'Произошла ошибка при регистрации.');
      } else {
        setError('Произошла ошибка при регистрации.');
      }
    }
  };

  return (
    <div className='register-form'>
      <h1>Регистрация</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form className='auth-form' onSubmit={handleRegister}>
        <input
          className='auth-input'
          type="text"
          placeholder="Имя пользователя"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
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
        <select className='auth-select' value={role} onChange={(e) => setRole(e.target.value)} required>
          <option value="">Выберите роль</option>
          {roles.map((roleOption) => (
            <option key={roleOption.id} value={roleOption.name}>
              {roleOption.name}
            </option>
          ))}
        </select>
        <button className='register-button' type="submit">Зарегистрироваться</button>        
      </form>
    </div>
  );
};

export default Register;