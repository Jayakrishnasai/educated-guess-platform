import React from 'react';
import GridSection from '../components/ContentGrid/GridSection';
import SearchBar from '../components/Common/SearchBar';
import { useFetch } from '../hooks/useFetch';
import api from '../services/api';

const NetworkPage = () => {
    const { data: content, loading, error, refetch } = useFetch(
        () => api.getContent({ category: 'network' }),
        []
    );

    const handleSearch = (query) => {
        // Implement search functionality
        console.log('Searching for:', query);
    };

    return (
        <div>
            <SearchBar onSearch={handleSearch} />
            <GridSection
                title="Network"
                subtitle="Explore connections and networking insights"
                items={content}
                loading={loading}
                error={error}
            />
        </div>
    );
};

export default NetworkPage;
