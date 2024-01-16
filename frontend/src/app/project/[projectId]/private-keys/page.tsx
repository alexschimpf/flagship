'use client';

import ProjectPrivateKeys from '@/components/custom/projectPrivateKeys';
import { queryClient } from '@/utils/api';
import { QueryClientProvider } from '@tanstack/react-query';

interface ProjectPrivateKeyPageProps {
	projectId: string
}

export default function(params: ProjectPrivateKeyPageProps) {
	return (
		<QueryClientProvider client={queryClient}>
			< ProjectPrivateKeys/>
		</QueryClientProvider>
  )
}
