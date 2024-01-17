'use client';

import ContextFields from "@/components/custom/contextFields";
import { queryClient } from "@/utils/api";
import { QueryClientProvider } from "@tanstack/react-query";

export default function() {
    return (
		<QueryClientProvider client={queryClient}>
			<ContextFields />
		</QueryClientProvider>
    )
}
