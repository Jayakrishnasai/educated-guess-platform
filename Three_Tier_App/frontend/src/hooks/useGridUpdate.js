import { useState, useCallback } from 'react';

export const useGridUpdate = () => {
    const [activeCategory, setActiveCategory] = useState(null);

    const updateGrid = useCallback((category) => {
        setActiveCategory(category);
    }, []);

    return { activeCategory, updateGrid };
};
