'use client';

import { Button } from '@/components/ui/button';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from '@/components/ui/dialog';
import {
    Tooltip,
    TooltipContent,
    TooltipProvider,
    TooltipTrigger,
} from '@/components/ui/tooltip';
import { useToast } from '@/components/ui/use-toast';
import { apiClient, getErrorMessage } from '@/utils/api';
import { CheckCircledIcon, ExclamationTriangleIcon } from '@radix-ui/react-icons';
import {
    useMutation, useQueryClient
} from '@tanstack/react-query';
import parseHTML from 'html-react-parser';
 

class DeleteProjectPrivateKeyDialogProps {
    projectId!: number
    projectPrivateKeyId!: number
    name!: string
    trigger: any
}

  
export default function(props: DeleteProjectPrivateKeyDialogProps) {
    const { toast } = useToast();
    const queryClient = useQueryClient(); 
    const mutation = useMutation({
        mutationFn: () => {
            return apiClient.projects.deleteProjectPrivateKey(props.projectId, props.projectPrivateKeyId);
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
            })
        },
        onSuccess: () => {
            queryClient.invalidateQueries({queryKey: [`projects/${props.projectId}/private-keys`]});
            toast({
                variant: 'success',
                title: (
                    <div className='flex flex-row items-center'>
                        <CheckCircledIcon />
                        <p className='text-black ml-2 font-bold'>Success!</p>
                    </div>
                ),
                description: 'Your project private key was sucessfully deleted.',
            })
        }
    });

	return (
        <div>
            <Dialog>
                <TooltipProvider>
                    <Tooltip>
                        <TooltipTrigger>
                            <DialogTrigger asChild>
                            { props.trigger }
                            </DialogTrigger>
                        </TooltipTrigger>
                        <TooltipContent>
                            <p>Delete project private key</p>
                        </TooltipContent>
                    </Tooltip>
                </TooltipProvider>
                <DialogContent className='sm:max-w-[425px]' onCloseAutoFocus={(e) => { e.preventDefault() }}>
                    <DialogHeader>
                        <DialogTitle>Delete Project Private Key</DialogTitle>
                    </DialogHeader>
                    <div className='w-full flex flex-col items-end'>
                        <p className='w-full'>Are you sure you want delete project private key <b>{props.name}</b>? This cannot be undone.</p>
                        <Button className='w-1/4 mt-4 bg-destructive' disabled={mutation.isPending || mutation.isSuccess} onClick={() => mutation.mutate()}>Delete</Button>
                    </div>
                </DialogContent>
            </Dialog>
        </div>
    )
}
