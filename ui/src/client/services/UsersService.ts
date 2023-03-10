/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { InviteUser } from '../models/InviteUser';
import type { ResetPassword } from '../models/ResetPassword';
import type { SetPassword } from '../models/SetPassword';
import type { SuccessResponse } from '../models/SuccessResponse';
import type { UpdateUser } from '../models/UpdateUser';
import type { User } from '../models/User';
import type { Users } from '../models/Users';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class UsersService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

    /**
     * Set Password
     * @param requestBody
     * @returns SuccessResponse Successful Response
     * @throws ApiError
     */
    public setPassword(
        requestBody: SetPassword,
    ): CancelablePromise<SuccessResponse> {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/users/password',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Bad Request`,
            },
        });
    }

    /**
     * Reset Password
     * @param requestBody
     * @returns SuccessResponse Successful Response
     * @throws ApiError
     */
    public resetPassword(
        requestBody: ResetPassword,
    ): CancelablePromise<SuccessResponse> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/users/password/reset',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Bad Request`,
            },
        });
    }

    /**
     * Get Users
     * @returns Users Successful Response
     * @throws ApiError
     */
    public getUsers(): CancelablePromise<Users> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/users',
            errors: {
                400: `Bad Request`,
            },
        });
    }

    /**
     * Invite User
     * @param requestBody
     * @returns User Successful Response
     * @throws ApiError
     */
    public inviteUser(
        requestBody: InviteUser,
    ): CancelablePromise<User> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/users',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Bad Request`,
            },
        });
    }

    /**
     * Get User
     * @param userId
     * @returns User Successful Response
     * @throws ApiError
     */
    public getUser(
        userId: string,
    ): CancelablePromise<User> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/users/{user_id}',
            path: {
                'user_id': userId,
            },
            errors: {
                400: `Bad Request`,
            },
        });
    }

    /**
     * Update User
     * @param userId
     * @param requestBody
     * @returns User Successful Response
     * @throws ApiError
     */
    public updateUser(
        userId: string,
        requestBody: UpdateUser,
    ): CancelablePromise<User> {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/users/{user_id}',
            path: {
                'user_id': userId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Bad Request`,
            },
        });
    }

    /**
     * Delete User
     * @param userId
     * @returns SuccessResponse Successful Response
     * @throws ApiError
     */
    public deleteUser(
        userId: string,
    ): CancelablePromise<SuccessResponse> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/users/{user_id}',
            path: {
                'user_id': userId,
            },
            errors: {
                400: `Bad Request`,
            },
        });
    }

}
