/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { UserRole } from './UserRole';
export type UpdateUser = {
    name: string;
    /**
     * read only: 1</br>standard: 2</br>admin: 3</br>owner: 4
     */
    role: UserRole;
    projects: Array<number>;
};
