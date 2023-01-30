import * as React from 'react';
import { Link, List, ListItem } from '@mui/material';
import { 
    useNavigate, useParams
} from 'react-router-dom';
import APIClient from '../../api';
import ProjectBreadcrumbs from '../projectBreadcrumbs';

function Project(): React.ReactElement {
    const navigate = useNavigate();
    const params = useParams();
    const projectId = params.projectId as string;
    
    const [name, setName]: [string | undefined, any] = React.useState();

    React.useEffect(() => {
        APIClient.projects.getProject(projectId).then((resp) => {
            setName(resp.name);
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
                projectName={name}
            />
            <hr style={{ width: '100%' }}/>
            <div>
                <List style={{ width: '100%' }}>
                    <ListItem
                        sx={{ paddingLeft: 0, paddingTop: 0 }}
                    >
                        <Link href={`/project/${projectId}/feature-flags`}>Manage feature flags</Link>
                    </ListItem>
                    <ListItem
                        sx={{ paddingLeft: 0, paddingTop: 0 }}
                    >
                        <Link href={`/project/${projectId}/context-fields`}>Manage context fields</Link>
                    </ListItem>
                    <ListItem
                        sx={{ paddingLeft: 0, paddingTop: 0 }}
                    >
                        <Link href={`/project/${projectId}/`}>Rename project</Link>
                    </ListItem>
                    <ListItem
                        sx={{ paddingLeft: 0, paddingTop: 0 }}
                    >
                        <Link href={`/project/${projectId}`}>Delete project</Link>
                    </ListItem>
                </List>
            </div>
        </div>
    );
}

export default Project;
