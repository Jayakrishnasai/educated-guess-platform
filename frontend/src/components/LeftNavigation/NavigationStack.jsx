import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import NavItem from './NavItem';
import './leftNavigation.css';

const NavigationStack = () => {
    const navigate = useNavigate();
    const location = useLocation();

    const navItems = [
        { title: 'Network', path: '/network' },
        { title: 'Library', path: '/library' },
        { title: 'About', path: '/about' },
        { title: 'Join', path: '/join' }
    ];

    const handleNavClick = (path) => {
        navigate(path);
    };

    return (
        <div className="nav-container">
            <div className="nav-header">
                <div className="nav-logo">EducatedGuess</div>
            </div>
            <div className="navigation-stack">
                {navItems.map((item, index) => (
                    <NavItem
                        key={index}
                        title={item.title}
                        isActive={location.pathname === item.path || (location.pathname === '/' && item.path === '/network')}
                        onClick={() => handleNavClick(item.path)}
                    />
                ))}
            </div>
        </div>
    );
};

export default NavigationStack;
