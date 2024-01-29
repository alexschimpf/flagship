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

class DeleteMemberDialogProps {
    userId!: number;
    email!: string;
    trigger: any;
}

export default function (props: DeleteMemberDialogProps) {
    const { toast } = useToast();
    const queryClient = useQueryClient();
    const mutation = useMutation({
        mutationFn: () => {
            return apiClient.users.deleteUser(props.userId);
        },
        onError: error => {
            toast(getErrorToast(error));
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['users'] });
            toast(getSuccessToast('Member was sucessfully deleted.'));
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
                        <DialogTitle>Delete User</DialogTitle>
                    </DialogHeader>
                    <div className='w-full flex flex-col items-end'>
                        <p className='w-full max-w-[375px] break-words'>
                            Are you sure you want delete user{' '}
                            <b>{props.email}</b>? This cannot be undone.
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
