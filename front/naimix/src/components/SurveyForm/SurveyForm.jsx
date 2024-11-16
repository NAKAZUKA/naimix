import React, { useContext, useState } from 'react';
import { SurveyContext } from './SurveyContext';
import { useLocation, useNavigate } from 'react-router-dom';
import './SurveyForm.css';

export default function SurveyForm() {
  const { surveyData, setSurveyData } = useContext(SurveyContext);
  const location = useLocation();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    age: '',
    feedback: '',
    image: null,
    specialty: location.state?.specialty || '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setFormData({
          ...formData,
          image: reader.result,
        });
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const updatedSurveyData = [...surveyData, formData];
    setSurveyData(updatedSurveyData);
    localStorage.setItem('surveyData', JSON.stringify(updatedSurveyData));


    setFormData({
      name: '',
      email: '',
      age: '',
      feedback: '',
      image: null,
      specialty: '',
    });
  };

  return (
    <div className="form-container">
      <h1 className='survey'>Анкета</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Имя:</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="age">Возраст:</label>
          <input
            type="number"
            id="age"
            name="age"
            value={formData.age}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="feedback">Стек знаний:</label>
          <textarea
            id="feedback"
            name="feedback"
            value={formData.feedback}
            onChange={handleChange}
            required
          ></textarea>
        </div>
        {/* Поле для загрузки изображения */}
        <div className="form-group">
          <label htmlFor="image">Загрузить фотографию:</label>
          <input
            type="file"
            id="image"
            name="image"
            accept="image/*"
            onChange={handleImageChange} // Обработчик изменения для загрузки изображения
          />
        </div>
        {formData.image && <img src={formData.image} alt="Preview" style={{ width: '100px', height: '100px', objectFit: 'cover' }} />} {/* Предварительный просмотр загруженного изображения */}
        <button className='formButton' type="submit">Отправить</button>
      </form>
    </div>
  );
}