import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { useSpring, animated } from 'react-spring';
import { useGesture } from 'react-use-gesture';
import './Tinder.css';

export default function TinderSwiper() {
  const location = useLocation();
  const specialty = location.state?.specialty;
  const [surveyData, setSurveyData] = useState([]);
  const [currentCardIndex, setCurrentCardIndex] = useState(0);
  const [likedData, setLikedData] = useState([]);
  const [teamMembers, setTeamMembers] = useState([]);
  const [showTeam, setShowTeam] = useState(false);
  
  const [{ x, y, rotate, opacity }, set] = useSpring(() => ({ x: 0, y: 0, rotate: 0, opacity: 1 }));

  useEffect(() => {
    const storedData = localStorage.getItem('surveyData');
    const storedUser = JSON.parse(localStorage.getItem('user'));
    const userRole = storedUser ? storedUser.role : null;
    
    if (storedData) {
      const parsedData = JSON.parse(storedData);
      const filteredData = specialty
        ? parsedData.filter(data => data.specialty === specialty)
        : parsedData;

      setSurveyData(filteredData);
    }
  }, [specialty]);

  const handleLike = () => {
    if (currentCardIndex < surveyData.length) {
      const likedCard = surveyData[currentCardIndex];
      setLikedData((prev) => [...prev, likedCard]);
      setTeamMembers((prev) => [...prev, likedCard]); 
      setCurrentCardIndex((prev) => prev + 1);
    }
  };

  const handleDislike = () => {
    if (currentCardIndex < surveyData.length) {
      const updatedSurveyData = surveyData.filter((_, index) => index !== currentCardIndex);
      setSurveyData(updatedSurveyData);
      localStorage.setItem('surveyData', JSON.stringify(updatedSurveyData));
      setCurrentCardIndex((prev) => prev + 1);
    }
  };

  const toggleTeam = () => {
    setShowTeam(!showTeam);
  };

  const handleRemoveMember = (index) => {
    setTeamMembers((prev) => prev.filter((_, i) => i !== index));
  };

  const bind = useGesture({
    onDrag: ({ offset: [xOffset, yOffset], memo = [x.get(), y.get()] }) => {
      const [prevX, prevY] = memo;
      const rotation = (xOffset / 100) * 30; // Угол поворота (максимум 30 градусов)
      set({ x: prevX + xOffset, y: Math.min(prevY + yOffset, 100), rotate: rotation, opacity: 1 - Math.abs(xOffset) / 100 });
      return memo;
    },
    onDragEnd: ({ offset: [xOffset], velocity }) => {
      const threshold = 100; // Порог для свайпа
      if (xOffset > threshold) {
        handleLike();
        set({ x: 1000, y: 200, rotate: 30, opacity: 0 }); // Удаляем карточку с вращением
      } else if (xOffset < -threshold) {
        handleDislike();
        set({ x: -1000, y: 200, rotate: -30, opacity: 0 }); // Удаляем карточку с вращением
      } else {
        set({ x: 0, y: 0, rotate: 0, opacity: 1 }); // Возвращаем карточку на место
      }
    },
  });

  return (
    <div className="container">
      {currentCardIndex < surveyData.length ? (
        <animated.div
          {...bind()}
          style={{
            transform: x.to((x, y) => `translate(${x}px, ${y}px) rotate(${rotate.get()}deg)`),
            opacity,
            position: "absolute",
            width: "300px",
            height: "400px",
            background: "white",
            borderRadius: "10px",
            boxShadow: "0 2px 10px rgba(0,0,0,0.1)",
          }}
        >
          <div className="image">
            {surveyData[currentCardIndex].image && (
              <img
                src={surveyData[currentCardIndex].image}
                alt={surveyData[currentCardIndex].name}
                style={{ width: '300px', height: '400px', objectFit: 'cover' }}
              />
            )}
          </div>
          <div className="card-content">
            <h2>{surveyData[currentCardIndex].name}</h2>
            <p>Email: {surveyData[currentCardIndex].email}</p>
            <p>Возраст: {surveyData[currentCardIndex].age}</p>
            <p>Отзыв: {surveyData[currentCardIndex].feedback}</p>
          </div>
        </animated.div>
      ) : (
        <p>Нет больше карточек</p>
      )}

      <div className="buttons-card">
        <button className='dislike-button' onClick={handleDislike}>dislike</button>
        <button className='like-button' onClick={handleLike}>like</button>
      </div>

      <button className='show-team-button' onClick={toggleTeam}>
        {showTeam ? 'Скрыть команду' : 'Показать команду'}
      </button>

      {showTeam && (
        <div className="team-members">
          <h3>Члены команды:</h3>
          <table>
            <thead>
              <tr>
                <th>Имя</th>
                <th>Email</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              {teamMembers.map((member, index) => (
                <tr key={index}>
                  <td>{member.name}</td>
                  <td>{member.email}</td>
                  <td>
                    <button onClick={() => handleRemoveMember(index)}>Удалить</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}