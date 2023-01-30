import * as React from 'react';
import { 
    Table, TableBody, TableHead, TableCell, TableRow, TableContainer, Switch, IconButton, Paper
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import HistoryIcon from '@mui/icons-material/History';
import { 
    useNavigate, useParams
} from 'react-router-dom';
import APIClient from '../../api';
import { FeatureFlag } from '../../client';
import ProjectBreadcrumbs from '../projectBreadcrumbs';

function FeatureFlags(): React.ReactElement {
    const navigate = useNavigate();
    const params = useParams();
    const projectId = params.projectId as string;
    
    const [projectName, setProjectName]: [string | undefined, any] = React.useState();
    const [featureFlags, setFeatureFlags]: [FeatureFlag[], any] = React.useState([]);

    React.useEffect(() => {
        APIClient.projects.getProject(projectId).then((resp) => {
            setProjectName(resp.name);
        }).catch((e) => {
            // TODO
        });
        APIClient.featureFlags.getFeatureFlags(projectId).then((resp) => {
            setFeatureFlags(resp.items);
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
                                <TableCell sx={{color: 'white', backgroundColor: 'black'}}>Description</TableCell>
                                <TableCell sx={{color: 'white', backgroundColor: 'black'}}>Last Updated</TableCell>
                                <TableCell sx={{backgroundColor: 'black'}}></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                        {featureFlags.map((featureFlag, i) => (
                            <TableRow hover key={featureFlag.name} sx={{backgroundColor: i % 2 == 0 ? '#ffffff' : '#fafafa'}}>
                                <TableCell component="th" scope="row">
                                    {featureFlag.name}
                                </TableCell>
                                <TableCell>{featureFlag.description}</TableCell>
                                <TableCell>{new Date(featureFlag.updated_date).toLocaleString()}</TableCell>
                                <TableCell align='right'>
                                    <Switch checked={featureFlag.enabled} />
                                    <IconButton>
                                        <EditIcon onClick={() => navigate(`/project/${projectId}/feature-flag/${featureFlag._id}`)} />
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

export default FeatureFlags;
