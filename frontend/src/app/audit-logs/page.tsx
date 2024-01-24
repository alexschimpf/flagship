'use client';

import AuditLogs from '@/components/custom/auditLogs';
import { queryClient } from '@/utils/api';
import { QueryClientProvider } from '@tanstack/react-query';
import { UserProvider } from '../userProvider';

export default function() {
	return (
		<QueryClientProvider client={queryClient}>
			<UserProvider>
				<AuditLogs />
			</UserProvider>
		</QueryClientProvider>
  )
}
