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
    /**
     * read only: 1</br>standard: 2</br>admin: 3</br>owner: 4
     */
    role: UserRole;
    projects: Array<number>;
    /**
     * invited: 1</br>activated: 2
     */
    status: UserStatus;
    created_date: string;
    updated_date: string;
};
