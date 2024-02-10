/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { UserRole } from './UserRole';
import type { UserStatus } from './UserStatus';
export type User = {
    user_id: number;
    email: string;
    name: string;
    role: UserRole;
    projects: Array<number>;
    status: UserStatus;
    created_date: string;
    updated_date: string;
};

