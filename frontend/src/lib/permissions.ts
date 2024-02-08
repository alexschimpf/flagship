import { User } from '@/api';

export enum Permission {
    // Projects
    CREATE_PROJECT,
    UPDATE_PROJECT,
    DELETE_PROJECT,
    READ_PROJECT_PRIVATE_KEYS,
    EDIT_PROJECT_PRIVATE_KEYS,
    CREATE_PROJECT_PRIVATE_KEY,
    DELETE_PROJECT_PRIVATE_KEY,

    // Feature flags
    CREATE_FEATURE_FLAG,
    UPDATE_FEATURE_FLAG,
    DELETE_FEATURE_FLAG,

    // Context fields
    CREATE_CONTEXT_FIELD,
    UPDATE_CONTEXT_FIELD,
    DELETE_CONTEXT_FIELD,
    READ_CONTEXT_FIELD_AUDIT_LOGS,

    // Users
    READ_USERS,
    INVITE_USER,
    UPDATE_USER,
    UPDATE_USER_PROJECTS,
    DELETE_USER,

    // Admin
    READ_SYSTEM_AUDIT_LOGS
}

export const hasPermission = (
    user: User | undefined,
    permission: Permission
): boolean => {
    if (!user) {
        return false;
    }

    if (user.role === 10) {
        return [
            Permission.CREATE_FEATURE_FLAG,
            Permission.UPDATE_FEATURE_FLAG,
            Permission.DELETE_FEATURE_FLAG,
            Permission.CREATE_CONTEXT_FIELD,
            Permission.UPDATE_CONTEXT_FIELD,
            Permission.DELETE_CONTEXT_FIELD,
            Permission.READ_CONTEXT_FIELD_AUDIT_LOGS
        ].includes(permission);
    } else if (user.role === 15) {
        return [
            Permission.CREATE_FEATURE_FLAG,
            Permission.UPDATE_FEATURE_FLAG,
            Permission.DELETE_FEATURE_FLAG,
            Permission.CREATE_CONTEXT_FIELD,
            Permission.UPDATE_CONTEXT_FIELD,
            Permission.DELETE_CONTEXT_FIELD,
            Permission.READ_CONTEXT_FIELD_AUDIT_LOGS,
            Permission.CREATE_PROJECT,
            Permission.UPDATE_PROJECT,
            Permission.READ_PROJECT_PRIVATE_KEYS,
            Permission.CREATE_PROJECT_PRIVATE_KEY,
            Permission.EDIT_PROJECT_PRIVATE_KEYS,
            Permission.READ_SYSTEM_AUDIT_LOGS,
            Permission.READ_USERS,
            Permission.INVITE_USER,
            Permission.UPDATE_USER,
            Permission.UPDATE_USER_PROJECTS,
            Permission.DELETE_USER
        ].includes(permission);
    } else if (user.role === 20) {
        return true;
    }

    return false;
};

export const permissionsSummary: readonly string[] = Object.freeze([
    'Read only users can view feature flags.',
    'Standard users can manage feature flags and context fields.',
    'Admins can do anything except delete projects and project private keys.',
    'Owners can do anything.'
]);
