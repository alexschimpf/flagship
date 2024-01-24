'use client';

import { UserProvider } from "@/app/userProvider";
import ContextFields from "@/components/custom/contextFields";
import { queryClient } from "@/utils/api";
import { QueryClientProvider } from "@tanstack/react-query";

export default function() {
    return (
		<QueryClientProvider client={queryClient}>
			<UserProvider>
				<ContextFields />
			</UserProvider>
		</QueryClientProvider>
    )
}
