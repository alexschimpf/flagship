/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CreateOrUpdateProject } from '../models/CreateOrUpdateProject';
import type { Project } from '../models/Project';
import type { Projects } from '../models/Projects';
import type { ProjectWithPrivateKey } from '../models/ProjectWithPrivateKey';
import type { SuccessResponse } from '../models/SuccessResponse';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class ProjectsService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

    /**
     * Get Projects
     * @returns Projects Successful Response
     * @throws ApiError
     */
    public getProjects(): CancelablePromise<Projects> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/projects',
            errors: {
                400: `Bad Request`,
            },
        });
    }

    /**
     * Create Project
     * @param requestBody
     * @returns ProjectWithPrivateKey Successful Response
     * @throws ApiError
     */
    public createProject(
        requestBody: CreateOrUpdateProject,
    ): CancelablePromise<ProjectWithPrivateKey> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/projects',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Bad Request`,
            },
        });
    }

    /**
     * Get Project
     * @param projectId
     * @returns Project Successful Response
     * @throws ApiError
     */
    public getProject(
        projectId: string,
    ): CancelablePromise<Project> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/projects/{project_id}',
            path: {
                'project_id': projectId,
            },
            errors: {
                400: `Bad Request`,
            },
        });
    }

    /**
     * Update Project
     * @param projectId
     * @param requestBody
     * @returns Project Successful Response
     * @throws ApiError
     */
    public updateProject(
        projectId: string,
        requestBody: CreateOrUpdateProject,
    ): CancelablePromise<Project> {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/projects/{project_id}',
            path: {
                'project_id': projectId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Bad Request`,
            },
        });
    }

    /**
     * Delete Project
     * @param projectId
     * @returns SuccessResponse Successful Response
     * @throws ApiError
     */
    public deleteProject(
        projectId: string,
    ): CancelablePromise<SuccessResponse> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/projects/{project_id}',
            path: {
                'project_id': projectId,
            },
            errors: {
                400: `Bad Request`,
            },
        });
    }

    /**
     * Reset Project Private Key
     * @param projectId
     * @returns ProjectWithPrivateKey Successful Response
     * @throws ApiError
     */
    public resetProjectPrivateKey(
        projectId: string,
    ): CancelablePromise<ProjectWithPrivateKey> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/projects/{project_id}/private_key',
            path: {
                'project_id': projectId,
            },
            errors: {
                400: `Bad Request`,
            },
        });
    }

}
