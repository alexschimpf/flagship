import * as React from 'react';
import { 
    Table, TableBody, TableHead, TableCell, TableRow, TableContainer, IconButton, Paper
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import HistoryIcon from '@mui/icons-material/History';
import { 
    useNavigate, useParams
} from 'react-router-dom';
import APIClient from '../../api';
import { ContextField } from '../../client';
import { CONTEXT_VALUE_TYPES } from '../contextField';
import ProjectBreadcrumbs from '../projectBreadcrumbs';

function ContextFields(): React.ReactElement {
    const navigate = useNavigate();
    const params = useParams();
    const projectId = params.projectId as string;
    
    const [projectName, setProjectName]: [string | undefined, any] = React.useState();
    const [contextFields, setContextFields]: [ContextField[], any] = React.useState([]);

    React.useEffect(() => {
        APIClient.projects.getProject(projectId).then((resp) => {
            setProjectName(resp.name);
        }).catch((e) => {
            // TODO
        });
        APIClient.contextFields.getContextFields(projectId).then((resp) => {
            setContextFields(resp.items);
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
            <ProjectBreadcrumbs
                projectId={projectId}
                projectName={projectName}
            />
            <hr style={{ width: '100%' }}/>
            <Paper sx={{ width: '100%', overflow: 'hidden' }}>
                <TableContainer sx={{maxHeight: '80vh'}}>
                    <Table stickyHeader>
                        <TableHead>
                            <TableRow>
                                <TableCell sx={{color: 'white', backgroundColor: 'black'}}>Name</TableCell>
                                <TableCell sx={{color: 'white', backgroundColor: 'black'}}>Type</TableCell>
                                <TableCell sx={{color: 'white', backgroundColor: 'black'}}>Description</TableCell>
                                <TableCell sx={{color: 'white', backgroundColor: 'black'}}>Last Updated</TableCell>
                                <TableCell sx={{backgroundColor: 'black'}}></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                        {contextFields.map((contextField, i) => (
                            <TableRow hover key={contextField.name} sx={{backgroundColor: i % 2 == 0 ? '#ffffff' : '#fafafa'}}>
                                <TableCell component="th" scope="row">
                                    {contextField.name}
                                </TableCell>
                                <TableCell>{CONTEXT_VALUE_TYPES[contextField.value_type.valueOf()]}</TableCell>
                                <TableCell>{contextField.description}</TableCell>
                                <TableCell>{new Date(contextField.updated_date).toLocaleString()}</TableCell>
                                <TableCell align='right'>
                                    <IconButton>
                                        <EditIcon onClick={() => navigate(`/project/${projectId}/context-field/${contextField._id}`)} />
                                    </IconButton>
                                    <IconButton>
                                        <DeleteIcon />
                                    </IconButton>
                                    <IconButton>
                                        <HistoryIcon/>
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

export default ContextFields;
