import * as React from 'react';
import { TextField, FormControlLabel, Checkbox, Button, Typography } from '@mui/material';
import { 
    useNavigate, useParams
} from 'react-router-dom';
import APIClient from '../../api';
import { FeatureFlagCondition } from '../../client';
import ProjectBreadcrumbs from '../projectBreadcrumbs';
import FeatureFlagConditions from '../featureFlagConditions';

export const CONTEXT_VALUE_TYPES: any = {
    1: 'String',
    2: 'Number',
    3: 'Integer',
    4: 'Boolean',
    5: 'Enum',
    6: 'Version',
    7: 'String List',
    8: 'Integer List',
    9: 'Enum List'
}

function ContextField(): React.ReactElement {
    const navigate = useNavigate();
    const params = useParams();
    const projectId = params.projectId as string;
    const contextFieldId = params.contextFieldId as string;
    
    const [projectName, setProjectName]: [string | undefined, any] = React.useState();
    const [name, setName]: [string, any] = React.useState('');
    const [key, setKey]: [string, any] = React.useState('');
    const [valueType, setValueType]: [string, any] = React.useState('');
    const [description, setDescription]: [string, any] = React.useState('');
    const [enumDef, setEnumDef]: [string, any] = React.useState('');

    React.useEffect(() => {
        APIClient.projects.getProject(projectId).then((resp) => {
            setProjectName(resp.name);
        }).catch((e) => {
            // TODO
        });
        APIClient.contextFields.getContextField(contextFieldId, projectId).then((resp) => {
            setName(resp.name);
            setKey(resp.key);
            setDescription(resp.description);
            setValueType(resp.value_type);
            setEnumDef(resp.enum_def);
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
                contextFieldId={contextFieldId}
                contextFieldName={name}
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
                    disabled
                    fullWidth
                    label='Key'
                    value={key}
                    sx={{display: 'block', margin: '30px 0'}}
                />
                <TextField
                    disabled
                    fullWidth
                    label='Type'
                    value={CONTEXT_VALUE_TYPES[valueType] || ''}
                    sx={{display: 'block', margin: '30px 0'}}
                />
                <TextField
                    fullWidth
                    label='Description'
                    value={description}
                    sx={{display: 'block', margin: '30px 0'}}
                />
                {enumDef &&
                    <TextField
                        fullWidth
                        label='Enum Definition'
                        value={enumDef}
                        sx={{display: 'block', margin: '30px 0'}}
                    />
                }
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

export default ContextField;
