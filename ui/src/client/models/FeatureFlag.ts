/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { FeatureFlagCondition } from './FeatureFlagCondition';

export type FeatureFlag = {
    _id: string;
    name: string;
    description: string;
    enabled: boolean;
    conditions: Array<Array<FeatureFlagCondition>>;
    created_date: string;
    updated_date: string;
};

