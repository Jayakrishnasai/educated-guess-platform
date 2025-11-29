import React from 'react';
import { motion } from 'framer-motion';
import './grid.css';

const GridItem = ({ item }) => {
    return (
        <motion.div
            className="grid-item"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.4 }}
            whileHover={{ scale: 1.03 }}
        >
            {item.image_url && (
                <img
                    src={item.image_url}
                    alt={item.title}
                    className="grid-item-image"
                    onError={(e) => {
                        e.target.style.display = 'none';
                    }}
                />
            )}
            <div className="grid-item-content">
                <h3 className="grid-item-title">{item.title}</h3>
                <p className="grid-item-description">{item.description}</p>
                {item.tags && item.tags.length > 0 && (
                    <div className="grid-item-tags">
                        {item.tags.map((tag, index) => (
                            <span key={index} className="grid-item-tag">{tag}</span>
                        ))}
                    </div>
                )}
            </div>
        </motion.div>
    );
};

export default GridItem;
