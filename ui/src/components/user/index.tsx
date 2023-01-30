import * as React from 'react';
import { 
    useNavigate, useParams
} from 'react-router-dom';
import APIClient from '../../api';

function User(): React.ReactElement {
    const navigate = useNavigate();
    const params = useParams();

    return (
        <div>
            user {params.userId}     
        </div>
    );
}

export default User;
