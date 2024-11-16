import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';

const CheckSession = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const verifySession = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/session', {
          withCredentials: true,
        });
        console.log('Текущая сессия:', response.data);
      } catch (err) {
        console.error('Ошибка проверки сессии:', err.response?.data || err.message);
        navigate('/login'); // Перенаправляем на логин при ошибке
      }
    };

    verifySession();
  }, [navigate]);

  return null;
};

export default CheckSession;