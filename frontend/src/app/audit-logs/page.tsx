'use client';

import AuditLogs from '@/components/custom/auditLogs';
import { queryClient } from '@/utils/api';
import { QueryClientProvider } from '@tanstack/react-query';



export default function() {
	return (
		<QueryClientProvider client={queryClient}>
			<AuditLogs />
		</QueryClientProvider>
  )
}
