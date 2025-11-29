import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import './hero.css';

const Hero = () => {
    const navigate = useNavigate();

    return (
        <div className="hero-section">
            <motion.div
                className="hero-content"
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8 }}
            >
                <h1 className="hero-title">EducatedGuess</h1>
                <p className="hero-subtitle">
                    A modern platform for thoughtful exploration of ideas, design, and culture
                </p>
                <div className="hero-cta">
                    <button
                        className="hero-button hero-button-primary"
                        onClick={() => navigate('/library')}
                    >
                        Explore Content
                    </button>
                    <button
                        className="hero-button hero-button-secondary"
                        onClick={() => navigate('/about')}
                    >
                        Learn More
                    </button>
                </div>
            </motion.div>
            <div className="hero-scroll-indicator">
                <span>Scroll to discover</span>
                <span>↓</span>
            </div>
        </div>
    );
};

export default Hero;
