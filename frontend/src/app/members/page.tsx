'use client';

import Members from '@/components/custom/members';
import { queryClient } from '@/utils/api';
import { QueryClientProvider } from '@tanstack/react-query';

export default function() {
	return (
		<QueryClientProvider client={queryClient}>
			<Members />
		</QueryClientProvider>
  )
}
