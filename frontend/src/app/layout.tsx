import Footer from '@/components/custom/footer';
import Header from '@/components/custom/header';
import { Toaster } from '@/components/ui/toaster';
import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
    title: 'Flagship',
    description: 'Feature flag management'
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en">
            <head>
                <link rel="icon" href="/favicon.svg" sizes="any" />
            </head>
            <body>
                <div className='min-h-screen bg-background font-sans flex flex-col'>
                    <Header />
                    <div className='flex-1 flex flex-col container items-center w-3/4'>
                        {children}
                    </div>
                    <Footer />
                    <Toaster />
                </div>
            </body>
        </html>
  )
}
