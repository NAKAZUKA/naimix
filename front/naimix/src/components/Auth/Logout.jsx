import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Logout = () => {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await axios.post('http://127.0.0.1:8000/logout', {}, { withCredentials: true });
      alert('Вы успешно вышли из системы.');
      localStorage.removeItem('role'); // Удаляем сохраненную роль
      navigate('/login');
    } catch (err) {
      console.error('Ошибка при выходе:', err.response?.data || err.message);
      alert('Произошла ошибка при выходе.');
    }
  };

  return <button onClick={handleLogout}>Выйти</button>;
};

export default Logout;