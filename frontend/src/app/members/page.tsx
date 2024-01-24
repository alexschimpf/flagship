'use client';

import Members from '@/components/custom/members';
import { queryClient } from '@/utils/api';
import { QueryClientProvider } from '@tanstack/react-query';
import { UserProvider } from '../userProvider';

export default function() {
	return (
		<QueryClientProvider client={queryClient}>
			<UserProvider>
				<Members />
			</UserProvider>
		</QueryClientProvider>
  )
}
