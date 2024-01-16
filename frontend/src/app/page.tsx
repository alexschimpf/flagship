'use client';

import Projects from '@/components/custom/projects';
import { queryClient } from '@/utils/api';
import { QueryClientProvider } from '@tanstack/react-query';

export default function() {
	return (
		<QueryClientProvider client={queryClient}>
			<Projects />
		</QueryClientProvider>
  )
}
