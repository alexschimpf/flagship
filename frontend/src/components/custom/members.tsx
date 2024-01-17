import SearchBar from '@/components/custom/searchBar'
import {
    Tooltip,
    TooltipContent,
    TooltipProvider,
    TooltipTrigger
} from '@/components/ui/tooltip'
import { apiClient, getErrorMessage, userRoles, userStatuses } from '@/utils/api'
import { getLocalTimeString } from '@/utils/time'
import { CheckCircledIcon, EnvelopeClosedIcon, ExclamationTriangleIcon, Pencil1Icon, PlusCircledIcon, TrashIcon } from '@radix-ui/react-icons'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Loader2 } from 'lucide-react'
import { Button } from '../ui/button'
import { Table, TableBody, TableCell, TableHeader, TableRow } from '../ui/table'
import { toast } from '../ui/use-toast'
import DeleteMemberDialog from './deleteMemberDialog'
import EditMemberDialog from './editMemberDialog'
import InviteMemberDialog from './inviteMemberDialog'

export default function() {
    const queryClient = useQueryClient(); 
    const query = useQuery({
        queryKey: ['users'], 
        queryFn: () => apiClient.users.getUsers()
    });
    const resetPasswordMutation = useMutation({
        mutationFn: (email: string) => {
            return apiClient.users.resetPassword({ email });
        },
        onError: (error) => {
            toast({
                variant: 'destructive',
                title: (
                    <div className='flex flex-row items-center'>
                        <ExclamationTriangleIcon />
                        <p className='text-white ml-2 font-bold'>Uh oh...</p>
                    </div>
                ),
                description: getErrorMessage(error),
            })
        },
        onSuccess: () => {
            queryClient.invalidateQueries({queryKey: ['users']});
            toast({
                variant: 'success',
                title: (
                    <div className='flex flex-row items-center'>
                        <CheckCircledIcon />
                        <p className='text-black ml-2 font-bold'>Success!</p>
                    </div>
                ),
                description: 'Reset password email was successfully sent.',
            })
        }
    });

    const users = query.data?.items || [];

    return (
        <div className='flex w-full justify-center'>
            {users.length > 0 &&
                <div className='p-4 flex flex-col fade-in-0 w-full'>
                    <div className='flex justify-end'>
                        <InviteMemberDialog trigger={(
                            <Button variant='ghost' className='hover:bg-accent px-2 size-9'>
                                <PlusCircledIcon className='size-8 cursor-pointer' />
                            </Button>
                        )} />
                    </div>
                    <div className='w-full flex justify-center mb-4'>
                        <SearchBar placeholder='Search for members...' className='w-1/2'/>
                    </div>
                    <Table>
                        <TableHeader>
                            <TableRow className='font-bold'>
                                <TableCell>ID</TableCell>
                                <TableCell>Email</TableCell>
                                <TableCell>Name</TableCell>
                                <TableCell>Role</TableCell>
                                <TableCell>Status</TableCell>
                                <TableCell>Created Date</TableCell>
                                <TableCell>Last Updated</TableCell>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {users.map((user, i) => (
                                <TableRow key={user.user_id} className={i % 2 == 0 ? 'bg-accent' : 'bg-white'}>
                                    <TableCell>{user.user_id}</TableCell>
                                    <TableCell>{user.email}</TableCell>
                                    <TableCell>{user.name}</TableCell>
                                    <TableCell>{userRoles[user.role]}</TableCell>
                                    <TableCell>{userStatuses[user.status]}</TableCell>
                                    <TableCell>{ getLocalTimeString(user.created_date) }</TableCell>
                                    <TableCell>{ getLocalTimeString(user.updated_date) }</TableCell>
                                    <TableCell className='flex flex-row justify-center'>   
                                        <EditMemberDialog 
                                            userId={user.user_id} 
                                            trigger={(
                                                <Pencil1Icon className='cursor-pointer mt-1 mr-4' />
                                            )} 
                                        />
                                        <TooltipProvider>
                                            <Tooltip>
                                                <TooltipTrigger>
                                                    <EnvelopeClosedIcon
                                                        className='cursor-pointer mr-4'
                                                        onClick={() => resetPasswordMutation.mutate(user.email)} 
                                                    />
                                                </TooltipTrigger>
                                                <TooltipContent>
                                                    <p>Send reset password email</p>
                                                </TooltipContent>
                                            </Tooltip>
                                        </TooltipProvider>
                                        <DeleteMemberDialog 
                                            userId={user.user_id} 
                                            email={user.email} 
                                            trigger={(
                                                <TrashIcon className='cursor-pointer mt-1' />
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
