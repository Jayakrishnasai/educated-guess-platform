import React, { useState } from 'react';
import GridSection from '../components/ContentGrid/GridSection';
import SearchBar from '../components/Common/SearchBar';
import { useFetch } from '../hooks/useFetch';
import api from '../services/api';

const LibraryPage = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const { data: content, loading, error } = useFetch(
        () => api.getContent({ search: searchQuery }),
        [searchQuery]
    );

    const handleSearch = (query) => {
        setSearchQuery(query);
    };

    return (
        <div>
            <SearchBar onSearch={handleSearch} />
            <GridSection
                title="Library"
                subtitle="Discover curated content across all categories"
                items={content}
                loading={loading}
                error={error}
            />
        </div>
    );
};

export default LibraryPage;
