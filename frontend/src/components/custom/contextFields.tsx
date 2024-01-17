import NewProjectDialog from '@/components/custom/newProjectDialog'
import SearchBar from '@/components/custom/searchBar'
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger
} from "@/components/ui/dropdown-menu"
import { apiClient, contextFieldValueTypes } from '@/utils/api'
import { getLocalTimeString } from '@/utils/time'
import { ArrowLeftIcon, DotsHorizontalIcon, PlusCircledIcon } from '@radix-ui/react-icons'
import { useQuery } from '@tanstack/react-query'
import { Loader2 } from 'lucide-react'
import { useParams, useRouter } from 'next/navigation'
import { Button } from '../ui/button'
import { Table, TableBody, TableCell, TableHeader, TableRow } from '../ui/table'

export default function() {
    const params = useParams<{ projectId: string }>();
    const projectId = parseInt(params.projectId);

    const router = useRouter();
    const query = useQuery({
        queryKey: [`projects/${projectId}/context-fields`], 
        queryFn: () => apiClient.contextFields.getContextFields(projectId)
    });

    const contextFields = query.data?.items || [];

    const onBackClick = () => router.replace('/');

    return (
        <div className='flex flex-col w-full justify-center'>
            <div className='flex items-center justify-center mt-4 h-10'>
                <div className='flex-1'>
                    <Button variant='ghost' className='hover:bg-accent px-2 size-9' onClick={onBackClick}>
                        <ArrowLeftIcon className='size-8 cursor-pointer' />
                    </Button>
                </div>
                <div className='flex-1'>
                    <h1 className='text-center text-lg font-bold'>Context Fields</h1>
                </div>
                <div className='flex-1'>
                    {!query.isFetching && contextFields.length > 0 &&
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
            {!query.isFetching && !contextFields.length &&
                <div className='flex items-center justify-center w-full'>
                <div className='flex flex-col items-center border-accent h-1/2 w-2/5 border-2 p-8 rounded-md bg-accent rounded-b-2xl mt-4'>
                        <p className='text-center pb-2'>Oops, you don't have any context fields for this project yet.</p>
                        <p className='text-center pb-2'>Don't be shy. Add one now.</p>
                        <NewProjectDialog trigger={(
                            <Button variant='ghost' className='hover:bg-accent px-2 size-12'>
                                <PlusCircledIcon className='size-8 cursor-pointer' />
                            </Button>
                        )} />
                    </div>
                </div>
            }
            {contextFields.length > 0 &&
                <div className='p-4 flex flex-col fade-in-0 w-full'>
                    <div className='w-full flex justify-center mb-4'>
                        <SearchBar placeholder='Search for context fields...' className='w-1/2'/>
                    </div>
                    <Table>
                        <TableHeader>
                            <TableRow className='font-bold hover:bg-white'>
                                <TableCell>ID</TableCell>
                                <TableCell>Name</TableCell>
                                <TableCell>Field Key</TableCell>
                                <TableCell>Value Type</TableCell>
                                <TableCell>Description</TableCell>
                                <TableCell>Created Date</TableCell>
                                <TableCell>Last Updated</TableCell>
                                <TableCell>Actions</TableCell>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {contextFields.map((contextField, i) => (
                                <TableRow key={contextField.context_field_id} className={i % 2 == 0 ? 'bg-accent' : 'bg-white'}>
                                    <TableCell>{contextField.context_field_id}</TableCell>
                                    <TableCell>{contextField.name}</TableCell>
                                    <TableCell>{contextField.field_key}</TableCell>
                                    <TableCell>{contextFieldValueTypes[contextField.value_type]}</TableCell>
                                    <TableCell>{contextField.description}</TableCell>
                                    <TableCell>{ getLocalTimeString(contextField.created_date) }</TableCell>
                                    <TableCell>{ getLocalTimeString(contextField.updated_date) }</TableCell>
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
                                                >
                                                    Edit context field
                                                </DropdownMenuItem>
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
