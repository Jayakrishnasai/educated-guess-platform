import React from 'react';
import GridItem from './GridItem';
import './grid.css';

const GridSection = ({ title, subtitle, items, loading, error }) => {
    if (loading) {
        return <div className="grid-loading">Loading content...</div>;
    }

    if (error) {
        return <div className="grid-error">Error: {error}</div>;
    }

    if (!items || items.length === 0) {
        return <div className="grid-empty">No content available</div>;
    }

    return (
        <div>
            {title && (
                <div className="grid-section-header">
                    <h1 className="grid-section-title">{title}</h1>
                    {subtitle && <p className="grid-section-subtitle">{subtitle}</p>}
                </div>
            )}
            <div className="content-grid">
                {items.map((item) => (
                    <GridItem key={item._id || item.id} item={item} />
                ))}
            </div>
        </div>
    );
};

export default GridSection;
