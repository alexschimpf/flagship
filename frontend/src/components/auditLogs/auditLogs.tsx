'use client';

import { SystemAuditLogs } from '@/api';
import { apiClient } from '@/lib/api';
import { getLocalTimeString } from '@/lib/utils';
import { ArrowLeftIcon } from '@radix-ui/react-icons';
import { useInfiniteQuery } from '@tanstack/react-query';
import { Loader2 } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { Button } from '../primitives/button';
import {
    Table,
    TableBody,
    TableCell,
    TableHeader,
    TableRow
} from '../primitives/table';

export default function AuditLogs() {
    const router = useRouter();
    const query = useInfiniteQuery<SystemAuditLogs, Error>({
        queryKey: [`audit-logs`],
        queryFn: ({ pageParam }) =>
            apiClient.admin.getAuditLogs(pageParam as number),
        initialPageParam: 0,
        getNextPageParam: (lastPage: any, pages: any, lastPageParam: any) => {
            if (!lastPage.items.length) {
                return undefined;
            }
            return lastPageParam + 1;
        }
    });

    const pages = query?.data?.pages || [];

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
                    <h1 className='text-center text-lg font-bold'>
                        Audit Logs
                    </h1>
                </div>
                <div className='flex-1'></div>
            </div>
            {pages.length > 0 && (
                <div className='p-4 flex flex-col fade-in-0 w-full'>
                    <Table>
                        <TableHeader>
                            <TableRow className='font-bold hover:bg-background'>
                                <TableCell>Actor</TableCell>
                                <TableCell>Event Type</TableCell>
                                <TableCell>Details</TableCell>
                                <TableCell>Event Time</TableCell>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {pages.map(page =>
                                page.items.map((auditLog, i) => (
                                    <TableRow
                                        key={i}
                                        className={
                                            i % 2 == 0
                                                ? 'bg-accent'
                                                : 'bg-muted/50'
                                        }
                                    >
                                        <TableCell className='max-w-[200px] break-words'>
                                            {auditLog.actor}
                                        </TableCell>
                                        <TableCell>
                                            {auditLog.event_type}
                                        </TableCell>
                                        <TableCell className='max-w-[400px] break-words'>
                                            {auditLog.details}
                                        </TableCell>
                                        <TableCell>
                                            {getLocalTimeString(
                                                auditLog.event_time
                                            )}
                                        </TableCell>
                                    </TableRow>
                                ))
                            )}
                        </TableBody>
                    </Table>
                    {query.hasNextPage && (
                        <div className='flex justify-center m-4'>
                            <Button
                                onClick={() => query.fetchNextPage()}
                                disabled={
                                    !query.hasNextPage ||
                                    query.isFetchingNextPage
                                }
                            >
                                {query.isFetchingNextPage
                                    ? 'Loading more...'
                                    : 'Load more'}
                            </Button>
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
