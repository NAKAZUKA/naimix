import React, { createContext, useState, useEffect} from 'react';

export const SurveyContext = createContext();

export const SurveyProvider = ({ children }) => {
    const [surveyData, setSurveyData] = useState([]);

    useEffect(() => {
        const storedData = localStorage.getItem('surveyData');
        if (storedData) {
            setSurveyData(JSON.parse(storedData));
        }
    }, []);

    return (
        <SurveyContext.Provider value={{ surveyData, setSurveyData }}>
            {children}
        </SurveyContext.Provider>
    )
}
