'use client';

import NewContextField from '@/components/custom/newContextField';
import { queryClient } from '@/utils/api';
import { QueryClientProvider } from '@tanstack/react-query';

export default function() {
	return (
		<QueryClientProvider client={queryClient}>
			< NewContextField />
		</QueryClientProvider>
  )
}
