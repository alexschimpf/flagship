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
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import {
    Tooltip,
    TooltipContent,
    TooltipProvider,
    TooltipTrigger,
} from '@/components/ui/tooltip';
import { useToast } from '@/components/ui/use-toast';
import { apiClient, getErrorMessage } from '@/utils/api';
import { zodResolver } from '@hookform/resolvers/zod';
import { CheckCircledIcon, ExclamationTriangleIcon } from '@radix-ui/react-icons';
import {
    useMutation, useQueryClient
} from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import * as z from 'zod';
 

const formSchema = z.object({
    name: z.string()
});

class NewProjectDialogProps {
    trigger: any
}

  
export default function NewProjectDialog(props: NewProjectDialogProps) {
    const { toast } = useToast();
    const queryClient = useQueryClient(); 
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            name: ''
        }
    });
    const mutation = useMutation({
        mutationFn: (name: string) => {
            return apiClient.projects.createProject({ name })
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
                description: getErrorMessage(error),
            })
        },
        onSuccess: () => {
            toast({
                variant: 'success',
                title: (
                    <div className='flex flex-row items-center'>
                        <CheckCircledIcon />
                        <p className='text-black ml-2 font-bold'>Success!</p>
                    </div>
                ),
                description: 'Your project was sucessfully created.',
            })
        }
    });
    const onSubmit = (values: z.infer<typeof formSchema>) => {
        mutation.mutate(values.name);
    };
    const onOpenChange = (open: boolean) => {
        form.reset();
        mutation.reset();

        if (!open && mutation.isSuccess) {
            queryClient.invalidateQueries({queryKey: ['projects']});
        }
    };

	return (
        <div>
            <Dialog onOpenChange={onOpenChange}>
                <TooltipProvider>
                    <Tooltip>
                        <TooltipTrigger>
                            <DialogTrigger asChild>
                            { props.trigger }
                            </DialogTrigger>
                        </TooltipTrigger>
                        <TooltipContent>
                            <p>Add new project</p>
                        </TooltipContent>
                    </Tooltip>
                </TooltipProvider>
                <DialogContent className='sm:max-w-[425px]' onCloseAutoFocus={(e) => { e.preventDefault() }}>
                    <DialogHeader>
                        <DialogTitle>New Project</DialogTitle>
                    </DialogHeader>
                    <div className='w-full'>
                        <Form {...form}>
                            <form onSubmit={form.handleSubmit(onSubmit)} className='space-y-4 flex flex-col items-end'>
                                <FormField
                                    control={form.control}
                                    name='name'
                                    render={({ field }) => (
                                        <FormItem className='w-full'>
                                            <FormLabel>Name</FormLabel>
                                            <FormControl>
                                                <Input disabled={mutation.isSuccess} className='disabled:cursor-default' placeholder='' {...field} />
                                            </FormControl>
                                        </FormItem>
                                    )}
                                />
                                {!mutation.isSuccess &&
                                    <Button type='submit' className='w-1/4' disabled={mutation.isPending}>Create</Button>
                                }
                            </form>
                        </Form>
                        {mutation.isSuccess &&
                            <div className='mt-4'>
                                <p className='mb-4 text-red-500 text-sm text-center'>Your project's <b>secret key</b> is below. Please save it somewhere safe and accessible. It is needed to authenticate your client's requests. You <b>will not</b> see it again after this dialog closes.</p>
                                <Textarea className='bg-accent cursor-pointer resize-none text-center' value={mutation.data.private_key}></Textarea>
                            </div>
                        }
                    </div>
                </DialogContent>
            </Dialog>
        </div>
    )
}
