'use client';

import SetPassword from "@/components/login/setPassword";
import { ThemeProvider } from "next-themes";


export default function () {
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
            <SetPassword />
        </ThemeProvider>
    );
}
