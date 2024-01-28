'use client';

import { Button } from '@/components/primitives/button';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogTrigger
} from '@/components/primitives/dialog';
import { useToast } from '@/components/primitives/use-toast';
import { apiClient, getErrorToast, getSuccessToast } from '@/lib/api';
import { useMutation, useQueryClient } from '@tanstack/react-query';

class DeleteContextFieldDialogProps {
    projectId!: number;
    contextFieldId!: number;
    name!: string;
    trigger: any;
}

export default function (props: DeleteContextFieldDialogProps) {
    const { toast } = useToast();
    const queryClient = useQueryClient();
    const mutation = useMutation({
        mutationFn: () => {
            return apiClient.contextFields.deleteContextField(
                props.contextFieldId,
                props.projectId
            );
        },
        onError: error => {
            toast(getErrorToast(error));
        },
        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: [`projects/${props.projectId}/context-fields`]
            });
            toast(getSuccessToast('Context field was sucessfully deleted.'));
        }
    });

    return (
        <div>
            <Dialog>
                <DialogTrigger asChild>{props.trigger}</DialogTrigger>
                <DialogContent
                    className='sm:max-w-[425px]'
                    onCloseAutoFocus={e => {
                        e.preventDefault();
                    }}
                >
                    <DialogHeader>
                        <DialogTitle>Delete Context Field</DialogTitle>
                    </DialogHeader>
                    <div className='w-full flex flex-col items-end'>
                        <p className='w-full'>
                            Are you sure you want delete context field{' '}
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
