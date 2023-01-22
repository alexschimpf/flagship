import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import APIClient from '../../../api';

function Login(): React.ReactElement {
    const navigate = useNavigate();

    React.useEffect(() => {
        const testLogin = async () => {
            await APIClient.login.getLoginTest();
        };
        testLogin().then(() => {
            navigate('/', { replace: true });
        });
    }, []);

    return (
        <div>
            <p>login</p>
        </div>
    );
}

export default Login;
