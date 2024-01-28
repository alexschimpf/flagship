/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Operator } from './Operator';
export type FeatureFlagCondition = {
    context_key: string;
    /**
     * equals: 1</br>not equals: 2</br>less than: 3</br>less than or equal to: 4</br>greater than: 5</br>greater than or equal to: 6</br>matches regex: 7</br>in list: 8</br>not in list: 9</br>intersects: 10</br>not intersects: 11</br>contains: 12</br>not contains: 13
     */
    operator: Operator;
    value: any;
};
