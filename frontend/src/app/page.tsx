'use client';

import Projects from '@/components/custom/projects';
import { queryClient } from '@/utils/api';
import { QueryClientProvider } from '@tanstack/react-query';
import { UserProvider } from './userProvider';

export default function() {
	return (
		<QueryClientProvider client={queryClient}>
			<UserProvider>
				<Projects />
			</UserProvider>
		</QueryClientProvider>
  )
}
