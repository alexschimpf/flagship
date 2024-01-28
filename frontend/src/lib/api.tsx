import { APIClient, ApiError } from '@/api';
import {
    CheckCircledIcon,
    ExclamationTriangleIcon
} from '@radix-ui/react-icons';
import { QueryClient } from '@tanstack/react-query';
import parseHTML from 'html-react-parser';

export const apiClient = new APIClient({ BASE: 'http://localhost:8000' });
export const queryClient = new QueryClient();

export const getErrorMessage = (error: Error | string): string => {
    let errorStr: string;
    if (error instanceof ApiError) {
        errorStr = error.body.errors
            .map((e: any) => e.message)
            .join('<br><br>');
    } else if (typeof error === 'string') {
        errorStr = error;
    } else {
        errorStr = 'Oops, something went wrong. Please try again.';
    }
    return errorStr;
};

export const getErrorToast = (error: Error | string): any => {
    return {
        variant: 'destructive',
        title: (
            <div className='flex flex-row items-center'>
                <ExclamationTriangleIcon />
                <p className='text-white ml-2 font-bold'>Uh oh...</p>
            </div>
        ),
        description: <p>{parseHTML(getErrorMessage(error))}</p>
    };
};

export const getSuccessToast = (message: string): any => {
    return {
        variant: 'success',
        title: (
            <div className='flex flex-row items-center'>
                <CheckCircledIcon />
                <p className='text-black ml-2 font-bold'>Success!</p>
            </div>
        ),
        description: message
    };
};
