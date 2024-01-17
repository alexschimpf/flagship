'use client';

import { apiClient } from '@/utils/api';
import { getLocalTimeString } from '@/utils/time';
import { useQuery } from '@tanstack/react-query';
import { Loader2 } from 'lucide-react';
import { Table, TableBody, TableCell, TableHeader, TableRow } from '../ui/table';

export default function() {
    const query = useQuery({
        queryKey: [`audit-logs`], 
        queryFn: () => apiClient.admin.getAuditLogs()
    });

	const auditLogs = query?.data?.items || [];

    return (
        <div className='flex flex-col w-full justify-center'>
            <h1 className='text-center text-lg font-bold mt-5 pt-0.5'>Audit Logs</h1>
            {auditLogs.length > 0 &&
                <div className='p-4 flex flex-col fade-in-0 w-full'>
                    <Table>
                        <TableHeader>
                            <TableRow className='font-bold hover:bg-white'>
                                <TableCell>Actor</TableCell>
                                <TableCell>Event Type</TableCell>
                                <TableCell>Details</TableCell>
                                <TableCell>Event Time</TableCell>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {auditLogs.map((auditLog, i) => (
                                <TableRow key={i} className={i % 2 == 0 ? 'bg-accent' : 'bg-white'}>
                                    <TableCell>{auditLog.actor}</TableCell>
                                    <TableCell>{auditLog.event_type}</TableCell>
                                    <TableCell>{auditLog.details}</TableCell>
                                    <TableCell>{ getLocalTimeString(auditLog.event_time) }</TableCell>
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
