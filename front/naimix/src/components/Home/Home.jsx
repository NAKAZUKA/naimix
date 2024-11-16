import React, { useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';
import JobTable from '../JobTable/JobTable.jsx';
import { ways } from '../JobTable/data.js';
import { SurveyContext } from '../SurveyForm/SurveyContext.jsx';

export default function Home() {
  const navigate = useNavigate();
  const { surveyData } = useContext(SurveyContext);

  // Проверка локального хранилища и роли пользователя
  useEffect(() => {
    const storedUser = JSON.parse(localStorage.getItem('user'));
    
    if (!storedUser || storedUser.role !== 'кандидат') {
      navigate('/login');
    }
  }, [navigate]);

  const handleClick = (specialty) => {
    navigate('/surveyform', { state: { specialty } });
  };

  const storedUser = JSON.parse(localStorage.getItem('user'));

  return (
    <div>
      {storedUser ? (
        <>
          <h1>Добро пожаловать, {storedUser.fullName || 'кандидат'}!</h1>
          <p>Это ваша домашняя страница.</p>
          <h2>Выберите желаемую специальность</h2>
          <div className='tables'>
            {ways.map((way, index) => (
              <div key={index}>
                <JobTable key={index} name={way.name} description={way.description} />
                <button onClick={() => handleClick(way.name)}>Заполнить анкету</button>
              </div>
            ))}
          </div>
        </>
      ) : (
        <p>Загрузка...</p>
      )}
    </div>
  );
}