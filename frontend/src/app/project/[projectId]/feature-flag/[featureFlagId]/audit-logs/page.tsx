'use client';

import { UserProvider } from "@/app/userProvider";
import FeatureFlagAuditLogs from "@/components/custom/featureFlagAuditLogs";
import { queryClient } from "@/utils/api";
import { QueryClientProvider } from "@tanstack/react-query";

export default function() {
    return (
        <QueryClientProvider client={queryClient}>
            <UserProvider>
                <FeatureFlagAuditLogs />
            </UserProvider>
        </QueryClientProvider>
    )
}
