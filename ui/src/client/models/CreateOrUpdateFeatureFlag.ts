/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { FeatureFlagCondition } from './FeatureFlagCondition';

export type CreateOrUpdateFeatureFlag = {
    name: string;
    description?: string;
    enabled: boolean;
    conditions?: Array<Array<FeatureFlagCondition>>;
};

