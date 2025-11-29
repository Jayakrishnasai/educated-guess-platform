import React from 'react';
import { Outlet } from 'react-router-dom';
import NavigationStack from '../LeftNavigation/NavigationStack';
import './layout.css';

const SplitScreenLayout = () => {
    return (
        <div className="split-screen-layout">
            <div className="left-section">
                <NavigationStack />
            </div>
            <div className="right-section">
                <Outlet />
            </div>
        </div>
    );
};

export default SplitScreenLayout;
