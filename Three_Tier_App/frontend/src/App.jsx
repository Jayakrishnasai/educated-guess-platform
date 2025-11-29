import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import SplitScreenLayout from './components/Layout/SplitScreenLayout';
import Home from './pages/Home';
import NetworkPage from './pages/NetworkPage';
import LibraryPage from './pages/LibraryPage';
import AboutPage from './pages/AboutPage';
import JoinPage from './pages/JoinPage';
import './App.css';

function App() {
    return (
        <BrowserRouter>
            <Routes>
                {/* Layout with split screen */}
                <Route path="/" element={<SplitScreenLayout />}>
                    <Route index element={<Navigate to="/network" replace />} />
                    <Route path="network" element={<NetworkPage />} />
                    <Route path="library" element={<LibraryPage />} />
                    <Route path="about" element={<AboutPage />} />
                </Route>

                {/* Full screen routes */}
                <Route path="/join" element={<JoinPage />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
