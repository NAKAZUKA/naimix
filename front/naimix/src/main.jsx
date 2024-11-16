import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import Videobg from './components/videobg.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
    <Videobg />
  </StrictMode>,
)
