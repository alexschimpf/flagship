import { User } from "@/api";

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
    READ_FEATURE_FLAG_AUDIT_LOGS,

    // Context fields
    CREATE_CONTEXT_FIELD,
    UPDATE_CONTEXT_FIELD,
    DELETE_CONTEXT_FIELD,
    READ_CONTEXT_FIELD_AUDIT_LOGS,

    // Users
    READ_USERS,
    INVITE_USER,
    UPDATE_USER,
    DELETE_USER ,

    // Admin
    READ_SYSTEM_AUDIT_LOGS
}

export const hasPermission = (user: User | undefined, permission: Permission): boolean => {
    if (!user) {
        return false;
    }

    if (user.role === 2) {
        return [
            Permission.CREATE_FEATURE_FLAG,
            Permission.UPDATE_FEATURE_FLAG,
            Permission.DELETE_FEATURE_FLAG,
            Permission.READ_FEATURE_FLAG_AUDIT_LOGS
        ].includes(permission);
    } else if (user.role === 3) {
        return [
            Permission.CREATE_FEATURE_FLAG,
            Permission.UPDATE_FEATURE_FLAG,
            Permission.DELETE_FEATURE_FLAG,
            Permission.CREATE_CONTEXT_FIELD,
            Permission.UPDATE_CONTEXT_FIELD,
            Permission.DELETE_CONTEXT_FIELD,
            Permission.READ_FEATURE_FLAG_AUDIT_LOGS,
            Permission.READ_CONTEXT_FIELD_AUDIT_LOGS,
            Permission.READ_SYSTEM_AUDIT_LOGS
        ].includes(permission)
    }
    else if (user.role === 4) {
        return true
    }

    return false
}
