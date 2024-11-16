import React from 'react'
import './JobTable.css'
import { useNavigate } from 'react-router-dom';

export default function JobTable({ name, description }) {

    const navigate = useNavigate(); // Получаем функцию навигации

    const handleClick = () => {
    navigate('/surveyform');
    }

    return(
      <>
        <div className="table-wrapper">
          <div className='include-table'>
            <div>
              <h2 className='table-name'>{name}</h2>
              <p className='description'>{description}</p>
            </div>
            
          </div>

        </div>
      </>
      
    )
  
  }