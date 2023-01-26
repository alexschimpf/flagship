import * as React from 'react';
import {
    Button
} from '@mui/material';
import PeopleIcon from '@mui/icons-material/People';
import AppsIcon from '@mui/icons-material/Apps';
import PersonIcon from '@mui/icons-material/Person';
import { useNavigate } from 'react-router-dom';
import APIClient from '../../api';

function Sidebar(): React.ReactElement {
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
                flexDirection: 'column',
                borderRight: '1px solid black',
                paddingRight: '25px',
                height: '100%'
            }}
        >
            <Button 
                variant="outlined" 
                startIcon={<AppsIcon />}
                sx={{
                    textTransform: 'none',
                    color: 'black',
                    borderColor: 'black',
                    fontSize: '16px',
                    fontWeight: page === '' ? 600 : 400
                }}
                onClick={() => page !== '' && navigate('/')}
            >
                Projects
            </Button>
            <hr
                style={{
                    width: '100%'
                }}
            />
            <Button 
                variant="outlined" 
                startIcon={<PeopleIcon />}
                sx={{
                    textTransform: 'none',
                    color: 'black',
                    borderColor: 'black',
                    fontSize: '16px',
                    fontWeight: page === 'users' ? 600 : 400
                }}
                onClick={() => page !== 'users' && navigate('/users')}
            >
                Users
            </Button>
            <hr
                style={{
                    width: '100%'
                }}
            />
            <Button 
                variant="outlined" 
                startIcon={<PersonIcon />}
                sx={{
                    textTransform: 'none',
                    color: 'black',
                    borderColor: 'black',
                    fontSize: '16px',
                    fontWeight: page === 'profile' ? 600 : 400
                }}
                onClick={() => page !== 'profile' && navigate('/profile')}
            >
                Profile
            </Button>
        </div>
    );
}

export default Sidebar;
