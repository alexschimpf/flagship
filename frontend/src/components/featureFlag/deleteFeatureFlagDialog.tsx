'use client';

import { Button } from '@/components/primitives/button';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from '@/components/primitives/dialog';
import { useToast } from '@/components/primitives/use-toast';
import { apiClient, getErrorMessage } from '@/lib/api';
import { CheckCircledIcon, ExclamationTriangleIcon } from '@radix-ui/react-icons';
import {
    useMutation, useQueryClient
} from '@tanstack/react-query';
import parseHTML from 'html-react-parser';

class DeleteFeatureFlagDialogProps {
    projectId!: number;
    featureFlagId!: number;
    name!: string;
    trigger: any;
}

export default function (props: DeleteFeatureFlagDialogProps) {
    const { toast } = useToast();
    const queryClient = useQueryClient();
    const mutation = useMutation({
        mutationFn: () => {
            return apiClient.featureFlags.deleteFeatureFlag(props.featureFlagId, props.projectId);
        },
        onError: (error) => {
            toast({
                variant: 'destructive',
                title: (
                    <div className='flex flex-row items-center'>
                        <ExclamationTriangleIcon />
                        <p className='text-white ml-2 font-bold'>Uh oh...</p>
                    </div>
                ),
                description: <p>{parseHTML(getErrorMessage(error))}</p>,
            });
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: [`projects/${props.projectId}/feature-flags`] });
            toast({
                variant: 'success',
                title: (
                    <div className='flex flex-row items-center'>
                        <CheckCircledIcon />
                        <p className='text-black ml-2 font-bold'>Success!</p>
                    </div>
                ),
                description: 'Feature flag was sucessfully deleted.',
            });
        }
    });

    return (
        <div>
            <Dialog>
                <DialogTrigger asChild>
                    {props.trigger}
                </DialogTrigger>
                <DialogContent className='sm:max-w-[425px]' onCloseAutoFocus={(e) => { e.preventDefault(); }}>
                    <DialogHeader>
                        <DialogTitle>Delete Feature Flag</DialogTitle>
                    </DialogHeader>
                    <div className='w-full flex flex-col items-end'>
                        <p className='w-full'>Are you sure you want delete feature flag <b>{props.name}</b>? This cannot be undone.</p>
                        <Button className='w-1/4 mt-4 bg-destructive' disabled={mutation.isPending || mutation.isSuccess} onClick={() => mutation.mutate()}>Delete</Button>
                    </div>
                </DialogContent>
            </Dialog>
        </div>
    );
}