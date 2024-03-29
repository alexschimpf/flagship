/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_set_password_users_password_set_post } from '../models/Body_set_password_users_password_set_post';
import type { InviteUser } from '../models/InviteUser';
import type { ResetPassword } from '../models/ResetPassword';
import type { SuccessResponse } from '../models/SuccessResponse';
import type { UpdateUser } from '../models/UpdateUser';
import type { User } from '../models/User';
import type { Users } from '../models/Users';
import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';
export class UsersService {
    constructor(public readonly httpRequest: BaseHttpRequest) {}
    /**
     * Get Users
     * @param page
     * @param pageSize
     * @returns Users Successful Response
     * @throws ApiError
     */
    public getUsers(
        page?: number,
        pageSize: number = 9223372036854776000
    ): CancelablePromise<Users> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/users',
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
     * Invite User
     * @param requestBody
     * @returns User Successful Response
     * @throws ApiError
     */
    public inviteUser(requestBody: InviteUser): CancelablePromise<User> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/users',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Bad Request`
            }
        });
    }
    /**
     * Get Me
     * @returns User Successful Response
     * @throws ApiError
     */
    public getMe(): CancelablePromise<User> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/users/me',
            errors: {
                400: `Bad Request`
            }
        });
    }
    /**
     * Get User
     * @param userId
     * @returns User Successful Response
     * @throws ApiError
     */
    public getUser(userId: number): CancelablePromise<User> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/users/{user_id}',
            path: {
                user_id: userId
            },
            errors: {
                400: `Bad Request`
            }
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
        userId: number,
        requestBody: UpdateUser
    ): CancelablePromise<User> {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/users/{user_id}',
            path: {
                user_id: userId
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Bad Request`
            }
        });
    }
    /**
     * Delete User
     * @param userId
     * @returns SuccessResponse Successful Response
     * @throws ApiError
     */
    public deleteUser(userId: number): CancelablePromise<SuccessResponse> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/users/{user_id}',
            path: {
                user_id: userId
            },
            errors: {
                400: `Bad Request`
            }
        });
    }
    /**
     * Set Password
     * @param formData
     * @returns void
     * @throws ApiError
     */
    public setPassword(
        formData: Body_set_password_users_password_set_post
    ): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/users/password/set',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                307: `Successful Response`,
                400: `Bad Request`
            }
        });
    }
    /**
     * Reset Password
     * @param requestBody
     * @returns SuccessResponse Successful Response
     * @throws ApiError
     */
    public resetPassword(
        requestBody: ResetPassword
    ): CancelablePromise<SuccessResponse> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/users/password/reset',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Bad Request`
            }
        });
    }
}
