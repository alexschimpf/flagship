import * as React from 'react';
import { Breadcrumbs, Link } from '@mui/material';

interface Props {
    projectId?: string;
    projectName?: string;
    featureFlagId?: string;
    featureFlagName?: string;
    contextFieldId?: string;
    contextFieldName?: string;

}

function ProjectBreadcrumbs(props: Props): React.ReactElement {
    const { 
        projectId,
        projectName,
        featureFlagId,
        featureFlagName,
        contextFieldId,
        contextFieldName
    } = props;

    const page = window.location.pathname.substring(1);

    return (
        <Breadcrumbs>
            <Link 
                sx={{
                    fontSize: '16px',
                    fontWeight: 600
                }}
                href='/'
            >
                Projects
            </Link>
            {projectId &&
                <Link 
                    sx={{
                        fontSize: '16px',
                        fontWeight: 600
                    }}
                    href={`/project/${projectId}`}
                >
                    {projectName || 'Loading...'}
                </Link>
            }
            {projectId && page.includes('feature-flag') &&
                <Link 
                    sx={{
                        fontSize: '16px',
                        fontWeight: 600
                    }}
                    href={`/project/${projectId}/feature-flags`}
                >
                    Feature Flags
                </Link>
            }
            {projectId && featureFlagId &&
                <Link 
                    sx={{
                        fontSize: '16px',
                        fontWeight: 600
                    }}
                    href={`/project/${projectId}/feature-flag/${featureFlagId}`}
                >
                    {featureFlagName || 'Loading...'}
                </Link>
            }
            {projectId && page.includes('context-field') &&
                <Link 
                    sx={{
                        fontSize: '16px',
                        fontWeight: 600
                    }}
                    href={`/project/${projectId}/context-fields`}
                >
                    Context Fields
                </Link>
            }
            {projectId && contextFieldId &&
                <Link 
                    sx={{
                        fontSize: '16px',
                        fontWeight: 600
                    }}
                    href={`/project/${projectId}/context-field/${contextFieldId}`}
                >
                    {contextFieldName || 'Loading...'}
                </Link>
            }
        </Breadcrumbs>
    );
}

export default ProjectBreadcrumbs;
