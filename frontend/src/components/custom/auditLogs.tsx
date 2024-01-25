'use client';

import { apiClient } from '@/utils/api';
import { getLocalTimeString } from '@/utils/time';
import { ArrowLeftIcon } from '@radix-ui/react-icons';
import { useQuery } from '@tanstack/react-query';
import { Loader2 } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { Button } from '../ui/button';
import { Table, TableBody, TableCell, TableHeader, TableRow } from '../ui/table';

export default function() {
    const router = useRouter();
    const query = useQuery({
        queryKey: [`audit-logs`], 
        queryFn: () => apiClient.admin.getAuditLogs()
    });

	const auditLogs = query?.data?.items || [];

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
                    <h1 className='text-center text-lg font-bold'>Audit Logs</h1>
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
                <div className='absolute top-[calc(50%-41px)] left-1/2'>
                    <Loader2 className='animate-spin' size={48} />
                </div>
            }
        </div>
    )
}
