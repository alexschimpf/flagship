import { APIClient, ApiError } from "@/api";
import { QueryClient } from "@tanstack/react-query";


export const apiClient = new APIClient({ BASE: 'http://localhost:8000' });
export const queryClient = new QueryClient();

export const getErrorMessage = (error: Error | string): string => {
    let errorStr: string;
    if (error instanceof ApiError) {
        errorStr = error.body.errors.map((e: any) => e.message).join('<br><br>');
    } else if (typeof error === 'string') {
        errorStr = error;
    } else {
        errorStr = 'Oops, something went wrong. Please try again.';
    }
    return errorStr;
};
