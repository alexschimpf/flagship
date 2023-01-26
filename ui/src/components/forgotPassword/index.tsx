import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Button, TextField, Typography, Link
} from '@mui/material';
import './index.css';
import APIClient from '../../api';

function ForgotPassword(): React.ReactElement {
    const navigate = useNavigate();

    const [email, setEmail] = React.useState('');
    const [error, setError] = React.useState('');
    const [info, setInfo] = React.useState('');

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

    const onForgotPasswordBtnClick = async () => {
        try {
            await APIClient.users.resetPassword({ email });
            setError('');
            setInfo(
                'An email was sent to the provided address, assuming the ' +
                'address is actually associated to an existing account.'
            );
        } catch (e) {
            setInfo('');
            setError(e.body.errors[0].message);
        }
    };

    return (
        <div className='forgot-password'>
            <div className='forgot-password--form'>
                <Typography
                    sx={{
                        fontSize: '24px',
                        marginBottom: '20px'
                    }}
                >
                    Reset Password
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
                    onChange={(e) => setEmail(e.target.value)}
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
                {info ?
                    <div>
                        <Typography
                            sx={{
                                color: 'green',
                                marginBottom: '20px'
                            }}
                        >
                            {info}
                        </Typography>
                    </div>
                    : null
                }
                <div style={{ textAlign: 'right' }}>
                    <Link
                        href='/login'
                    >
                        Back to login?
                    </Link>
                    <br />
                    <Button
                        type='button'
                        sx={{
                            marginTop: '20px',
                            border: '1px solid #5d5d5d',
                            textTransform: 'none',
                            color: 'black',
                            '&:hover': {
                                backgroundColor: '#f5f5f5'
                            }
                        }}
                        onClick={onForgotPasswordBtnClick}
                    >
                        Send email
                    </Button>
                </div>
            </div>
        </div>
    );
}

export default ForgotPassword;
