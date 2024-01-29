/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ContextField } from '../models/ContextField';
import type { ContextFieldAuditLogs } from '../models/ContextFieldAuditLogs';
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
     * @param page
     * @param pageSize
     * @returns ContextFields Successful Response
     * @throws ApiError
     */
    public getContextFields(
        projectId: number,
        page?: number,
        pageSize: number = 9223372036854776000,
    ): CancelablePromise<ContextFields> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/context_fields',
            query: {
                'project_id': projectId,
                'page': page,
                'page_size': pageSize,
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
        projectId: number,
        requestBody: CreateContextField,
    ): CancelablePromise<ContextField> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/context_fields',
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
        contextFieldId: number,
        projectId: number,
    ): CancelablePromise<ContextField> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/context_fields/{context_field_id}',
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
        contextFieldId: number,
        projectId: number,
        requestBody: UpdateContextField,
    ): CancelablePromise<ContextField> {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/context_fields/{context_field_id}',
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
        contextFieldId: number,
        projectId: number,
    ): CancelablePromise<SuccessResponse> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/context_fields/{context_field_id}',
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
     * Get Context Field Audit Logs
     * @param contextFieldId
     * @param projectId
     * @param page
     * @param pageSize
     * @returns ContextFieldAuditLogs Successful Response
     * @throws ApiError
     */
    public getContextFieldAuditLogs(
        contextFieldId: number,
        projectId: number,
        page?: number,
        pageSize: number = 100,
    ): CancelablePromise<ContextFieldAuditLogs> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/context_fields/{context_field_id}/audit_logs',
            path: {
                'context_field_id': contextFieldId,
            },
            query: {
                'project_id': projectId,
                'page': page,
                'page_size': pageSize,
            },
            errors: {
                400: `Bad Request`,
            },
        });
    }
}
