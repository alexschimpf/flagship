import NewProjectDialog from '@/components/custom/newProjectDialog'
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger
} from "@/components/ui/dropdown-menu"
import { apiClient } from '@/utils/api'
import { getLocalTimeString } from '@/utils/time'
import { DropdownMenuSeparator } from '@radix-ui/react-dropdown-menu'
import { DotsHorizontalIcon, PlusCircledIcon } from '@radix-ui/react-icons'
import { useQuery } from '@tanstack/react-query'
import { Loader2 } from 'lucide-react'
import { useRouter } from 'next/navigation'
import { Button } from '../ui/button'
import { Table, TableBody, TableCell, TableHeader, TableRow } from '../ui/table'
import DeleteProjectDialog from './deleteProjectDialog'
import EditProjectDialog from './editProjectDialog'
import SearchBar from './searchBar'

export default function() {
    const router = useRouter();
    const query = useQuery({
        queryKey: ['projects'], 
        queryFn: () => apiClient.projects.getProjects()
    });

    const onProjectPrivateKeysClick = (projectId: number) => router.replace(`/project/${projectId}/private-keys`);
    const onFeatureFlagsClick = (projectId: number) => router.replace(`/project/${projectId}/feature-flags`);
    const onContextFieldsClick = (projectId: number) => router.replace(`/project/${projectId}/context-fields`);

    const projects = query.data?.items || [];

    return (
        <div className='flex flex-col w-full justify-center'>
            <div className='flex items-center justify-center h-10 mt-4'>
                <div className='flex-1' />
                <div className='flex-1'>
                    <h1 className='text-center text-lg font-bold'>Projects</h1>
                </div>
                <div className='flex-1'>
                    {!query.isFetching && projects.length > 0 &&
                    <NewProjectDialog 
                        trigger={(
                            <Button variant='ghost' className='hover:bg-accent px-2 size-9'>
                                <PlusCircledIcon className='size-8 cursor-pointer' />
                            </Button>
                        )} 
                    />
                    }
                </div>
            </div>
            {!query.isFetching && !projects.length &&
                <div className='flex items-center justify-center border-accent h-1/2 w-2/5border-2 p-8 rounded-md bg-accent rounded-b-2xl mt-4'>
                    <div className='flex flex-col items-center'>
                        <p className='text-center pb-2'>Oops, you don't have any projects yet.</p>
                        <p className='text-center pb-2'>Don't be shy. Add one now.</p>
                        <NewProjectDialog trigger={(
                            <Button variant='ghost' className='hover:bg-accent px-2 size-12'>
                                <PlusCircledIcon className='size-8 cursor-pointer' />
                            </Button>
                        )} />
                    </div>
                </div>
            }
            {projects.length > 0 &&
                <div className='p-4 flex flex-col fade-in-0 w-full'>
                    <div className='w-full flex justify-center mb-4'>
                        <SearchBar placeholder='Search for projects..' className='w-1/2'/>
                    </div>
                    <Table>
                        <TableHeader>
                            <TableRow className='font-bold hover:bg-white'>
                                <TableCell>ID</TableCell>
                                <TableCell>Name</TableCell>
                                <TableCell>Created Date</TableCell>
                                <TableCell>Actions</TableCell>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {projects.map((project, i) => (
                                <TableRow key={project.project_id} className={i % 2 == 0 ? 'bg-accent' : 'bg-white'}>
                                    <TableCell>{project.project_id}</TableCell>
                                    <TableCell>{project.name}</TableCell>
                                    <TableCell>{ getLocalTimeString(project.created_date) }</TableCell>
                                    <TableCell className='flex flex-row justify-start items-center'>
                                        <DropdownMenu>
                                            <DropdownMenuTrigger asChild>
                                                <Button variant="ghost" className="size-8 p-0">
                                                    <span className="sr-only">Open menu</span>
                                                    <DotsHorizontalIcon className='hover:cursor-pointer hover:scale-125' />
                                                </Button>
                                            </DropdownMenuTrigger>
                                            <DropdownMenuContent>
                                                <DropdownMenuItem 
                                                    className='hover:cursor-pointer'
                                                    onClick={() => onFeatureFlagsClick(project.project_id)}
                                                >
                                                    Manage feature flags
                                                </DropdownMenuItem>
                                                <DropdownMenuItem
                                                    className='hover:cursor-pointer'
                                                    onClick={() => onContextFieldsClick(project.project_id)}
                                                >
                                                    Manage context fields
                                                </DropdownMenuItem>
                                                <DropdownMenuItem
                                                    className='hover:cursor-pointer'
                                                    onClick={() => onProjectPrivateKeysClick(project.project_id)}
                                                >
                                                    Manage private keys
                                                </DropdownMenuItem>
                                                <DropdownMenuSeparator
                                                    className='border-y h-0.5 my-2' 
                                                />      
                                                <EditProjectDialog 
                                                    projectId={project.project_id} 
                                                    initialName={project.name} 
                                                    trigger={(
                                                        <DropdownMenuItem className='hover:cursor-pointer' onSelect={(e) => e.preventDefault()}>
                                                            Edit project
                                                        </DropdownMenuItem>
                                                    )} 
                                                />    
                                                <DeleteProjectDialog 
                                                    projectId={project.project_id} 
                                                    name={project.name} 
                                                    trigger={(
                                                        <DropdownMenuItem className='hover:cursor-pointer' onSelect={(e) => e.preventDefault()}>
                                                            Delete project
                                                        </DropdownMenuItem>
                                                    )} 
                                                />  
                                            </DropdownMenuContent>
                                        </DropdownMenu>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </div>
            }
            {query.isFetching &&
                <div className='absolute top-1/2 left-1/2'>
                    <Loader2 className='animate-spin' size={48} />
                </div>
            }
        </div>
    )
}
