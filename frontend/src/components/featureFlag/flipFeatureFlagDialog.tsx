'use client';

import { Button } from '@/components/primitives/button';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogTrigger
} from '@/components/primitives/dialog';
import {
    Tooltip,
    TooltipContent,
    TooltipProvider,
    TooltipTrigger
} from '@/components/primitives/tooltip';
import { useToast } from '@/components/primitives/use-toast';
import { apiClient, getErrorToast, getSuccessToast } from '@/lib/api';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useState } from 'react';
import * as z from 'zod';

const formSchema = z.object({
    name: z.string()
});

interface FlipFeatureFlagDialogProps {
    name: string;
    projectId: number;
    featureFlagId: number;
    enabled: boolean;
    trigger: any;
}

export default function FlipFeatureFlagDialog(
    props: FlipFeatureFlagDialogProps
) {
    const { toast } = useToast();
    const [open, setOpen] = useState(false);
    const queryClient = useQueryClient();
    const mutation = useMutation({
        mutationFn: () => {
            return apiClient.featureFlags.updateFeatureFlagStatus(
                props.featureFlagId,
                props.projectId,
                {
                    enabled: props.enabled
                }
            );
        },
        onError: error => {
            toast(getErrorToast(error));
        },
        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: [`projects/${props.projectId}/feature-flags`]
            });
            queryClient.invalidateQueries({
                queryKey: [
                    `projects/${props.projectId}/feature-flags/${props.featureFlagId}`
                ]
            });
            toast(
                getSuccessToast(
                    `Feature flag was ${props.enabled ? 'enabled' : 'disabled'}.`
                )
            );
            setOpen(false);
        }
    });
    const onOpenChange = (open: boolean) => {
        mutation.reset();
        setOpen(open);
    };

    return (
        <div>
            <Dialog onOpenChange={onOpenChange} open={open}>
                <TooltipProvider>
                    <Tooltip>
                        <TooltipTrigger>
                            <DialogTrigger asChild>
                                {props.trigger}
                            </DialogTrigger>
                        </TooltipTrigger>
                        <TooltipContent>
                            <p>Enable/disable feature flag</p>
                        </TooltipContent>
                    </Tooltip>
                </TooltipProvider>
                <DialogContent
                    className='sm:max-w-[425px]'
                    onCloseAutoFocus={e => {
                        e.preventDefault();
                    }}
                >
                    <DialogHeader>
                        <DialogTitle>{`${props.enabled ? 'Enable' : 'Disable'} Feature Flag`}</DialogTitle>
                    </DialogHeader>
                    <div className='w-full'>
                        <p className='m-4'>
                            Are you sure you want to{' '}
                            {props.enabled ? 'enable' : 'disable'} feature flag{' '}
                            <b>{props.name}?</b>
                        </p>
                        <div className='flex justify-end'>
                            <Button
                                className='w-1/4'
                                disabled={mutation.isPending}
                                onClick={() => mutation.mutate()}
                            >
                                {props.enabled ? 'Enable' : 'Disable'}
                            </Button>
                        </div>
                    </div>
                </DialogContent>
            </Dialog>
        </div>
    );
}
