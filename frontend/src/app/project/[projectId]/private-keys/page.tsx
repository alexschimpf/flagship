'use client';

import { UserProvider } from '@/app/userProvider';
import ProjectPrivateKeys from '@/components/custom/projectPrivateKeys';
import { queryClient } from '@/utils/api';
import { QueryClientProvider } from '@tanstack/react-query';

export default function() {
	return (
		<QueryClientProvider client={queryClient}>
			<UserProvider>
				< ProjectPrivateKeys />
			</UserProvider>
		</QueryClientProvider>
  )
}
