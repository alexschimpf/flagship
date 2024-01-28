'use client';

import { apiClient } from '@/lib/api';
import { getLocalTimeString } from "@/lib/utils";
import { ArrowLeftIcon } from '@radix-ui/react-icons';
import { useQuery } from '@tanstack/react-query';
import { Loader2 } from 'lucide-react';
import { useParams, useRouter } from 'next/navigation';
import { Button } from '../primitives/button';
import { Table, TableBody, TableCell, TableHeader, TableRow } from '../primitives/table';

export default function () {
    const params = useParams<{ projectId: string, contextFieldId: string; }>();
    const router = useRouter();

    const contextFieldId = parseInt(params.contextFieldId);
    const projectId = parseInt(params.projectId);

    const query = useQuery({
        queryKey: [`audit-logs`],
        queryFn: () => apiClient.contextFields.getContextFieldAuditLogs(contextFieldId, projectId)
    });

    const auditLogs = query?.data?.items || [];

    const onBackClick = () => router.replace(`/project/${projectId}/context-fields`);

    const getAuditLogRows = () => {
        let rowNum = 0;
        const rows = [];
        for (const auditLog of auditLogs) {
            for (const change of auditLog?.changes || []) {
                rows.push(
                    <TableRow key={rowNum} className={rowNum % 2 == 0 ? 'bg-accent' : 'bg-white'}>
                        <TableCell>{auditLog.actor}</TableCell>
                        <TableCell>{change.field}</TableCell>
                        <TableCell className='break-normal'>{change.old || '--'}</TableCell>
                        <TableCell className='break-normal'>{change.new || '--'}</TableCell>
                        <TableCell>{getLocalTimeString(auditLog.event_time)}</TableCell>
                    </TableRow>
                );
                rowNum += 1;
            }
        }

        return rows;
    };

    return (
        <div className='flex flex-col w-full justify-center'>
            <div className='flex items-center justify-center mt-4 h-10'>
                <div className='flex-1'>
                    <Button variant='ghost' className='hover:bg-accent px-2 size-9' onClick={onBackClick}>
                        <ArrowLeftIcon className='size-8 cursor-pointer' />
                    </Button>
                </div>
                <div className='flex-1'>
                    <h1 className='text-center text-lg font-bold'>Context Field Audit Logs</h1>
                </div>
                <div className='flex-1'>
                </div>
            </div>
            {auditLogs.length > 0 &&
                <div className='p-4 flex flex-col fade-in-0 w-full'>
                    <Table>
                        <TableHeader>
                            <TableRow className='font-bold hover:bg-white'>
                                <TableCell>Actor</TableCell>
                                <TableCell>Field</TableCell>
                                <TableCell>Old Value</TableCell>
                                <TableCell>New Value</TableCell>
                                <TableCell>Event Time</TableCell>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {getAuditLogRows()}
                        </TableBody>
                    </Table>
                </div>
            }
            {query.isFetching &&
                <div className='absolute top-[calc(50%-41px)] left-1/2'>
                    <Loader2 className='animate-spin' size={48} />
                </div>
            }
        </div>
    );
}
