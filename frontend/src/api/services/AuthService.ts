/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_login_auth_login_post } from '../models/Body_login_auth_login_post';
import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';
export class AuthService {
    constructor(public readonly httpRequest: BaseHttpRequest) {}
    /**
     * Login
     * @param formData
     * @returns void
     * @throws ApiError
     */
    public login(
        formData: Body_login_auth_login_post
    ): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/auth/login',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                307: `Successful Response`,
                400: `Bad Request`
            }
        });
    }
    /**
     * Login Test
     * @returns void
     * @throws ApiError
     */
    public loginTest(): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/auth/login/test',
            errors: {
                307: `Successful Response`,
                400: `Bad Request`
            }
        });
    }
    /**
     * Logout
     * @returns void
     * @throws ApiError
     */
    public logout(): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/auth/logout',
            errors: {
                307: `Successful Response`,
                400: `Bad Request`
            }
        });
    }
}
