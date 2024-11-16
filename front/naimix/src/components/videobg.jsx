import React from 'react'
import backgroundvideo from '../assets/videobg2.mp4'

export default function Videobg() {
    return(
        <div className="videobg">
            <video src={backgroundvideo} autoPlay loop muted />
        </div>
    )
}