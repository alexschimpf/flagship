import * as React from 'react';
import { 
    useNavigate, BrowserRouter, Routes, Route
} from 'react-router-dom';
import APIClient from '../../api';

function Projects(): React.ReactElement {
    const navigate = useNavigate();

    return (
        <div>
            projects            
        </div>
    );
}

export default Projects;
