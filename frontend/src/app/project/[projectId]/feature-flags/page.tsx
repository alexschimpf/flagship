'use client';

import { queryClient } from "@/utils/api";
import { QueryClientProvider } from "@tanstack/react-query";

export default function() {
    return (
		<QueryClientProvider client={queryClient}>
			<div>feature flags</div>
		</QueryClientProvider>
    )
}
