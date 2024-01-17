'use client';

import { useParams } from "next/navigation";

export default function() {
    const params = useParams<{ projectId: string }>();

    const projectId = parseInt(params.projectId);

    return (
        <div>Project {projectId}</div>
    )
}
