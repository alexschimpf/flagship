'use client';

import FeatureFlags from "@/components/custom/featureFlags";
import { queryClient } from "@/utils/api";
import { QueryClientProvider } from "@tanstack/react-query";

export default function() {
    return (
		<QueryClientProvider client={queryClient}>
			<FeatureFlags />
		</QueryClientProvider>
    )
}
