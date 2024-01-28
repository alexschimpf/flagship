/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CreateOrUpdateFeatureFlag } from '../models/CreateOrUpdateFeatureFlag';
import type { FeatureFlag } from '../models/FeatureFlag';
import type { FeatureFlagAuditLogs } from '../models/FeatureFlagAuditLogs';
import type { FeatureFlags } from '../models/FeatureFlags';
import type { SuccessResponse } from '../models/SuccessResponse';
import type { UpdateFeatureFlagStatus } from '../models/UpdateFeatureFlagStatus';
import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';
export class FeatureFlagsService {
    constructor(public readonly httpRequest: BaseHttpRequest) {}
    /**
     * Get Feature Flags
     * @param projectId
     * @param page
     * @param pageSize
     * @returns FeatureFlags Successful Response
     * @throws ApiError
     */
    public getFeatureFlags(
        projectId: number,
        page?: number,
        pageSize: number = 50
    ): CancelablePromise<FeatureFlags> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/feature_flags',
            query: {
                project_id: projectId,
                page: page,
                page_size: pageSize
            },
            errors: {
                400: `Bad Request`
            }
        });
    }
    /**
     * Create Feature Flag
     * @param projectId
     * @param requestBody
     * @returns FeatureFlag Successful Response
     * @throws ApiError
     */
    public createFeatureFlag(
        projectId: number,
        requestBody: CreateOrUpdateFeatureFlag
    ): CancelablePromise<FeatureFlag> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/feature_flags',
            query: {
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
     * Get Feature Flag
     * @param featureFlagId
     * @param projectId
     * @returns FeatureFlag Successful Response
     * @throws ApiError
     */
    public getFeatureFlag(
        featureFlagId: number,
        projectId: number
    ): CancelablePromise<FeatureFlag> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/feature_flags/{feature_flag_id}',
            path: {
                feature_flag_id: featureFlagId
            },
            query: {
                project_id: projectId
            },
            errors: {
                400: `Bad Request`
            }
        });
    }
    /**
     * Update Feature Flag
     * @param featureFlagId
     * @param projectId
     * @param requestBody
     * @returns FeatureFlag Successful Response
     * @throws ApiError
     */
    public updateFeatureFlag(
        featureFlagId: number,
        projectId: number,
        requestBody: CreateOrUpdateFeatureFlag
    ): CancelablePromise<FeatureFlag> {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/feature_flags/{feature_flag_id}',
            path: {
                feature_flag_id: featureFlagId
            },
            query: {
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
     * Delete Feature Flag
     * @param featureFlagId
     * @param projectId
     * @returns SuccessResponse Successful Response
     * @throws ApiError
     */
    public deleteFeatureFlag(
        featureFlagId: number,
        projectId: number
    ): CancelablePromise<SuccessResponse> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/feature_flags/{feature_flag_id}',
            path: {
                feature_flag_id: featureFlagId
            },
            query: {
                project_id: projectId
            },
            errors: {
                400: `Bad Request`
            }
        });
    }
    /**
     * Get Feature Flag Audit Logs
     * @param featureFlagId
     * @param projectId
     * @param page
     * @param pageSize
     * @returns FeatureFlagAuditLogs Successful Response
     * @throws ApiError
     */
    public getFeatureFlagAuditLogs(
        featureFlagId: number,
        projectId: number,
        page?: number,
        pageSize: number = 50
    ): CancelablePromise<FeatureFlagAuditLogs> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/feature_flags/{feature_flag_id}/audit_logs',
            path: {
                feature_flag_id: featureFlagId
            },
            query: {
                project_id: projectId,
                page: page,
                page_size: pageSize
            },
            errors: {
                400: `Bad Request`
            }
        });
    }
    /**
     * Update Feature Flag Status
     * @param featureFlagId
     * @param projectId
     * @param requestBody
     * @returns SuccessResponse Successful Response
     * @throws ApiError
     */
    public updateFeatureFlagStatus(
        featureFlagId: number,
        projectId: number,
        requestBody: UpdateFeatureFlagStatus
    ): CancelablePromise<SuccessResponse> {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/feature_flags/{feature_flag_id}/status',
            path: {
                feature_flag_id: featureFlagId
            },
            query: {
                project_id: projectId
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Bad Request`
            }
        });
    }
}
