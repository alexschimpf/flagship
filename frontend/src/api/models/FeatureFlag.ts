/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { FeatureFlagCondition } from './FeatureFlagCondition';
export type FeatureFlag = {
    feature_flag_id: number;
    name: string;
    description: string;
    enabled: boolean;
    conditions: Array<Array<FeatureFlagCondition>>;
    created_date: string;
    updated_date: string;
};

