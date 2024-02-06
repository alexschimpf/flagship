'use client';

import { ThemeProvider } from "next-themes";

import ForgotPassword from "@/components/login/forgotPassword";

export default function ForgotPasswordPage() {
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
            <ForgotPassword />
        </ThemeProvider>
    );
}
