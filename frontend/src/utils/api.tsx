import { APIClient, ApiError } from "@/api";
import { QueryClient } from "@tanstack/react-query";


export const apiClient = new APIClient({BASE: 'http://localhost:8000'});

export const queryClient = new QueryClient()

export const getErrorMessage = (error: Error | string): string => {
    let errorStr: string;
    if (error instanceof ApiError) {
        errorStr = error.body.errors.map((e: any) => e.message).join('\n')
    } else if (typeof error === 'string') {
        errorStr = error;
    } else {
        errorStr = 'Oops, something went wrong. Please try again.'
    }
    return errorStr;
}

export const userRoles = {
    1: 'Read only',
    2: 'Standard',
    3: 'Admin',
    4: 'Owner'
}

export const userStatuses = {
    1: 'Invited',
    2: 'Activated',
}

export const contextFieldValueTypes = {
    1: 'String',
    2: 'Number',
    3: 'Integer',
    4: 'Boolean',
    5: 'Enum',
    6: 'Version',
    7: 'String List',
    8: 'Integer List',
    9: 'Enum List'
}
