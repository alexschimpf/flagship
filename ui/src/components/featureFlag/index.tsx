import * as React from 'react';
import { TextField, FormControlLabel, Checkbox, Button, Typography } from '@mui/material';
import { 
    useNavigate, useParams
} from 'react-router-dom';
import APIClient from '../../api';
import { FeatureFlagCondition } from '../../client';
import ProjectBreadcrumbs from '../projectBreadcrumbs';
import FeatureFlagConditions from '../featureFlagConditions';

function FeatureFlag(): React.ReactElement {
    const navigate = useNavigate();
    const params = useParams();
    const projectId = params.projectId as string;
    const featureFlagId = params.featureFlagId as string;
    
    const [projectName, setProjectName]: [string | undefined, any] = React.useState();
    const [name, setName]: [string, any] = React.useState('');
    const [description, setDescription]: [string, any] = React.useState('');
    const [conditions, setConditions]: [FeatureFlagCondition[], any] = React.useState([]);
    const [enabled, setEnabled]: [boolean, any] = React.useState(false);

    React.useEffect(() => {
        APIClient.projects.getProject(projectId).then((resp) => {
            setProjectName(resp.name);
        }).catch((e) => {
            // TODO
        });
        APIClient.featureFlags.getFeatureFlag(featureFlagId, projectId).then((resp) => {
            setName(resp.name);
            setDescription(resp.description);
            setConditions(resp.conditions);
            setEnabled(resp.enabled);
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
                featureFlagId={featureFlagId}
                featureFlagName={name}
            />
            <hr style={{ width: '100%' }}/>
            <div style={{ width: '64ch' }}>
                <TextField
                    autoFocus
                    fullWidth
                    label='Name'
                    value={name}
                    sx={{display: 'block', margin: '30px 0'}}
                />
                <TextField
                    fullWidth
                    label='Description'
                    value={description}
                    sx={{display: 'block', margin: '30px 0'}}
                />
                <Typography>Conditions</Typography>
                <FeatureFlagConditions />
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
                <FormControlLabel 
                    control={<Checkbox checked={enabled} sx={{display: 'block', margin: '0'}} />} 
                    label='Enabled'
                    labelPlacement='start'
                    sx={{margin: '0 20px'}}
                />
            </div>
            </div>
        </div>
    );
}

export default FeatureFlag;
