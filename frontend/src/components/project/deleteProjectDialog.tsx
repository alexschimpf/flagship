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

class DeleteProjectDialogProps {
    projectId!: number;
    name!: string;
    trigger: any;
}

export default function DeleteProjectDialog(props: DeleteProjectDialogProps) {
    const { toast } = useToast();
    const queryClient = useQueryClient();
    const mutation = useMutation({
        mutationFn: () => {
            return apiClient.projects.deleteProject(props.projectId);
        },
        onError: error => {
            toast(getErrorToast(error));
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['projects'] });
            toast(getSuccessToast('Project was sucessfully deleted.'));
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
                    <DialogHeader className='border-b pb-4'>
                        <DialogTitle>Delete Project</DialogTitle>
                    </DialogHeader>
                    <div className='w-full flex flex-col items-end'>
                        <p className='w-full max-w-[375px] break-words'>
                            Are you sure you want delete project{' '}
                            <b>{props.name}</b>? This cannot be undone.
                        </p>
                        <Button
                            className='w-1/4 mt-4 bg-destructive text-destructive-foreground'
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
