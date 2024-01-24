'use client';

import { apiClient } from '@/utils/api';
import { getLocalTimeString } from '@/utils/time';
import { ArrowLeftIcon, PlusCircledIcon, TrashIcon } from '@radix-ui/react-icons';
import { useQuery } from '@tanstack/react-query';
import { Loader2 } from 'lucide-react';
import { useParams, useRouter } from 'next/navigation';
import { Button } from '../ui/button';
import { Table, TableBody, TableCell, TableHeader, TableRow } from '../ui/table';
import DeleteProjectPrivateKeyDialog from './deleteProjectPrivateKeyDialog';
import NewProjectPrivateKeyDialog from './newProjectPrivateKeyDialog';

export default function() {
    const router = useRouter();
	const params = useParams<{ projectId: string }>();

	const projectId = parseInt(params.projectId);

    const query = useQuery({
        queryKey: [`projects/${projectId}/private-keys`], 
        queryFn: () => apiClient.projects.getProjectPrivateKeys(projectId)
    });

	const privateKeys = query?.data?.items || [];

    const onBackClick = () => router.replace('/')

    return (
        <div className='flex flex-col w-full justify-center items-center'>
            {!query.isFetching && !privateKeys.length &&
                <div className='flex items-center justify-center border-accent h-1/2 w-2/5 border-2 p-8 rounded-md bg-accent rounded-b-2xl'>
                    <div className='flex flex-col items-center'>
                        <p className='text-center pb-2'>Oops, you don't have any private keys for this project yet.</p>
                        <p className='text-center pb-2'>Don't be shy. Add one now.</p>
                        <NewProjectPrivateKeyDialog 
                            projectId={projectId}
                            trigger={(
                                <Button variant='ghost' className='hover:bg-accent px-2 size-12'>
                                    <PlusCircledIcon className='size-8 cursor-pointer' />
                                </Button>
                            )} 
                        />
                    </div>
                </div>
            }
            {privateKeys.length > 0 &&
                <div className='p-4 flex flex-col fade-in-0 w-full'>
                    <div className='flex items-center justify-center mt-4 h-10'>
                        <div className='flex-1'>
                            <Button variant='ghost' className='hover:bg-accent px-2 size-9' onClick={onBackClick}>
                                <ArrowLeftIcon className='size-8 cursor-pointer' />
                            </Button>
                        </div>
                        <div className='flex-1'>
                            <h1 className='text-center text-lg font-bold'>Private Keys</h1>
                        </div>
                        <NewProjectPrivateKeyDialog 
                            projectId={projectId}
                            trigger={(
                                <Button variant='ghost' className='hover:bg-accent px-2 size-9'>
                                    <PlusCircledIcon className='size-8 cursor-pointer' />
                                </Button>
                            )} 
                        />
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
                            {privateKeys.map((privateKey, i) => (
                                <TableRow key={privateKey.project_private_key_id} className={i % 2 == 0 ? 'bg-accent' : 'bg-white'}>
                                    <TableCell>{privateKey.project_private_key_id}</TableCell>
                                    <TableCell>{privateKey.name}</TableCell>
                                    <TableCell>{ getLocalTimeString(privateKey.created_date) }</TableCell>
                                    <TableCell className='flex flex-row justify-center'>   
										<DeleteProjectPrivateKeyDialog 
                                            projectId={projectId}
											projectPrivateKeyId={privateKey.project_private_key_id}
                                            name={privateKey.name} 
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
