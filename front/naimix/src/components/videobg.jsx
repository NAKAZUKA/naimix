import React from 'react'
import backgroundimage from '../assets/image.png'

export default function Videobg() {
    return(
        <div className="videobg">
            <img src={backgroundimage} autoPlay loop muted />
        </div>
    )
}