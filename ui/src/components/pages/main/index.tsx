import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import APIClient from '../../../api';

function Main(): React.ReactElement {
    const navigate = useNavigate();

    React.useEffect(() => {
        APIClient.login.getLoginTest().catch(() => {
            navigate('/login', { replace: true });
        });
    }, []);

    return (
        <div>
            <p>main</p>
        </div>
    );
}

export default Main;
