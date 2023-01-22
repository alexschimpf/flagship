/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { UserRole } from './UserRole';

export type InviteUser = {
    email: string;
    name: string;
    role: UserRole;
    projects: Array<string>;
};

