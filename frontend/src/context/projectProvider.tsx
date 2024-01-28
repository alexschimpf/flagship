import { Project } from '@/api';
import { apiClient } from '@/lib/api';
import { useParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import { ProjectContext } from './projectContext';

export const ProjectProvider = ({ children }: any) => {
    const params = useParams<{ projectId: string }>();
    const [project, setProject] = useState<Project | undefined>(undefined);

    useEffect(() => {
        if (
            params.projectId &&
            project?.project_id !== parseInt(params.projectId)
        ) {
            apiClient.projects
                .getProject(parseInt(params.projectId))
                .then((data: Project) => {
                    setProject(data);
                });
        }
    }, [params.projectId]);

    return (
        <ProjectContext.Provider value={project}>
            {children}
        </ProjectContext.Provider>
    );
};
