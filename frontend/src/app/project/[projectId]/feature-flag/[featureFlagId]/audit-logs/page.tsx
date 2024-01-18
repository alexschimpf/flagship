'use client';

import FeatureFlagAuditLogs from "@/components/custom/featureFlagAuditLogs";
import { queryClient } from "@/utils/api";
import { QueryClientProvider } from "@tanstack/react-query";

export default function() {
    return (
        <QueryClientProvider client={queryClient}>
            <FeatureFlagAuditLogs />
        </QueryClientProvider>
    )
}
