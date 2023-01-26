import * as React from 'react';
import { Link } from '@mui/material';

function Header(): React.ReactElement {
    return (
        <div>
            <Link
                href='/'
                sx={{
                    fontSize: '28px',
                    fontWeight: 700,
                    textDecoration: 'none',
                    color: 'black',
                    cursor: 'pointer'
                }}
            >
                Flagship
            </Link>
            <hr />
        </div>
    );
}

export default Header;
