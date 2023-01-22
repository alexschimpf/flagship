/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ContextValueType } from './ContextValueType';

export type ContextField = {
    _id: string;
    name: string;
    key: string;
    value_type: ContextValueType;
    description: string;
    enum_def?: string;
    created_date: string;
    updated_date: string;
};

