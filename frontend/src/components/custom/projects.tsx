import NewProjectDialog from '@/components/custom/newProjectDialog'
import SearchBar from '@/components/custom/searchBar'
import {
    Tooltip,
    TooltipContent,
    TooltipTrigger
} from '@/components/ui/tooltip'
import { apiClient } from '@/utils/api'
import { getLocalTimeString } from '@/utils/time'
import { EyeOpenIcon, GearIcon, Pencil1Icon, PlusCircledIcon, TrashIcon } from '@radix-ui/react-icons'
import { TooltipProvider } from '@radix-ui/react-tooltip'
import { useQuery } from '@tanstack/react-query'
import { Loader2 } from 'lucide-react'
import { useRouter } from 'next/navigation'
import { Button } from '../ui/button'
import { Table, TableBody, TableCell, TableHeader, TableRow } from '../ui/table'
import DeleteProjectDialog from './deleteProjectDialog'
import EditProjectDialog from './editProjectDialog'

export default function() {
    const router = useRouter();
    const query = useQuery({
        queryKey: ['projects'], 
        queryFn: () => apiClient.projects.getProjects()
    });

    const onProjectPrivateKeysClick = (projectId: number) => router.replace(`/project/${projectId}/private-keys`);
    const onOpenProjectClick = (projectId: number) => router.replace(`/project/${projectId}`);

    const projects = query.data?.items || [];

    return (
        <div className='flex w-full justify-center'>
            {!query.isFetching && !projects.length &&
                <div className='flex items-center justify-center border-accent h-1/2 w-2/5border-2 p-8 rounded-md bg-accent rounded-b-2xl'>
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
                    <div className='flex justify-end'>
                        <NewProjectDialog trigger={(
                            <Button variant='ghost' className='hover:bg-accent px-2 size-9'>
                                <PlusCircledIcon className='size-8 cursor-pointer' />
                            </Button>
                        )} />
                    </div>
                    <div className='w-full flex justify-center mb-4'>
                        <SearchBar placeholder='Search for projects...' className='w-1/2'/>
                    </div>
                    <Table>
                        <TableHeader>
                            <TableRow className='font-bold hover:bg-white'>
                                <TableCell>ID</TableCell>
                                <TableCell>Name</TableCell>
                                <TableCell>Created Date</TableCell>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {projects.map((project, i) => (
                                <TableRow key={project.project_id} className={i % 2 == 0 ? 'bg-accent' : 'bg-white'}>
                                    <TableCell>{project.project_id}</TableCell>
                                    <TableCell>{project.name}</TableCell>
                                    <TableCell>{ getLocalTimeString(project.created_date) }</TableCell>
                                    <TableCell className='flex flex-row justify-center'>
                                        <TooltipProvider>
                                            <Tooltip>
                                                <TooltipTrigger>
                                                    <EyeOpenIcon className='cursor-pointer mr-4 hover:scale-125' onClick={() => onOpenProjectClick(project.project_id)} />
                                                </TooltipTrigger>
                                                <TooltipContent>
                                                    <p>Open project</p>
                                                </TooltipContent>
                                            </Tooltip>
                                        </TooltipProvider>       
                                        <EditProjectDialog 
                                            projectId={project.project_id} 
                                            initialName={project.name} 
                                            trigger={(
                                                <Pencil1Icon className='cursor-pointer mr-4 mt-1 hover:scale-125' />
                                            )} 
                                        />
                                        <TooltipProvider>
                                            <Tooltip>
                                                <TooltipTrigger>
                                                    <GearIcon className='cursor-pointer mr-4 hover:scale-125' onClick={() => onProjectPrivateKeysClick(project.project_id)} />
                                                </TooltipTrigger>
                                                <TooltipContent>
                                                    <p>Manage project private keys</p>
                                                </TooltipContent>
                                            </Tooltip>
                                        </TooltipProvider>
                                        <DeleteProjectDialog 
                                            projectId={project.project_id} 
                                            name={project.name} 
                                            trigger={(
                                                <TrashIcon className='cursor-pointer mt-1 hover:scale-125' />
                                            )} 
                                        />
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
