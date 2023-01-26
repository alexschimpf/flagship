import * as React from 'react';
import { 
    useNavigate, BrowserRouter, Routes, Route
} from 'react-router-dom';
import APIClient from '../../api';

function Users(): React.ReactElement {
    const navigate = useNavigate();

    return (
        <div>
            users            
        </div>
    );
}

export default Users;
