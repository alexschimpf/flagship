import * as React from 'react';
import {
    Link, List, ListItem, Breadcrumbs
} from '@mui/material';
import APIClient from '../../api';
import { Project } from '../../client/models/Project'
import ProjectBreadcrumbs from '../projectBreadcrumbs';

function Projects(): React.ReactElement {
    const [projects, setProjects]: [Project[], any] = React.useState([]);

    React.useEffect(() => {
        APIClient.projects.getProjects().then((resp) => {
            setProjects(resp.items.sort((a, b) => (
                a.name.toLowerCase().localeCompare(b.name.toLowerCase())
            )))
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
            <ProjectBreadcrumbs />
            <hr style={{ width: '100%' }}/>
            <List>
                {
                    projects.map((project) => (
                        <ListItem
                            key={project._id}
                            sx={{ paddingLeft: 0, paddingTop: 0 }}
                        >
                            <Link href={`/project/${project._id}`}>{project.name}</Link>
                        </ListItem>
                    ))
                }
            </List>
        </div>
    );
}

export default Projects;
