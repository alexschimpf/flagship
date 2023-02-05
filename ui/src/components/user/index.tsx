import * as React from 'react';
import { TextField, Button, Typography, Select, MenuItem, Input, FormControl, InputLabel } from '@mui/material';
import { 
    useNavigate, useParams
} from 'react-router-dom';
import APIClient from '../../api';
import UserBreadcrumbs from '../userBreadcrumbs';

export const USER_STATUSES: any = {
    1: 'Invited',
    2: 'Activated'
}

export const USER_ROLES: any = {
    1: 'Read-only',
    2: 'Standard',
    3: 'Admin'
}

function User(): React.ReactElement {
    const navigate = useNavigate();
    const params = useParams();
    const userId = params.userId as string;
    
    const [email, setEmail]: [string, any] = React.useState('');
    const [name, setName]: [string, any] = React.useState('');
    const [role, setRole]: [number, any] = React.useState(-1);
    const [projects, setProjects]: [number[], any] = React.useState([]);

    React.useEffect(() => {
        APIClient.users.getUser(userId).then((resp) => {
            setEmail(resp.email);
            setName(resp.name);
            setRole(resp.role);
            setProjects(resp.projects);
        }).catch((e) => {
            // TODO
        });
    }, []);

    return (
        <div
            style={{
                display: 'flex',
                flexDirection: 'column'
            }}
        >
            <UserBreadcrumbs
                userId={userId}
                userEmail={email}
            />
            <hr style={{ width: '100%' }}/>
            <div style={{ width: '64ch' }}>
                <TextField
                    fullWidth
                    disabled
                    label='Email'
                    value={email}
                    sx={{display: 'block', margin: '30px 0'}}
                />
                <TextField
                    fullWidth
                    label='Name'
                    value={name}
                    sx={{display: 'block', margin: '30px 0'}}
                />
                { /* TODO: Allow admin to update his/her own role */ }
                <FormControl fullWidth>
                    <InputLabel htmlFor='role'>Role</InputLabel>
                    <Select
                        value={role}
                        input={<Input />}
                        inputProps={{name: 'role'}}
                    >
                    {Object.keys(USER_ROLES).map(roleId =>
                        <MenuItem key={roleId} value={roleId}>{USER_ROLES[roleId]}</MenuItem>
                    )}
                    </Select>
                </FormControl>
                <div style={{marginTop: '40px'}}>
                    <Typography>Projects</Typography>
                </div>
            <div style={{display: 'flex', flexDirection: 'row-reverse'}}>
                <Button 
                    variant='outlined'
                    sx={{
                        display: 'block',
                        textTransform: 'none',
                        color: 'black',
                        borderColor: 'black',
                        margin: '50px 0'
                    }}
                >
                    Save
                </Button>
            </div>
            </div>
        </div>
    );
}

export default User;
