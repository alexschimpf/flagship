'use client';

import { ThemeProvider } from "next-themes";

import Login from '@/components/login/login';

export default function LoginPage() {
    let theme = 'dark';
    if (typeof window !== 'undefined') {
        theme = localStorage.getItem('theme') || 'dark';
    }
    return (
        <ThemeProvider
            attribute='class'
            defaultTheme={theme}
            enableSystem
        >
            <Login />
        </ThemeProvider>
    );
}
