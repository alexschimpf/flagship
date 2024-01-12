import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
	DropdownMenu,
	DropdownMenuContent,
	DropdownMenuItem,
	DropdownMenuSeparator,
	DropdownMenuTrigger,
  } from "@/components/ui/dropdown-menu"
import { PersonIcon, QuestionMarkCircledIcon, RocketIcon, MagnifyingGlassIcon, PlusCircledIcon } from '@radix-ui/react-icons'

export default function Home() {
	return (
		<main className='min-h-screen bg-background font-sans'>
			<div className='relative flex min-h-screen flex-col'>
				<header className='sticky top-0 z-50 w-full border-b'>
					<div className='container flex h-10 max-w-screen-2xl items-center'>
						<div className='flex flex-1 items-center'>
							<RocketIcon />
							<h1 className='font-bold text-lg pl-2 pr-6 cursor-pointer'>Flagship</h1>
							<nav>
								<Button variant='ghost' className='hover:bg-accent hover:rounded-none'>Projects</Button>
								<Button variant='ghost' className='hover:bg-accent hover:rounded-none'>Members</Button>
								<Button variant='ghost' className='hover:bg-accent hover:rounded-none'>Audit Logs</Button>
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
									<DropdownMenuItem className='cursor-pointer'>My Account</DropdownMenuItem>
									<DropdownMenuSeparator />
									<DropdownMenuItem className='cursor-pointer'>Logout</DropdownMenuItem>
								</DropdownMenuContent>
							</DropdownMenu>
						</div>
					</div>
				</header>
				<main className='flex-1 container items-center w-1/2 py-4'>
					<div className='flex flex-col items-center justify-center'>
						<div className='w-1/2 flex items-center justify-center pb-4'>
							<MagnifyingGlassIcon className='size-5 relative left-7 top-2.5 transform -translate-y-1/2' />
							<Input className='hover:border-slate-400 focus-visible:border-slate-400 pl-10' placeholder='Search for projects...' />
						</div>
						<div className='flex flex-col items-center rounded-sm border-accent size-5/6 border-2 p-4'>
							<p className='text-center pb-2'>Oops, you don't have any projects yet.</p>
							<p className='text-center pb-2'>Create one now!</p>
							<Button variant='ghost' className='hover:bg-accent px-2 size-12'>
								<PlusCircledIcon className='size-8 cursor-pointer' />
							</Button>
						</div>
					</div>
				</main>
				<footer className='sticky z-50 w-full border-t'>
					<div className='container flex h-10 max-w-screen-2xl items-center justify-center'>
						<div>
							<h1>&copy; 2024</h1>
						</div>
					</div>
				</footer>
			</div>
   	 	</main>
  )
}
