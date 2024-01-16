import NewProjectDialog from '@/components/custom/newProjectDialog'
import SearchBar from '@/components/custom/searchBar'
import { apiClient } from '@/utils/api'
import { EyeOpenIcon, Pencil1Icon, PlusCircledIcon, TrashIcon } from '@radix-ui/react-icons'
import { useQuery } from '@tanstack/react-query'
import { Loader2 } from 'lucide-react'
import { Button } from '../ui/button'
import { Table, TableBody, TableCell, TableHeader, TableRow } from '../ui/table'
import DeleteProjectDialog from './deleteProjectDialog'
import EditProjectDialog from './editProjectDialog'

export default function() {
    const query = useQuery({
        queryKey: ['projects'], 
        queryFn: () => apiClient.projects.getProjects()
    });

    const projects = query.data?.items || [];

    return (
        <div className='flex flex-1 w-full justify-center'>
            {!query.isFetching && !projects.length &&
                <div className='flex items-center justify-center border-accent h-1/2 w-1/2 border-2 p-8 rounded-md bg-accent'>
                    <div className='flex flex-col items-center'>
                        <p className='text-center pb-2'>Oops, you don't have any projects yet.</p>
                        <p className='text-center pb-2'>Create one now!</p>
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
                        <SearchBar className='w-1/2'/>
                    </div>
                    <Table>
                        <TableHeader>
                            <TableRow className='font-bold'>
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
                                    <TableCell>{project.created_date}</TableCell>
                                    <TableCell className='flex flex-row justify-center'>
                                        <EyeOpenIcon className='cursor-pointer mr-4' />                               
                                        <EditProjectDialog 
                                            projectId={project.project_id} 
                                            initialName={project.name} 
                                            trigger={(
                                                <Pencil1Icon className='cursor-pointer mr-4' />
                                            )} 
                                        />
                                        <DeleteProjectDialog 
                                            projectId={project.project_id} 
                                            name={project.name} 
                                            trigger={(
                                                <TrashIcon className='cursor-pointer' />
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
