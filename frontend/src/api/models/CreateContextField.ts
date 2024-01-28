/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ContextValueType } from './ContextValueType';
export type CreateContextField = {
    name: string;
    field_key: string;
    /**
     * string: 1</br>number: 2</br>integer: 3</br>boolean: 4</br>enum: 5</br>version: 6</br>string list: 7</br>integer list: 8</br>enum list: 9
     */
    value_type: ContextValueType;
    description?: string;
    enum_def?: Record<string, any> | null;
};
