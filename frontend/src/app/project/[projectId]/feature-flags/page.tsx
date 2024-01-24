'use client';

import { UserProvider } from "@/app/userProvider";
import FeatureFlags from "@/components/custom/featureFlags";
import { queryClient } from "@/utils/api";
import { QueryClientProvider } from "@tanstack/react-query";

export default function() {
    return (
		<QueryClientProvider client={queryClient}>
			<UserProvider>
				<FeatureFlags />
			</UserProvider>
		</QueryClientProvider>
    )
}
