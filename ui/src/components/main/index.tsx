import * as React from 'react';
import { 
    useNavigate, BrowserRouter, Routes, Route
} from 'react-router-dom';
import APIClient from '../../api';
import Sidebar from '../sidebar';
import Projects from '../projects';
import Users from '../users';

function Main(): React.ReactElement {
    const navigate = useNavigate();

    const page = window.location.pathname.substring(1);

    React.useEffect(() => {
        APIClient.login.getLoginTest().catch(() => {
            navigate('/login', { replace: true });
        });
    }, []);

    return (
        <div
            style={{
                display: 'flex',
                height: '100%'
            }}
        >
            <div
                style={{
                    marginRight: '20px',
                    width: '200px',
                }}
            >
                <Sidebar />
            </div>
            <div>
                {
                    page === '' ? <Projects /> : <Users />
                }
            </div>
        </div>
    );
}

export default Main;
