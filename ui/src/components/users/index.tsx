import * as React from 'react';
import { 
    useNavigate
} from 'react-router-dom';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import { 
    Table, TableBody, TableHead, TableCell, TableRow, TableContainer, IconButton, Paper
} from '@mui/material';
import { User } from '../../client';
import APIClient from '../../api';
import UserBreadcrumbs from '../userBreadcrumbs';
import { USER_STATUSES, USER_ROLES } from '../user';

function Users(): React.ReactElement {
    const navigate = useNavigate();

    const [users, setUsers]: [User[], any] = React.useState([]);

    React.useEffect(() => {
        APIClient.users.getUsers().then((resp) => {
            setUsers(resp.items);
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
            <UserBreadcrumbs />
            <hr style={{ width: '100%' }}/>
            <Paper sx={{ width: '100%', overflow: 'hidden' }}>
                <TableContainer sx={{maxHeight: '80vh'}}>
                    <Table stickyHeader>
                        <TableHead>
                            <TableRow>
                                <TableCell sx={{color: 'white', backgroundColor: 'black'}}>Email</TableCell>
                                <TableCell sx={{color: 'white', backgroundColor: 'black'}}>Name</TableCell>
                                <TableCell sx={{color: 'white', backgroundColor: 'black'}}>Role</TableCell>
                                <TableCell sx={{color: 'white', backgroundColor: 'black'}}>Status</TableCell>
                                <TableCell sx={{backgroundColor: 'black'}}></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                        {users.map((user, i) => (
                            <TableRow hover key={user.email} sx={{backgroundColor: i % 2 == 0 ? '#ffffff' : '#fafafa'}}>
                                <TableCell component="th" scope="row">
                                    {user.email}
                                </TableCell>
                                <TableCell>{user.name}</TableCell>
                                <TableCell>{USER_ROLES[user.role]}</TableCell>
                                <TableCell>{USER_STATUSES[user.status]}</TableCell>
                                <TableCell align='right'>
                                    <IconButton>
                                        <EditIcon onClick={() => navigate(`/user/${user._id}`)} />
                                    </IconButton>
                                    <IconButton>
                                        <DeleteIcon />
                                    </IconButton>
                                </TableCell>
                            </TableRow>
                        ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </Paper>
        </div>
    );
}

export default Users;
