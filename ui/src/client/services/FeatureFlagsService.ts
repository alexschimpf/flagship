/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CreateOrUpdateFeatureFlag } from '../models/CreateOrUpdateFeatureFlag';
import type { FeatureFlag } from '../models/FeatureFlag';
import type { FeatureFlags } from '../models/FeatureFlags';
import type { SuccessResponse } from '../models/SuccessResponse';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class FeatureFlagsService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

    /**
     * Get Feature Flags
     * @param projectId
     * @returns FeatureFlags Successful Response
     * @throws ApiError
     */
    public getFeatureFlags(
        projectId: string,
    ): CancelablePromise<FeatureFlags> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/feature-flags',
            query: {
                'project_id': projectId,
            },
            errors: {
                400: `Bad Request`,
            },
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
        projectId: string,
        requestBody: CreateOrUpdateFeatureFlag,
    ): CancelablePromise<FeatureFlag> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/feature-flags',
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
     * Get Feature Flag
     * @param featureFlagId
     * @param projectId
     * @returns FeatureFlag Successful Response
     * @throws ApiError
     */
    public getFeatureFlag(
        featureFlagId: string,
        projectId: string,
    ): CancelablePromise<FeatureFlag> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/feature-flags/{feature_flag_id}',
            path: {
                'feature_flag_id': featureFlagId,
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
     * Update Feature Flag
     * @param featureFlagId
     * @param projectId
     * @param requestBody
     * @returns FeatureFlag Successful Response
     * @throws ApiError
     */
    public updateFeatureFlag(
        featureFlagId: string,
        projectId: string,
        requestBody: CreateOrUpdateFeatureFlag,
    ): CancelablePromise<FeatureFlag> {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/feature-flags/{feature_flag_id}',
            path: {
                'feature_flag_id': featureFlagId,
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
     * Delete Feature Flag
     * @param featureFlagId
     * @param projectId
     * @returns SuccessResponse Successful Response
     * @throws ApiError
     */
    public deleteFeatureFlag(
        featureFlagId: string,
        projectId: string,
    ): CancelablePromise<SuccessResponse> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/feature-flags/{feature_flag_id}',
            path: {
                'feature_flag_id': featureFlagId,
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
