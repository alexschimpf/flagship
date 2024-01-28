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

interface DeleteProjectPrivateKeyDialogProps {
    projectId: number;
    projectPrivateKeyId: number;
    name: string;
    trigger: any;
}

export default function (props: DeleteProjectPrivateKeyDialogProps) {
    const { toast } = useToast();
    const queryClient = useQueryClient();
    const mutation = useMutation({
        mutationFn: () => {
            return apiClient.projects.deleteProjectPrivateKey(
                props.projectId,
                props.projectPrivateKeyId
            );
        },
        onError: error => {
            toast(getErrorToast(error));
        },
        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: [`projects/${props.projectId}/private-keys`]
            });
            toast(
                getSuccessToast('Project private key was sucessfully deleted.')
            );
        }
    });

    return (
        <div>
            <Dialog>
                <TooltipProvider>
                    <Tooltip>
                        <TooltipTrigger>
                            <DialogTrigger asChild>
                                {props.trigger}
                            </DialogTrigger>
                        </TooltipTrigger>
                        <TooltipContent>
                            <p>Delete project private key</p>
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
                        <DialogTitle>Delete Project Private Key</DialogTitle>
                    </DialogHeader>
                    <div className='w-full flex flex-col items-end'>
                        <p className='w-full'>
                            Are you sure you want delete project private key{' '}
                            <b>{props.name}</b>? This cannot be undone.
                        </p>
                        <Button
                            className='w-1/4 mt-4 bg-destructive'
                            disabled={mutation.isPending || mutation.isSuccess}
                            onClick={() => mutation.mutate()}
                        >
                            Delete
                        </Button>
                    </div>
                </DialogContent>
            </Dialog>
        </div>
    );
}
