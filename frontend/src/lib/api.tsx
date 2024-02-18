import { APIClient, ApiError } from '@/api';
import { API_BASE_URL } from '@/app/config';
import {
    CheckCircledIcon,
    ExclamationTriangleIcon
} from '@radix-ui/react-icons';
import { QueryClient } from '@tanstack/react-query';
import axios from 'axios';
import parseHTML from 'html-react-parser';
import { ApiRequestOptions } from '../api/core/ApiRequestOptions';
import { BaseHttpRequest } from '../api/core/BaseHttpRequest';
import { CancelablePromise } from '../api/core/CancelablePromise';
import type { OpenAPIConfig } from '../api/core/OpenAPI';
import { request as __request } from '../api/core/request';

export class AxiosClient extends BaseHttpRequest {
    axiosInstance = axios.create();

    constructor(config: OpenAPIConfig) {
        super(config);

        this.axiosInstance.interceptors.response.use(
            response => response,
            error => {
                if (
                    error?.response?.status === 401 &&
                    window.location.pathname.indexOf('/login') !== 0 &&
                    window.location.pathname.indexOf('/forgot-password') !== 0
                ) {
                    window.location.replace(
                        `/login?return_url=${encodeURIComponent(window.location.pathname)}`
                    );
                }

                return Promise.reject(error);
            }
        );
    }

    public override request<T>(
        options: ApiRequestOptions
    ): CancelablePromise<T> {
        return __request(this.config, options, this.axiosInstance);
    }
}

export const apiClient = new APIClient(
    {
        BASE: API_BASE_URL,

        WITH_CREDENTIALS: true
    },
    AxiosClient
);
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
                <p className='text-foreground ml-2 font-bold'>Success!</p>
            </div>
        ),
        description: message
    };
};
