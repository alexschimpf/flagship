import * as React from 'react';
import { 
    useNavigate, Routes, Route
} from 'react-router-dom';
import APIClient from '../../api';
import Sidebar from '../sidebar';
import Projects from '../projects';
import Project from '../project';
import Users from '../users';
import User from '../user';
import NotFound from '../notFound';
import FeatureFlags from '../featureFlags';
import ContextFields from '../contextFields';
import FeatureFlag from '../featureFlag';
import ContextField from '../contextField';

function Main(): React.ReactElement {
    const navigate = useNavigate();

    React.useEffect(() => {
        APIClient.login.getLoginTest().catch(() => {
            navigate('/login', { replace: true });
        });
    }, []);

    return (
        <div
            style={{
                display: 'flex',
                height: '100%'
            }}
        >
            <div
                style={{
                    marginRight: '20px',
                    width: '200px',
                }}
            >
                <Sidebar />
            </div>
            <div
                style={{
                    width: '100%'
                }}
            >
                <Routes>
                    <Route index element={<Projects />} />
                    <Route path='project/:projectId' element={<Project />} />
                    <Route path='project/:projectId/feature-flags' element={<FeatureFlags />} />
                    <Route path='project/:projectId/feature-flag/:featureFlagId' element={<FeatureFlag />} />
                    <Route path='project/:projectId/context-fields' element={<ContextFields />} />
                    <Route path='project/:projectId/context-field/:contextFieldId' element={<ContextField />} />
                    <Route path='users' element={<Users />} />
                    <Route path='user/:userId' element={<User />} />
                    <Route path='*' element={<NotFound />} />
                </Routes>
            </div>
        </div>
    );
}

export default Main;
