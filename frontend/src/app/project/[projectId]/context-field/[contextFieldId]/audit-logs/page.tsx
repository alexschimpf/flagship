'use client';

import ContextFieldAuditLogs from "@/components/custom/contextFieldAuditLogs";
import { queryClient } from "@/utils/api";
import { QueryClientProvider } from "@tanstack/react-query";

export default function() {
    return (
        <QueryClientProvider client={queryClient}>
            <ContextFieldAuditLogs />
        </QueryClientProvider>
    )
}
