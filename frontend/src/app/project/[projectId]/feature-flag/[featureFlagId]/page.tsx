'use client';

import { UserProvider } from "@/app/userProvider";
import EditFeatureFlag from "@/components/custom/editFeatureFlag";
import { queryClient } from "@/utils/api";
import { QueryClientProvider } from "@tanstack/react-query";

export default function() {
    return (
        <QueryClientProvider client={queryClient}>
            <UserProvider>
                <EditFeatureFlag />
            </UserProvider>
        </QueryClientProvider>
    )
}
