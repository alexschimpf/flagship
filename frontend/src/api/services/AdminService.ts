/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { SystemAuditLogs } from '../models/SystemAuditLogs';
import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';
export class AdminService {
    constructor(public readonly httpRequest: BaseHttpRequest) {}
    /**
     * Get Audit Logs
     * @param page
     * @param pageSize
     * @returns SystemAuditLogs Successful Response
     * @throws ApiError
     */
    public getAuditLogs(
        page?: number,
        pageSize: number = 100,
    ): CancelablePromise<SystemAuditLogs> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/admin/audit_logs',
            query: {
                'page': page,
                'page_size': pageSize,
            },
            errors: {
                400: `Bad Request`,
            },
        });
    }
}
