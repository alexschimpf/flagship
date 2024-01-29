'use client';

import { ThemeProvider } from "next-themes";

import Login from '@/components/login/login';

export default function () {
    const theme = localStorage.getItem('theme') || 'dark';
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
