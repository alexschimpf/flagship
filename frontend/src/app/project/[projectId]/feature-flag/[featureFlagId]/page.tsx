'use client';

import EditFeatureFlag from "@/components/custom/editFeatureFlag";
import { queryClient } from "@/utils/api";
import { QueryClientProvider } from "@tanstack/react-query";

export default function() {
    return (
        <QueryClientProvider client={queryClient}>
            <EditFeatureFlag />
        </QueryClientProvider>
    )
}
