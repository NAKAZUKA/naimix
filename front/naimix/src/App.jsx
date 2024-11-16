import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/Home/Home.jsx'; // Импортируйте компонент Home
import SurveyForm from './components/SurveyForm/SurveyForm.jsx'; // Импортируйте компонент SurveyForm
import TinderSwiper from './components/Tinder/TinderSwiper.jsx'; // Импортируйте компонент TinderSwiper
import Login from './components/Auth/Login.jsx'; // Импортируйте компонент Login
import Register from './components/Auth/Register.jsx'; // Импортируйте компонент Register
import AuthPage from './components/Auth/AuthPage.jsx'; // Импортируйте компонент AuthPage
import { SurveyProvider } from './components/SurveyForm/SurveyContext.jsx';
import CheckSession from './components/Auth/ChechSession.jsx';

function App() {
  return (
    <SurveyProvider>
      <Router>
        <Routes>
          <Route path="/" element={<AuthPage />} /> {/* Главная страница для входа/регистрации */}
          <Route path="/home" element={<Home />} /> {/* Страница для кандидатов */}
          <Route path="/surveyform" element={<SurveyForm />} />
          <Route path="/swiper" element={<TinderSwiper />} />
          <Route path="/login" element={<Login />} /> {/* Страница входа */}
          <Route path="/register" element={<Register />} /> {/* Страница регистрации */}
        </Routes>
      </Router>
    </SurveyProvider>
    
  );
}

export default App;