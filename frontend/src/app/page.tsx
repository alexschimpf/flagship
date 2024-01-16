'use client';

import Header from '@/components/custom/header'
import Main from '@/components/custom/main'
import Footer from '@/components/custom/footer'
import {
	QueryClient,
	QueryClientProvider,
} from '@tanstack/react-query'
  

const queryClient = new QueryClient()

export default function Home() {
	return (
		<QueryClientProvider client={queryClient}>
			<main className='min-h-screen bg-background font-sans'>
				<div className='relative flex min-h-screen flex-col'>
					<Header />
					<Main />
					<Footer />
				</div>
			</main>
		</QueryClientProvider>
  )
}
