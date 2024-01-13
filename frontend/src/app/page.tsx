import Header from '@/components/custom/header'
import Main from '@/components/custom/main'
import Footer from '@/components/custom/footer'

export default function Home() {
	return (
		<main className='min-h-screen bg-background font-sans'>
			<div className='relative flex min-h-screen flex-col'>
				<Header />
				<Main />
				<Footer />
			</div>
   	 	</main>
  )
}
