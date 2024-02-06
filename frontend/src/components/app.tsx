'use client';

import { ProjectProvider } from '@/context/projectProvider';
import { apiClient, queryClient } from '@/lib/api';
import { QueryClientProvider } from '@tanstack/react-query';
import { ThemeProvider } from "next-themes";
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import { UserProvider } from '../context/userProvider';
import Footer from './footer';
import Header from './header';
import { Toaster } from './primitives/toaster';

export default function App({ children }: any) {
    const router = useRouter();
    useEffect(() => {
        apiClient.auth.loginTest().catch(() => {
            router.push('/login');
        });
    }, [router]);

    let theme = 'dark';
    if (typeof window !== 'undefined') {
        theme = localStorage.getItem('theme') || 'dark';
    }

    return (
        <div className='flex-1 flex flex-col container items-center w-3/4'>
            <QueryClientProvider client={queryClient}>
                <ThemeProvider
                    attribute='class'
                    defaultTheme={theme}
                    enableSystem
                >
                    <UserProvider>
                        <ProjectProvider>
                            <Header />
                            <div className='flex-1 w-full'>{children}</div>
                            <Footer />
                        </ProjectProvider>
                    </UserProvider>
                </ThemeProvider>
            </QueryClientProvider>
            <Toaster />
        </div>
    );
}
