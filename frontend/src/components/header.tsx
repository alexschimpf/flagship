'use client';

import { API_BASE_URL } from '@/app/config';
import { Button } from '@/components/primitives/button';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuSeparator,
    DropdownMenuTrigger
} from '@/components/primitives/dropdown-menu';
import { ProjectContext } from '@/context/projectContext';
import { UserContext } from '@/context/userContext';
import { UserProvider } from '@/context/userProvider';
import { Permission, hasPermission } from '@/lib/permissions';
import {
    PersonIcon,
    QuestionMarkCircledIcon,
    RocketIcon
} from '@radix-ui/react-icons';
import { Moon } from 'lucide-react';
import { useTheme } from 'next-themes';
import { usePathname, useRouter } from 'next/navigation';
import { useContext } from 'react';

export default function Header() {
    return (
        <UserProvider>
            <Header_ />
        </UserProvider>
    );
}

const Header_ = () => {
    const { theme, setTheme } = useTheme();
    const currentUser = useContext(UserContext);
    const currentProject = useContext(ProjectContext);
    const router = useRouter();
    const pathName = usePathname();

    const onLogoutClick = () => {
        sessionStorage.clear();
        router.replace(`${API_BASE_URL}/auth/logout`);
    };

    const onToggleLightDarkModeClick = () => {
        const newTheme = theme === 'dark' ? 'light' : 'dark';
        localStorage.setItem('theme', newTheme);
        setTheme(newTheme);
    };

    return (
        <header className='sticky top-0 z-50 w-full bg-accent rounded-b-sm'>
            <div className='container flex h-10 max-w-screen-2xl items-center'>
                <div className='flex flex-1 items-center flex-shrink'>
                    <Button
                        variant='ghost'
                        className='focus-visible:bg-white p-0 mr-6'
                        onClick={() => {
                            window.location.replace('/');
                        }}
                    >
                        <RocketIcon className='size-5' />
                        <h1 className='font-bold text-lg pl-2 cursor-pointer'>
                            Flagship
                        </h1>
                    </Button>
                    <nav>
                        <Button
                            variant='ghost'
                            className={`h-full p-3 hover:bg-background rounded-none ${pathName === '/' ? 'bg-background' : ''}`}
                            onClick={() => router.push('/')}
                        >
                            Projects
                        </Button>
                        {hasPermission(currentUser, Permission.READ_USERS) && (
                            <Button
                                variant='ghost'
                                className={`h-full p-3 hover:bg-background rounded-none ${pathName === '/members' ? 'bg-background' : ''}`}
                                onClick={() => router.push('/members')}
                            >
                                Members
                            </Button>
                        )}
                        {hasPermission(
                            currentUser,
                            Permission.READ_SYSTEM_AUDIT_LOGS
                        ) && (
                            <Button
                                variant='ghost'
                                className={`h-full p-3 hover:bg-background rounded-none ${pathName === '/audit-logs' ? 'bg-background' : ''}`}
                                onClick={() => router.push('/audit-logs')}
                            >
                                Audit Logs
                            </Button>
                        )}
                    </nav>
                </div>
                {currentProject?.name?.length && (
                    <div className='flex justify-end items-center h-full mr-6 px-4 bg-background'>
                        <p className='font-bold text-sm max-w-[300px] overflow-hidden text-ellipsis'>
                            {currentProject?.name}
                        </p>
                    </div>
                )}
                <div className='flex justify-end items-center cursor-pointer'>
                    <a
                        href='/help'
                        className='flex justify-center items-center hover:bg-background hover:rounded-none px-2 size-10'
                    >
                        <QuestionMarkCircledIcon className='size-5' />
                    </a>
                    <div
                        className='flex justify-center items-center hover:bg-background hover:rounded-none px-2 size-10'
                        title='Toggle dark mode'
                        onClick={onToggleLightDarkModeClick}
                    >
                        <Moon className='size-5' />
                    </div>
                    <DropdownMenu>
                        <DropdownMenuTrigger className='focus-visible:outline-none hover:bg-background size-10 flex items-center justify-center'>
                            <PersonIcon className='size-5' />
                        </DropdownMenuTrigger>
                        <DropdownMenuContent>
                            <DropdownMenuItem className='cursor-pointer'>
                                <a className='w-full' href='/account'>
                                    My Account
                                </a>
                            </DropdownMenuItem>
                            <DropdownMenuSeparator />
                            <DropdownMenuItem className='cursor-pointer'>
                                <a className='w-full' onClick={onLogoutClick}>
                                    Log out
                                </a>
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>
                </div>
            </div>
        </header>
    );
};
