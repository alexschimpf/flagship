'use client';

import { queryClient } from '@/utils/api';
import { QueryClientProvider } from '@tanstack/react-query';
import { UserProvider } from '../userProvider';
import EditMyAccount from '@/components/custom/editMyAccount';

export default function() {
	return (
		<QueryClientProvider client={queryClient}>
			<UserProvider>
				<EditMyAccount />
			</UserProvider>
		</QueryClientProvider>
  )
}
