/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CreateOrUpdateProject } from '../models/CreateOrUpdateProject';
import type { Project } from '../models/Project';
import type { ProjectPrivateKey } from '../models/ProjectPrivateKey';
import type { ProjectPrivateKeyName } from '../models/ProjectPrivateKeyName';
import type { ProjectPrivateKeys } from '../models/ProjectPrivateKeys';
import type { Projects } from '../models/Projects';
import type { ProjectWithPrivateKey } from '../models/ProjectWithPrivateKey';
import type { SuccessResponse } from '../models/SuccessResponse';
import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';
export class ProjectsService {
    constructor(public readonly httpRequest: BaseHttpRequest) {}
    /**
     * Get Projects
     * @param page
     * @param pageSize
     * @returns Projects Successful Response
     * @throws ApiError
     */
    public getProjects(
        page?: number,
        pageSize: number = 9223372036854776000
    ): CancelablePromise<Projects> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/projects',
            query: {
                page: page,
                page_size: pageSize
            },
            errors: {
                400: `Bad Request`
            }
        });
    }
    /**
     * Create Project
     * @param requestBody
     * @returns ProjectWithPrivateKey Successful Response
     * @throws ApiError
     */
    public createProject(
        requestBody: CreateOrUpdateProject
    ): CancelablePromise<ProjectWithPrivateKey> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/projects',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Bad Request`
            }
        });
    }
    /**
     * Get Project
     * @param projectId
     * @returns Project Successful Response
     * @throws ApiError
     */
    public getProject(projectId: number): CancelablePromise<Project> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/projects/{project_id}',
            path: {
                project_id: projectId
            },
            errors: {
                400: `Bad Request`
            }
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
        projectId: number,
        requestBody: CreateOrUpdateProject
    ): CancelablePromise<Project> {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/projects/{project_id}',
            path: {
                project_id: projectId
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Bad Request`
            }
        });
    }
    /**
     * Delete Project
     * @param projectId
     * @returns SuccessResponse Successful Response
     * @throws ApiError
     */
    public deleteProject(
        projectId: number
    ): CancelablePromise<SuccessResponse> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/projects/{project_id}',
            path: {
                project_id: projectId
            },
            errors: {
                400: `Bad Request`
            }
        });
    }
    /**
     * Create Project Private Key
     * @param projectId
     * @param requestBody
     * @returns ProjectPrivateKey Successful Response
     * @throws ApiError
     */
    public createProjectPrivateKey(
        projectId: number,
        requestBody: ProjectPrivateKeyName
    ): CancelablePromise<ProjectPrivateKey> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/projects/{project_id}/private_keys',
            path: {
                project_id: projectId
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Bad Request`
            }
        });
    }
    /**
     * Get Project Private Keys
     * @param projectId
     * @param page
     * @param pageSize
     * @returns ProjectPrivateKeys Successful Response
     * @throws ApiError
     */
    public getProjectPrivateKeys(
        projectId: number,
        page?: number,
        pageSize: number = 9223372036854776000
    ): CancelablePromise<ProjectPrivateKeys> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/projects/{project_id}/private_keys',
            path: {
                project_id: projectId
            },
            query: {
                page: page,
                page_size: pageSize
            },
            errors: {
                400: `Bad Request`
            }
        });
    }
    /**
     * Update Project Private Key
     * @param projectId
     * @param projectPrivateKeyId
     * @param requestBody
     * @returns SuccessResponse Successful Response
     * @throws ApiError
     */
    public updateProjectPrivateKey(
        projectId: number,
        projectPrivateKeyId: number,
        requestBody: ProjectPrivateKeyName
    ): CancelablePromise<SuccessResponse> {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/projects/{project_id}/private_keys/{project_private_key_id}',
            path: {
                project_id: projectId,
                project_private_key_id: projectPrivateKeyId
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Bad Request`
            }
        });
    }
    /**
     * Delete Project Private Key
     * @param projectId
     * @param projectPrivateKeyId
     * @returns SuccessResponse Successful Response
     * @throws ApiError
     */
    public deleteProjectPrivateKey(
        projectId: number,
        projectPrivateKeyId: number
    ): CancelablePromise<SuccessResponse> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/projects/{project_id}/private_keys/{project_private_key_id}',
            path: {
                project_id: projectId,
                project_private_key_id: projectPrivateKeyId
            },
            errors: {
                400: `Bad Request`
            }
        });
    }
}
