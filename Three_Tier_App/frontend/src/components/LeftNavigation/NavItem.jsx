import React from 'react';
import { motion } from 'framer-motion';
import './leftNavigation.css';

const NavItem = ({ title, isActive, onClick }) => {
    return (
        <motion.div
            className={`nav-item ${isActive ? 'active' : ''}`}
            onClick={onClick}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3 }}
        >
            {title}
        </motion.div>
    );
};

export default NavItem;
