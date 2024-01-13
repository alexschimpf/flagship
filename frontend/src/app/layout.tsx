import type { Metadata } from 'next'
import './globals.css'

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
            <body>{children}</body>
        </html>
  )
}
