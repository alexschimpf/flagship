'use client';

import { Button } from '@/components/ui/button'
import {
	DropdownMenu,
	DropdownMenuContent,
	DropdownMenuItem,
	DropdownMenuSeparator,
	DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { PersonIcon, QuestionMarkCircledIcon, RocketIcon } from '@radix-ui/react-icons'
import { useGlobalStore, Page } from '@/stores'


export default function() {
    const globalStore = useGlobalStore()

    return (
        <header className='sticky top-0 z-50 w-full border-b bg-white'>
            <div className='container flex h-10 max-w-screen-2xl items-center'>
                <div className='flex flex-1 items-center'>
                    <Button 
                        variant='ghost' 
                        className='focus-visible:bg-white hover:bg-white p-0 mr-6' 
                        onClick={() => { window.location.replace('http://localhost:3000') }}
                    >
                        <RocketIcon />
                        <h1 className='font-bold text-lg pl-2 cursor-pointer'>Flagship</h1>
                    </Button>
                    <nav>
                        <Button 
                            variant='ghost' 
                            className={`hover:bg-accent rounded-none ${globalStore.currPage == Page.Projects ? 'bg-accent' : ''}`} 
                            onClick={() => globalStore.setCurrPage(Page.Projects)}
                        >
                            Projects
                        </Button>
                        <Button 
                            variant='ghost'
                            className={`hover:bg-accent rounded-none ${globalStore.currPage == Page.Members ? 'bg-accent' : ''}`}
                            onClick={() => globalStore.setCurrPage(Page.Members)}
                        >
                            Members
                        </Button>
                        <Button 
                            variant='ghost'
                            className={`hover:bg-accent rounded-none ${globalStore.currPage == Page.AuditLogs ? 'bg-accent' : ''}`}
                            onClick={() => globalStore.setCurrPage(Page.AuditLogs)}
                        >
                            Audit Logs
                        </Button>
                    </nav>
                </div>
                <div className='flex items-center cursor-pointer'>
                    <Button variant='ghost' className='hover:bg-accent hover:rounded-none px-2 size-10'>
                        <QuestionMarkCircledIcon className='size-5' />
                    </Button>
                    <DropdownMenu>
                        <DropdownMenuTrigger className='focus-visible:outline-none hover:bg-accent size-10 flex items-center justify-center'>
                            <PersonIcon className='size-5' />
                        </DropdownMenuTrigger>
                        <DropdownMenuContent>
                            <DropdownMenuItem 
                                className='cursor-pointer'
                            >
                                My Account
                            </DropdownMenuItem>
                            <DropdownMenuSeparator />
                            <DropdownMenuItem
                                className='cursor-pointer'
                            >
                                <a href='//localhost:8000/auth/logout'>Logout</a>
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>
                </div>
            </div>
        </header>
    )
}