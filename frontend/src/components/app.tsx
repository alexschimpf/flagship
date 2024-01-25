'use client';

import { ProjectProvider } from '@/context/projectProvider';
import { queryClient } from '@/lib/api';
import { QueryClientProvider } from '@tanstack/react-query';
import { UserProvider } from '../context/userProvider';
import Footer from './footer';
import Header from './header';
import { Toaster } from './primitives/toaster';

export default function ({ children }: any) {
    return (
        <div className='flex-1 flex flex-col container items-center w-3/4'>
            <QueryClientProvider client={queryClient}>
                <UserProvider>
                    <ProjectProvider>
                        <Header />
                        <div className='flex-1 w-full'>
                            {children}
                        </div>
                        <Footer />
                    </ProjectProvider>
                </UserProvider>
            </QueryClientProvider>
            <Toaster />
        </div>
    );
}
