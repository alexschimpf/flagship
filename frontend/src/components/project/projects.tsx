import { Project } from '@/api';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger
} from '@/components/primitives/dropdown-menu';
import NewProjectDialog from '@/components/project/newProjectDialog';
import { UserContext } from '@/context/userContext';
import { apiClient } from '@/lib/api';
import { Permission, hasPermission } from '@/lib/permissions';
import { getLocalTimeString } from '@/lib/utils';
import { DropdownMenuSeparator } from '@radix-ui/react-dropdown-menu';
import { DotsHorizontalIcon, PlusCircledIcon } from '@radix-ui/react-icons';
import { useQuery } from '@tanstack/react-query';
import { Loader2 } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { useContext, useState } from 'react';
import { Button } from '../primitives/button';
import SearchBar from '../primitives/searchBar';
import {
    Table,
    TableBody,
    TableCell,
    TableHeader,
    TableRow
} from '../primitives/table';
import DeleteProjectDialog from './deleteProjectDialog';
import EditProjectDialog from './editProjectDialog';

export default function () {
    const currentUser = useContext(UserContext);
    const router = useRouter();
    const [searchText, setSearchText] = useState('');
    const query = useQuery({
        queryKey: ['projects'],
        queryFn: () => apiClient.projects.getProjects()
    });

    const onProjectPrivateKeysClick = (projectId: number) =>
        router.replace(`/project/${projectId}/private-keys`);
    const onFeatureFlagsClick = (projectId: number) =>
        router.replace(`/project/${projectId}/feature-flags`);
    const onContextFieldsClick = (projectId: number) =>
        router.replace(`/project/${projectId}/context-fields`);

    const projectMatchesSearchText = (project: Project) => {
        return !searchText || project.name.toLowerCase().includes(searchText.toLowerCase());
    };

    const projects = query.data?.items || [];
    const filteredProjects = projects.filter(projectMatchesSearchText);

    return (
        <div className='flex flex-col w-full justify-center'>
            <div className='flex items-center justify-center h-10 mt-4'>
                <div className='flex-1' />
                <div className='flex-1'>
                    <h1 className='text-center text-lg font-bold'>Projects</h1>
                </div>
                <div className='flex-1'>
                    {!query.isFetching &&
                        projects.length > 0 &&
                        hasPermission(
                            currentUser,
                            Permission.CREATE_PROJECT
                        ) && (
                            <NewProjectDialog
                                trigger={
                                    <Button
                                        variant='ghost'
                                        className='hover:bg-accent px-2 size-9'
                                    >
                                        <PlusCircledIcon className='size-8 cursor-pointer' />
                                    </Button>
                                }
                            />
                        )}
                </div>
            </div>
            {!query.isFetching && !projects.length && (
                <div className='flex items-center justify-center w-full'>
                    <div className='flex flex-col items-center border-accent h-1/2 w-2/5 border-2 p-8 rounded-md bg-accent rounded-b-2xl mt-4'>
                        <p className='text-center pb-2'>
                            Oops, you don't have any projects yet.
                        </p>
                        <p className='text-center pb-2'>
                            Don't be shy. Add one now.
                        </p>
                        {hasPermission(
                            currentUser,
                            Permission.CREATE_PROJECT
                        ) && (
                                <NewProjectDialog
                                    trigger={
                                        <Button
                                            variant='ghost'
                                            className='hover:bg-background px-2 size-12'
                                        >
                                            <PlusCircledIcon className='size-8 cursor-pointer' />
                                        </Button>
                                    }
                                />
                            )}
                    </div>
                </div>
            )}
            {projects.length > 0 && (
                <div className='p-4 flex flex-col fade-in-0 w-full'>
                    <div className='w-full flex justify-center mb-4'>
                        <SearchBar
                            placeholder='Search for projects..'
                            className='w-1/2'
                            onChange={(e) => setSearchText(e.currentTarget.value)}
                        />
                    </div>
                    <Table>
                        <TableHeader>
                            <TableRow className='font-bold hover:bg-background'>
                                <TableCell>ID</TableCell>
                                <TableCell>Name</TableCell>
                                <TableCell>Created Date</TableCell>
                                <TableCell>Actions</TableCell>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {filteredProjects.map((project, i) => (
                                <TableRow
                                    key={project.project_id}
                                    className={
                                        i % 2 == 0 ? 'bg-accent' : 'bg-muted/50'
                                    }
                                >
                                    <TableCell>{project.project_id}</TableCell>
                                    <TableCell>{project.name}</TableCell>
                                    <TableCell>
                                        {getLocalTimeString(
                                            project.created_date
                                        )}
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
                                                <DropdownMenuItem
                                                    className='hover:cursor-pointer'
                                                    onClick={() =>
                                                        onFeatureFlagsClick(
                                                            project.project_id
                                                        )
                                                    }
                                                >
                                                    Manage feature flags
                                                </DropdownMenuItem>
                                                {hasPermission(
                                                    currentUser,
                                                    Permission.UPDATE_CONTEXT_FIELD
                                                ) && (
                                                        <DropdownMenuItem
                                                            className='hover:cursor-pointer'
                                                            onClick={() =>
                                                                onContextFieldsClick(
                                                                    project.project_id
                                                                )
                                                            }
                                                        >
                                                            Manage context fields
                                                        </DropdownMenuItem>
                                                    )}
                                                {hasPermission(
                                                    currentUser,
                                                    Permission.READ_PROJECT_PRIVATE_KEYS
                                                ) && (
                                                        <DropdownMenuItem
                                                            className='hover:cursor-pointer'
                                                            onClick={() =>
                                                                onProjectPrivateKeysClick(
                                                                    project.project_id
                                                                )
                                                            }
                                                        >
                                                            Manage private keys
                                                        </DropdownMenuItem>
                                                    )}
                                                {(hasPermission(
                                                    currentUser,
                                                    Permission.UPDATE_PROJECT
                                                ) ||
                                                    hasPermission(
                                                        currentUser,
                                                        Permission.DELETE_PROJECT
                                                    )) && (
                                                        <DropdownMenuSeparator className='border-y h-0.5 my-2' />
                                                    )}
                                                {hasPermission(
                                                    currentUser,
                                                    Permission.UPDATE_PROJECT
                                                ) && (
                                                        <EditProjectDialog
                                                            projectId={
                                                                project.project_id
                                                            }
                                                            initialName={
                                                                project.name
                                                            }
                                                            trigger={
                                                                <DropdownMenuItem
                                                                    className='hover:cursor-pointer'
                                                                    onSelect={e =>
                                                                        e.preventDefault()
                                                                    }
                                                                >
                                                                    Edit project
                                                                </DropdownMenuItem>
                                                            }
                                                        />
                                                    )}
                                                {hasPermission(
                                                    currentUser,
                                                    Permission.DELETE_PROJECT
                                                ) && (
                                                        <DeleteProjectDialog
                                                            projectId={
                                                                project.project_id
                                                            }
                                                            name={project.name}
                                                            trigger={
                                                                <DropdownMenuItem
                                                                    className='hover:cursor-pointer'
                                                                    onSelect={e =>
                                                                        e.preventDefault()
                                                                    }
                                                                >
                                                                    Delete project
                                                                </DropdownMenuItem>
                                                            }
                                                        />
                                                    )}
                                            </DropdownMenuContent>
                                        </DropdownMenu>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                    {!filteredProjects.length &&
                        <div className='flex justify-center w-full m-4'>
                            <p>No results</p>
                        </div>
                    }
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
