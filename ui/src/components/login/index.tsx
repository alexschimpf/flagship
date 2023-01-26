import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Button, TextField, Typography, Link
} from '@mui/material';
import './index.css';
import APIClient from '../../api';

function Login(): React.ReactElement {
    const navigate = useNavigate();

    const [error, setError] = React.useState('');

    React.useEffect(() => {
        APIClient.login.getLoginTest().then(() => {
            navigate('/', { replace: true });
        });

        const queryParams = window.location.search.substring(1).split('&');
        for (const param of queryParams) {
            const [key, value] = param.split('=');
            if (key === 'error') {
                setError(decodeURIComponent(value));
            }
        }
    }, []);

    return (
        // TODO: Add API base URL to config
        <form className='login' action='http://localhost:8000/login' method='post'>
            <div className='login--form'>
                <Typography
                    sx={{
                        fontSize: '24px',
                        marginBottom: '20px'
                    }}
                >
                    Login
                </Typography>
                <TextField
                    autoFocus
                    type='email'
                    label='Email'
                    name='email'
                    sx={{
                        border: '1px solid #5d5d5d 5px',
                        marginBottom: '10px',
                        color: '#5d5d5d',
                        '& label.Mui-focused': {
                            color: 'black'
                        },
                        '& .MuiOutlinedInput-root': {
                            '&.Mui-focused fieldset': {
                                borderColor: 'black',
                                borderWidth: '1px'
                            }
                        }
                    }}
                />
                <TextField
                    type='password'
                    label='Password'
                    name='password'
                    sx={{
                        border: '1px solid #5d5d5d 5px',
                        marginBottom: '20px',
                        color: '#5d5d5d',
                        '& label.Mui-focused': {
                            color: 'black'
                        },
                        '& .MuiOutlinedInput-root': {
                            '&.Mui-focused fieldset': {
                                borderColor: 'black',
                                borderWidth: '1px'
                            }
                        }
                    }}
                />
                {error ?
                    <div>
                        <Typography
                            sx={{
                                color: 'red',
                                marginBottom: '20px'
                            }}
                        >
                            {error}
                        </Typography>
                    </div>
                    : null
                }
                <div style={{ textAlign: 'right' }}>
                    <Link
                        href='/forgot-password'
                    >
                        Forgot password?
                    </Link>
                    <br />
                    <Button
                        type='submit'
                        sx={{
                            marginTop: '20px',
                            border: '1px solid #5d5d5d',
                            textTransform: 'none',
                            color: 'black',
                            '&:hover': {
                                backgroundColor: '#f5f5f5'
                            }
                        }}
                    >
                        Log in
                    </Button>
                </div>
            </div>
        </form>
    );
}

export default Login;
