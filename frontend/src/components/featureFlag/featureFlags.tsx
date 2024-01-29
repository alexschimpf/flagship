import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger
} from '@/components/primitives/dropdown-menu';
import SearchBar from '@/components/primitives/searchBar';
import { UserContext } from '@/context/userContext';
import { apiClient } from '@/lib/api';
import { Permission, hasPermission } from '@/lib/permissions';
import { cn, getLocalTimeString } from '@/lib/utils';
import {
    ArrowLeftIcon,
    DotsHorizontalIcon,
    PlusCircledIcon
} from '@radix-ui/react-icons';
import { useQuery } from '@tanstack/react-query';
import { Loader2 } from 'lucide-react';
import { useParams, useRouter } from 'next/navigation';
import { useContext, useState } from 'react';
import { Button } from '../primitives/button';
import { Switch } from '../primitives/switch';
import {
    Table,
    TableBody,
    TableCell,
    TableHeader,
    TableRow
} from '../primitives/table';
import DeleteFeatureFlagDialog from './deleteFeatureFlagDialog';
import FlipFeatureFlagDialog from './flipFeatureFlagDialog';

export default function () {
    const params = useParams<{ projectId: string; }>();
    const projectId = parseInt(params.projectId);
    const currentUser = useContext(UserContext);
    const [searchText, setSearchText] = useState('');
    const router = useRouter();
    const query = useQuery({
        queryKey: [`projects/${projectId}/feature-flags`],
        queryFn: () => apiClient.featureFlags.getFeatureFlags(projectId)
    });

    const featureFlagMatchesSearchText = (featureFlag: FeatureFlag) => {
        return !searchText || featureFlag.name.toLowerCase().includes(searchText.toLowerCase());
    };

    const featureFlags = query.data?.items || [];
    const filteredFeatureFlags = featureFlags.filter(featureFlagMatchesSearchText);

    const onBackClick = () => router.push('/');
    const onNewClick = () =>
        router.push(`/project/${projectId}/feature-flags/new`);
    const onEditClick = (featureFlagId: number) =>
        router.push(`/project/${projectId}/feature-flag/${featureFlagId}`);
    const onAuditLogsClick = (featureFlagId: number) =>
        router.push(
            `/project/${projectId}/feature-flag/${featureFlagId}/audit-logs`
        );

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
                    <h1 className='text-center text-lg font-bold'>
                        Feature Flags
                    </h1>
                </div>
                <div className='flex-1 h-full'>
                    {!query.isFetching &&
                        featureFlags.length > 0 &&
                        hasPermission(
                            currentUser,
                            Permission.CREATE_FEATURE_FLAG
                        ) && (
                            <PlusCircledIcon className='size-9 cursor-pointer hover:bg-accent px-2' onClick={onNewClick} />
                        )}
                </div>
            </div>
            {!query.isFetching && !featureFlags.length && (
                <div className='flex items-center justify-center w-full'>
                    <div className='flex flex-col items-center border-accent h-1/2 w-2/5 border-2 p-8 rounded-md bg-accent rounded-b-2xl mt-4'>
                        <p className='text-center pb-2'>
                            Oops, you don't have any feature flags for this
                            project yet.
                        </p>
                        <p className='text-center pb-2'>
                            Don't be shy. Add one now.
                        </p>
                        {hasPermission(
                            currentUser,
                            Permission.CREATE_FEATURE_FLAG
                        ) && (
                                <PlusCircledIcon className='size-9 cursor-pointer hover:bg-accent px-2' onClick={onNewClick} />
                            )}
                    </div>
                </div>
            )}
            {featureFlags.length > 0 && (
                <div className='p-4 flex flex-col fade-in-0 w-full'>
                    <div className='w-full flex justify-center mb-4'>
                        <SearchBar
                            placeholder='Search for feature flags...'
                            className='w-1/2'
                            onChange={e => setSearchText(e.currentTarget.value)}
                        />
                    </div>
                    <Table className='w-full'>
                        <TableHeader>
                            <TableRow className='font-bold hover:bg-background'>
                                <TableCell>ID</TableCell>
                                <TableCell>Name</TableCell>
                                <TableCell>Description</TableCell>
                                <TableCell>Created Date</TableCell>
                                <TableCell>Last Updated</TableCell>
                                <TableCell>Enabled</TableCell>
                                <TableCell>Actions</TableCell>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {filteredFeatureFlags.map((featureFlag, i) => (
                                <TableRow
                                    key={featureFlag.feature_flag_id}
                                    className={
                                        i % 2 == 0 ? 'bg-accent' : 'bg-muted/50'
                                    }
                                >
                                    <TableCell>
                                        {featureFlag.feature_flag_id}
                                    </TableCell>
                                    <TableCell className='max-w-[300px] break-words'>{featureFlag.name}</TableCell>
                                    <TableCell className='max-w-[300px] break-words'>
                                        {featureFlag.description}
                                    </TableCell>
                                    <TableCell>
                                        {getLocalTimeString(
                                            featureFlag.created_date
                                        )}
                                    </TableCell>
                                    <TableCell>
                                        {getLocalTimeString(
                                            featureFlag.updated_date
                                        )}
                                    </TableCell>
                                    <TableCell>
                                        <FlipFeatureFlagDialog
                                            name={featureFlag.name}
                                            featureFlagId={
                                                featureFlag.feature_flag_id
                                            }
                                            projectId={projectId}
                                            enabled={!featureFlag.enabled}
                                            trigger={
                                                <div>
                                                    <Switch
                                                        className={cn(
                                                            'scale-75',
                                                            !hasPermission(
                                                                currentUser,
                                                                Permission.UPDATE_FEATURE_FLAG
                                                            )
                                                                ? 'cursor-not-allowed'
                                                                : ''
                                                        )}
                                                        checked={
                                                            featureFlag.enabled
                                                        }
                                                        disabled={
                                                            !hasPermission(
                                                                currentUser,
                                                                Permission.UPDATE_FEATURE_FLAG
                                                            )
                                                        }
                                                    />
                                                </div>
                                            }
                                        />
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
                                                        onEditClick(
                                                            featureFlag.feature_flag_id
                                                        )
                                                    }
                                                >
                                                    Edit feature flag
                                                </DropdownMenuItem>
                                                {hasPermission(
                                                    currentUser,
                                                    Permission.DELETE_FEATURE_FLAG
                                                ) && (
                                                        <DeleteFeatureFlagDialog
                                                            projectId={projectId}
                                                            featureFlagId={
                                                                featureFlag.feature_flag_id
                                                            }
                                                            name={featureFlag.name}
                                                            trigger={
                                                                <DropdownMenuItem
                                                                    className='hover:cursor-pointer'
                                                                    onSelect={e =>
                                                                        e.preventDefault()
                                                                    }
                                                                >
                                                                    Delete feature
                                                                    flag
                                                                </DropdownMenuItem>
                                                            }
                                                        />
                                                    )}
                                                {hasPermission(
                                                    currentUser,
                                                    Permission.READ_FEATURE_FLAG_AUDIT_LOGS
                                                ) && (
                                                        <DropdownMenuItem
                                                            className='hover:cursor-pointer'
                                                            onClick={() =>
                                                                onAuditLogsClick(
                                                                    featureFlag.feature_flag_id
                                                                )
                                                            }
                                                        >
                                                            View audit logs
                                                        </DropdownMenuItem>
                                                    )}
                                            </DropdownMenuContent>
                                        </DropdownMenu>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                    {!filteredFeatureFlags.length &&
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
