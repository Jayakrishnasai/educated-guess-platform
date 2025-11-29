import React from 'react';
import { motion } from 'framer-motion';

const AboutPage = () => {
    return (
        <div style={{ padding: '60px 80px', maxWidth: '900px', margin: '0 auto' }}>
            <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
            >
                <h1 style={{
                    fontFamily: 'Playfair Display, serif',
                    fontSize: '52px',
                    fontWeight: 900,
                    marginBottom: '32px',
                    background: 'linear-gradient(135deg, #1a1a1a 0%, #6366f1 100%)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    backgroundClip: 'text'
                }}>
                    About EducatedGuess
                </h1>

                <div style={{ fontFamily: 'Inter, sans-serif', lineHeight: 1.8, color: '#4b5563' }}>
                    <p style={{ fontSize: '20px', marginBottom: '24px' }}>
                        EducatedGuess is a modern media platform dedicated to thoughtful exploration
                        of ideas, design, culture, and philosophy.
                    </p>

                    <h2 style={{
                        fontFamily: 'Playfair Display, serif',
                        fontSize: '32px',
                        fontWeight: 700,
                        margin: '48px 0 24px 0',
                        color: '#1a1a1a'
                    }}>
                        Our Mission
                    </h2>
                    <p style={{ marginBottom: '20px' }}>
                        We believe in creating space for nuanced conversations and deep thinking.
                        Our platform brings together writers, thinkers, and creators who challenge
                        conventional wisdom and explore new perspectives.
                    </p>

                    <h2 style={{
                        fontFamily: 'Playfair Display, serif',
                        fontSize: '32px',
                        fontWeight: 700,
                        margin: '48px 0 24px 0',
                        color: '#1a1a1a'
                    }}>
                        What We Offer
                    </h2>
                    <ul style={{ marginBottom: '20px', paddingLeft: '24px' }}>
                        <li style={{ marginBottom: '12px' }}>Curated content across philosophy, design, and culture</li>
                        <li style={{ marginBottom: '12px' }}>Thought-provoking essays and articles</li>
                        <li style={{ marginBottom: '12px' }}>A community of curious minds</li>
                        <li style={{ marginBottom: '12px' }}>Beautiful, distraction-free reading experience</li>
                    </ul>

                    <h2 style={{
                        fontFamily: 'Playfair Display, serif',
                        fontSize: '32px',
                        fontWeight: 700,
                        margin: '48px 0 24px 0',
                        color: '#1a1a1a'
                    }}>
                        Technology
                    </h2>
                    <p>
                        Built with modern web technologies including React, FastAPI, and MongoDB,
                        deployed on Azure Kubernetes Service for scalability and reliability.
                    </p>
                </div>
            </motion.div>
        </div>
    );
};

export default AboutPage;
