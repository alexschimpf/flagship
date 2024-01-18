'use client';

import NewFeatureFlag from '@/components/custom/newFeatureFlag';
import { queryClient } from '@/utils/api';
import { QueryClientProvider } from '@tanstack/react-query';

export default function() {
	return (
		<QueryClientProvider client={queryClient}>
			< NewFeatureFlag />
		</QueryClientProvider>
  )
}
