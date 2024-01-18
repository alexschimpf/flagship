'use client';

import EditContextField from "@/components/custom/editContextField";
import { queryClient } from "@/utils/api";
import { QueryClientProvider } from "@tanstack/react-query";

export default function() {
    return (
        <QueryClientProvider client={queryClient}>
            <EditContextField />
        </QueryClientProvider>
    )
}
