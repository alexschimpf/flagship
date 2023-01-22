/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ContextField } from '../models/ContextField';
import type { ContextFields } from '../models/ContextFields';
import type { CreateContextField } from '../models/CreateContextField';
import type { SuccessResponse } from '../models/SuccessResponse';
import type { UpdateContextField } from '../models/UpdateContextField';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class ContextFieldsService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

    /**
     * Get Context Fields
     * @param projectId
     * @returns ContextFields Successful Response
     * @throws ApiError
     */
    public getContextFields(
        projectId: string,
    ): CancelablePromise<ContextFields> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/context-fields',
            query: {
                'project_id': projectId,
            },
            errors: {
                400: `Bad Request`,
            },
        });
    }

    /**
     * Create Context Field
     * @param projectId
     * @param requestBody
     * @returns ContextField Successful Response
     * @throws ApiError
     */
    public createContextField(
        projectId: string,
        requestBody: CreateContextField,
    ): CancelablePromise<ContextField> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/context-fields',
            query: {
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
     * Get Context Field
     * @param contextFieldId
     * @param projectId
     * @returns ContextField Successful Response
     * @throws ApiError
     */
    public getContextField(
        contextFieldId: string,
        projectId: string,
    ): CancelablePromise<ContextField> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/context-fields/{context_field_id}',
            path: {
                'context_field_id': contextFieldId,
            },
            query: {
                'project_id': projectId,
            },
            errors: {
                400: `Bad Request`,
            },
        });
    }

    /**
     * Update Context Field
     * @param contextFieldId
     * @param projectId
     * @param requestBody
     * @returns ContextField Successful Response
     * @throws ApiError
     */
    public updateContextField(
        contextFieldId: string,
        projectId: string,
        requestBody: UpdateContextField,
    ): CancelablePromise<ContextField> {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/context-fields/{context_field_id}',
            path: {
                'context_field_id': contextFieldId,
            },
            query: {
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
     * Delete Context Field
     * @param contextFieldId
     * @param projectId
     * @returns SuccessResponse Successful Response
     * @throws ApiError
     */
    public deleteContextField(
        contextFieldId: string,
        projectId: string,
    ): CancelablePromise<SuccessResponse> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/context-fields/{context_field_id}',
            path: {
                'context_field_id': contextFieldId,
            },
            query: {
                'project_id': projectId,
            },
            errors: {
                400: `Bad Request`,
            },
        });
    }

}
