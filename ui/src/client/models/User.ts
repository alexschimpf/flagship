/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { UserRole } from './UserRole';
import type { UserStatus } from './UserStatus';

export type User = {
    _id: string;
    email: string;
    name: string;
    /**
     * read only: 1</br>standard: 2</br>admin: 3
     */
    role: UserRole;
    projects: Array<string>;
    /**
     * invited: 1</br>activated: 2
     */
    status: UserStatus;
    created_date: string;
    updated_date: string;
};

