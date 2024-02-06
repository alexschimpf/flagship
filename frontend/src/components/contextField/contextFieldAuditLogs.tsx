'use client';

import { ContextFieldAuditLogs } from '@/api';
import { apiClient } from '@/lib/api';
import { getLocalTimeString } from '@/lib/utils';
import { ArrowLeftIcon } from '@radix-ui/react-icons';
import { useInfiniteQuery } from '@tanstack/react-query';
import { Loader2 } from 'lucide-react';
import { useParams, useRouter } from 'next/navigation';
import { Button } from '../primitives/button';
import {
    Table,
    TableBody,
    TableCell,
    TableHeader,
    TableRow
} from '../primitives/table';

export default function ContextFieldAuditLogs() {
    const params = useParams<{ projectId: string; contextFieldId: string; }>();
    const router = useRouter();

    const contextFieldId = parseInt(params.contextFieldId);
    const projectId = parseInt(params.projectId);

    const query = useInfiniteQuery<ContextFieldAuditLogs, Error>({
        queryKey: [`/projects/${projectId}/context-fields/${contextFieldId}/audit-logs`],
        queryFn: ({ pageParam }) => apiClient.contextFields.getContextFieldAuditLogs(contextFieldId, projectId, pageParam as number),
        initialPageParam: 0,
        getNextPageParam: (lastPage: any, pages: any, lastPageParam: any) => {
            if (!lastPage.items.length) {
                return undefined;
            }
            return lastPageParam + 1;
        }
    });

    const pages = query?.data?.pages || [];

    const onBackClick = () =>
        router.push(`/project/${projectId}/context-fields`);

    const getAuditLogRows = () => {
        let rowNum = 0;
        const rows = [];
        for (const page of pages) {
            for (const auditLog of page.items) {
                for (const change of auditLog?.changes || []) {
                    rows.push(
                        <TableRow
                            key={rowNum}
                            className={rowNum % 2 == 0 ? 'bg-accent' : 'bg-muted/50'}
                        >
                            <TableCell className='max-w-[200px] break-words'>{auditLog.actor}</TableCell>
                            <TableCell>{change.field}</TableCell>
                            <TableCell className='break-normal max-w-[200px] break-words'>
                                {change.old || '--'}
                            </TableCell>
                            <TableCell className='break-normal max-w-[200px] break-words'>
                                {change.new || '--'}
                            </TableCell>
                            <TableCell>
                                {getLocalTimeString(auditLog.event_time)}
                            </TableCell>
                        </TableRow>
                    );
                    rowNum += 1;
                }
            }
        }

        return rows;
    };

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
                        Context Field Audit Logs
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
                                <TableCell>Field</TableCell>
                                <TableCell>Old Value</TableCell>
                                <TableCell>New Value</TableCell>
                                <TableCell>Event Time</TableCell>
                            </TableRow>
                        </TableHeader>
                        <TableBody>{getAuditLogRows()}</TableBody>
                    </Table>
                    {query.hasNextPage &&
                        <div className='flex justify-center m-4'>
                            <Button
                                onClick={() => query.fetchNextPage()}
                                disabled={!query.hasNextPage || query.isFetchingNextPage}
                            >
                                {query.isFetchingNextPage
                                    ? 'Loading more...'
                                    : 'Load more'
                                }
                            </Button>
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
