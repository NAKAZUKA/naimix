// Home.jsx
import React, { useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './Home.css';
import JobTable from '../JobTable/JobTable.jsx';
import { ways } from '../JobTable/data.js';
import { SurveyContext } from '../SurveyForm/SurveyContext.jsx';

export default function Home() {
  const navigate = useNavigate();
  const { surveyData } = useContext(SurveyContext);

  const handleClick = (specialty) => {
    navigate('/surveyform', { state: {specialty}});
  };

  const storedUser = JSON.parse(localStorage.getItem('user'));
  
  // Проверяем, является ли пользователь кандидатом
  if (!storedUser || storedUser.role !== 'candidate') {
    navigate('/login');
    return null;
  }


  return (
    <div>
      <h1>Добро пожаловать, {storedUser.fullName}!</h1>
      <p>Это ваша домашняя страница.</p>
      <h2>Выберите желаемую специальность</h2>
      {/* <Link to="/swiper">
        <button className='swiper'>Свайпер</button>
      </Link> */}
      <div className='tables'>
        {ways.map((way, index) => (
          <div key={index}>
            <JobTable key={index} name={way.name} description={way.description} />
            <button onClick={() => handleClick(way.name)}>Заполнить анкету</button>
          </div>
        ))}
      </div>

      {/* <h3>Сохраненные данные:</h3>
      {surveyData.length > 0 ? (
        <ul>
          {surveyData.map((data, index) => (
            <li key={index}>
              {data.name} - {data.email} - {data.age} - {data.feedback}
            </li>
          ))}
        </ul>
      ) : (
        <p>Нет сохраненных данных</p>
      )} */}
    </div>
  );
}