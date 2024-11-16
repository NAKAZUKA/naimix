import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Auth.css';

const Register = () => {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('candidate'); // По умолчанию кандидат
  const [category, setCategory] = useState(''); // Категория для HR
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    
    try {
      const userData = { fullName, email, password, role, category };
      const response = await axios.post('http://localhost:8000/register', userData);
      
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
          placeholder="ФИО"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
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
        <select className='auth-select' value={role} onChange={(e) => setRole(e.target.value)}>
          <option value="candidate">Кандидат</option>
          <option value="hr">HR</option>
        </select>
        {role === 'hr' && (
          <select value={category} onChange={(e) => setCategory(e.target.value)} required>
            <option value="">Выберите категорию</option>
            <option value="frontend">Frontend</option>
            <option value="backend">Backend</option>
            <option value="qa">QA</option>
            <option value="test">Test</option>
          </select>
        )}
        <button className='register-button' type="submit">Зарегистрироваться</button>        
      </form>
    </div>
  );
};

export default Register;