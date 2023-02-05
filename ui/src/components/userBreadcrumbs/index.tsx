import * as React from 'react';
import { Breadcrumbs, Link } from '@mui/material';

interface Props {
    userId?: string;
    userEmail?: string;
}

function UserBreadcrumbs(props: Props): React.ReactElement {
    const { 
        userId,
        userEmail
    } = props;

    return (
        <Breadcrumbs>
            <Link 
                sx={{
                    fontSize: '16px',
                    fontWeight: 600
                }}
                href='/users'
            >
                Users
            </Link>
            {userId &&
                <Link 
                    sx={{
                        fontSize: '16px',
                        fontWeight: 600
                    }}
                    href={`/user/${userId}`}
                >
                    {userEmail || 'Loading...'}
                </Link>
            }
        </Breadcrumbs>
    );
}

export default UserBreadcrumbs;
