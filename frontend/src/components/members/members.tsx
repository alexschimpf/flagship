'use client';

import { User } from '@/api';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger
} from '@/components/primitives/dropdown-menu';
import SearchBar from '@/components/primitives/searchBar';
import { UserContext } from '@/context/userContext';
import { apiClient, getErrorToast, getSuccessToast } from '@/lib/api';
import { userRoles, userStatuses } from '@/lib/constants';
import { Permission, hasPermission } from '@/lib/permissions';
import { getLocalTimeString } from '@/lib/utils';
import {
    ArrowLeftIcon,
    DotsHorizontalIcon,
    PlusCircledIcon
} from '@radix-ui/react-icons';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Loader2 } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { useContext, useState } from 'react';
import { Button } from '../primitives/button';
import {
    Table,
    TableBody,
    TableCell,
    TableHeader,
    TableRow
} from '../primitives/table';
import { toast } from '../primitives/use-toast';
import DeleteMemberDialog from './deleteMemberDialog';
import EditMemberDialog from './editMemberDialog';
import InviteMemberDialog from './inviteMemberDialog';

export default function Members() {
    const currentUser = useContext(UserContext);
    const router = useRouter();
    const queryClient = useQueryClient();
    const [searchText, setSearchText] = useState('');
    const query = useQuery({
        queryKey: ['users'],
        queryFn: () => apiClient.users.getUsers()
    });
    const resetPasswordMutation = useMutation({
        mutationFn: (email: string) => {
            return apiClient.users.resetPassword({ email });
        },
        onError: error => {
            toast(getErrorToast(error));
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['users'] });
            toast(
                getSuccessToast('Reset password email was successfully sent.')
            );
        }
    });

    const userMatchesSearchText = (user: User) => {
        return (
            !searchText ||
            user.email.toLowerCase().includes(searchText.toLowerCase()) ||
            user.name.toLowerCase().includes(searchText.toLowerCase())
        );
    };

    const users = query.data?.items || [];
    const filteredUsers = users.filter(userMatchesSearchText);

    const onBackClick = () => router.push('/');

    return (
        <div className='flex flex-col w-full justify-center'>
            <div className='flex items-center justify-center mt-4 h-10'>
                <div className='flex-1'>
                    <Button
                        variant='ghost'
                        className='hover:bg-accent px-2 size-9'
                        onClick={onBackClick}
                    >
                        <ArrowLeftIcon className='size-8 cursor-pointer' />
                    </Button>
                </div>
                <div className='flex-1'>
                    <h1 className='text-center text-lg font-bold'>Members</h1>
                </div>
                <div className='flex-1 h-full'>
                    {!query.isFetching && users.length > 0 && (
                        <InviteMemberDialog
                            trigger={
                                <PlusCircledIcon className='size-9 cursor-pointer hover:bg-accent px-2' />
                            }
                        />
                    )}
                </div>
            </div>
            {users.length > 0 && (
                <div className='p-4 flex flex-col fade-in-0 w-full'>
                    <div className='w-full flex justify-center mb-4'>
                        <SearchBar
                            placeholder='Search for members...'
                            className='w-1/2'
                            onChange={e => setSearchText(e.currentTarget.value)}
                        />
                    </div>
                    <Table>
                        <TableHeader>
                            <TableRow className='font-bold hover:bg-background'>
                                <TableCell>ID</TableCell>
                                <TableCell>Email</TableCell>
                                <TableCell>Name</TableCell>
                                <TableCell>Role</TableCell>
                                <TableCell>Status</TableCell>
                                <TableCell>Created Date</TableCell>
                                <TableCell>Last Updated</TableCell>
                                <TableCell>Actions</TableCell>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {filteredUsers.map((user, i) => (
                                <TableRow
                                    key={user.user_id}
                                    className={
                                        i % 2 == 0 ? 'bg-accent' : 'bg-muted/50'
                                    }
                                >
                                    <TableCell>{user.user_id}</TableCell>
                                    <TableCell className='max-w-[200px] break-words'>
                                        {user.email}
                                    </TableCell>
                                    <TableCell className='max-w-[200px] break-words'>
                                        {user.name}
                                    </TableCell>
                                    <TableCell>
                                        {userRoles[user.role]}
                                    </TableCell>
                                    <TableCell>
                                        {userStatuses[user.status]}
                                    </TableCell>
                                    <TableCell>
                                        {getLocalTimeString(user.created_date)}
                                    </TableCell>
                                    <TableCell>
                                        {getLocalTimeString(user.updated_date)}
                                    </TableCell>
                                    <TableCell className='flex flex-row justify-start items-center'>
                                        <DropdownMenu>
                                            <DropdownMenuTrigger asChild>
                                                <Button
                                                    variant='ghost'
                                                    className='size-8 p-0'
                                                >
                                                    <span className='sr-only'>
                                                        Open menu
                                                    </span>
                                                    <DotsHorizontalIcon className='hover:cursor-pointer hover:scale-125' />
                                                </Button>
                                            </DropdownMenuTrigger>
                                            <DropdownMenuContent>
                                                <EditMemberDialog
                                                    userId={user.user_id}
                                                    trigger={
                                                        <DropdownMenuItem
                                                            className='hover:cursor-pointer'
                                                            onSelect={e =>
                                                                e.preventDefault()
                                                            }
                                                        >
                                                            Edit member
                                                        </DropdownMenuItem>
                                                    }
                                                />
                                                {hasPermission(
                                                    currentUser,
                                                    Permission.DELETE_USER
                                                ) && (
                                                    <DeleteMemberDialog
                                                        userId={user.user_id}
                                                        email={user.email}
                                                        trigger={
                                                            <DropdownMenuItem
                                                                className='hover:cursor-pointer'
                                                                onSelect={e =>
                                                                    e.preventDefault()
                                                                }
                                                            >
                                                                Delete member
                                                            </DropdownMenuItem>
                                                        }
                                                    />
                                                )}
                                                {(hasPermission(
                                                    currentUser,
                                                    Permission.UPDATE_USER
                                                ) ||
                                                    currentUser?.user_id ===
                                                        user.user_id) && (
                                                    <DropdownMenuItem
                                                        className='hover:cursor-pointer'
                                                        onClick={() =>
                                                            resetPasswordMutation.mutate(
                                                                user.email
                                                            )
                                                        }
                                                    >
                                                        Resend set password
                                                        email
                                                    </DropdownMenuItem>
                                                )}
                                            </DropdownMenuContent>
                                        </DropdownMenu>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                    {!filteredUsers.length && (
                        <div className='flex justify-center w-full m-4'>
                            <p>No results</p>
                        </div>
                    )}
                </div>
            )}
            {query.isFetching && (
                <div className='absolute top-[calc(50%-41px)] left-1/2'>
                    <Loader2 className='animate-spin' size={48} />
                </div>
            )}
        </div>
    );
}
