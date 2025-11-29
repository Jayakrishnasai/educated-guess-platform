import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const JoinPage = () => {
    const navigate = useNavigate();
    const [isLogin, setIsLogin] = useState(true);
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        full_name: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            if (isLogin) {
                const response = await api.login({
                    email: formData.email,
                    password: formData.password
                });
                localStorage.setItem('accessToken', response.data.access_token);
                localStorage.setItem('user', JSON.stringify(response.data.user));
                navigate('/library');
            } else {
                await api.register({
                    email: formData.email,
                    password: formData.password,
                    full_name: formData.full_name
                });
                setIsLogin(true);
                setError('Registration successful! Please login.');
            }
        } catch (err) {
            setError(err.response?.data?.detail || 'An error occurred');
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    return (
        <div style={{
            minHeight: '100vh',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            padding: '40px'
        }}>
            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.4 }}
                style={{
                    background: '#ffffff',
                    borderRadius: '24px',
                    padding: '48px',
                    maxWidth: '480px',
                    width: '100%',
                    boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)'
                }}
            >
                <h1 style={{
                    fontFamily: 'Playfair Display, serif',
                    fontSize: '36px',
                    fontWeight: 900,
                    marginBottom: '12px',
                    textAlign: 'center',
                    color: '#1a1a1a'
                }}>
                    {isLogin ? 'Welcome Back' : 'Join Us'}
                </h1>
                <p style={{
                    fontFamily: 'Inter, sans-serif',
                    color: '#6b7280',
                    textAlign: 'center',
                    marginBottom: '32px'
                }}>
                    {isLogin ? 'Login to your account' : 'Create your account'}
                </p>

                <form onSubmit={handleSubmit}>
                    {!isLogin && (
                        <div style={{ marginBottom: '20px' }}>
                            <label style={{
                                fontFamily: 'Inter, sans-serif',
                                fontSize: '14px',
                                fontWeight: 600,
                                color: '#374151',
                                display: 'block',
                                marginBottom: '8px'
                            }}>
                                Full Name
                            </label>
                            <input
                                type="text"
                                name="full_name"
                                value={formData.full_name}
                                onChange={handleChange}
                                required={!isLogin}
                                style={{
                                    width: '100%',
                                    padding: '14px',
                                    border: '2px solid #e5e7eb',
                                    borderRadius: '12px',
                                    fontFamily: 'Inter, sans-serif',
                                    fontSize: '16px',
                                    outline: 'none',
                                    transition: 'border-color 0.3s ease'
                                }}
                            />
                        </div>
                    )}

                    <div style={{ marginBottom: '20px' }}>
                        <label style={{
                            fontFamily: 'Inter, sans-serif',
                            fontSize: '14px',
                            fontWeight: 600,
                            color: '#374151',
                            display: 'block',
                            marginBottom: '8px'
                        }}>
                            Email
                        </label>
                        <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            required
                            style={{
                                width: '100%',
                                padding: '14px',
                                border: '2px solid #e5e7eb',
                                borderRadius: '12px',
                                fontFamily: 'Inter, sans-serif',
                                fontSize: '16px',
                                outline: 'none'
                            }}
                        />
                    </div>

                    <div style={{ marginBottom: '24px' }}>
                        <label style={{
                            fontFamily: 'Inter, sans-serif',
                            fontSize: '14px',
                            fontWeight: 600,
                            color: '#374151',
                            display: 'block',
                            marginBottom: '8px'
                        }}>
                            Password
                        </label>
                        <input
                            type="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            required
                            minLength={8}
                            style={{
                                width: '100%',
                                padding: '14px',
                                border: '2px solid #e5e7eb',
                                borderRadius: '12px',
                                fontFamily: 'Inter, sans-serif',
                                fontSize: '16px',
                                outline: 'none'
                            }}
                        />
                    </div>

                    {error && (
                        <div style={{
                            padding: '12px',
                            background: '#fee2e2',
                            color: '#dc2626',
                            borderRadius: '8px',
                            marginBottom: '20px',
                            fontFamily: 'Inter, sans-serif',
                            fontSize: '14px'
                        }}>
                            {error}
                        </div>
                    )}

                    <button
                        type="submit"
                        disabled={loading}
                        style={{
                            width: '100%',
                            padding: '16px',
                            background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                            color: '#ffffff',
                            border: 'none',
                            borderRadius: '12px',
                            fontFamily: 'Inter, sans-serif',
                            fontSize: '16px',
                            fontWeight: 600,
                            cursor: loading ? 'not-allowed' : 'pointer',
                            transition: 'transform 0.2s ease',
                            opacity: loading ? 0.7 : 1
                        }}
                    >
                        {loading ? 'Processing...' : (isLogin ? 'Login' : 'Sign Up')}
                    </button>
                </form>

                <div style={{
                    marginTop: '24px',
                    textAlign: 'center',
                    fontFamily: 'Inter, sans-serif',
                    color: '#6b7280'
                }}>
                    {isLogin ? "Don't have an account? " : "Already have an account? "}
                    <button
                        onClick={() => {
                            setIsLogin(!isLogin);
                            setError('');
                        }}
                        style={{
                            background: 'none',
                            border: 'none',
                            color: '#6366f1',
                            fontWeight: 600,
                            cursor: 'pointer',
                            textDecoration: 'underline'
                        }}
                    >
                        {isLogin ? 'Sign Up' : 'Login'}
                    </button>
                </div>
            </motion.div>
        </div>
    );
};

export default JoinPage;
