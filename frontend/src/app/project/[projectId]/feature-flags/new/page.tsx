'use client';

import { UserProvider } from '@/app/userProvider';
import NewFeatureFlag from '@/components/custom/newFeatureFlag';
import { queryClient } from '@/utils/api';
import { QueryClientProvider } from '@tanstack/react-query';

export default function() {
	return (
		<QueryClientProvider client={queryClient}>
			<UserProvider>
				< NewFeatureFlag />
			</UserProvider>
		</QueryClientProvider>
  )
}
