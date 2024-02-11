/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { FeatureFlagChange } from './FeatureFlagChange';
export type FeatureFlagAuditLog = {
    actor: string;
    event_time: string;
    changes: Array<FeatureFlagChange>;
};
