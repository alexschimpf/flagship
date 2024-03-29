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
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel
} from '@/components/primitives/form';
import { Input } from '@/components/primitives/input';
import { Textarea } from '@/components/primitives/textarea';
import {
    Tooltip,
    TooltipContent,
    TooltipProvider,
    TooltipTrigger
} from '@/components/primitives/tooltip';
import { useToast } from '@/components/primitives/use-toast';
import { apiClient, getErrorToast, getSuccessToast } from '@/lib/api';
import { ErrorMessage } from '@hookform/error-message';
import { zodResolver } from '@hookform/resolvers/zod';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import * as z from 'zod';

const formSchema = z.object({
    name: z.string().min(1).max(128)
});

class NewProjectDialogProps {
    trigger: any;
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
            return apiClient.projects.createProject({ name });
        },
        onError: error => {
            toast(getErrorToast(error));
        },
        onSuccess: () => {
            toast(getSuccessToast('Project was sucessfully created.'));
        }
    });
    const onSubmit = (values: z.infer<typeof formSchema>) => {
        mutation.mutate(values.name);
    };
    const onOpenChange = (open: boolean) => {
        form.reset();
        mutation.reset();

        if (!open && mutation.isSuccess) {
            queryClient.invalidateQueries({ queryKey: ['projects'] });
        }
    };
    const onPrivateKeyClick = (e: any) => {
        e.currentTarget.select();
    };

    return (
        <div>
            <Dialog onOpenChange={onOpenChange}>
                <TooltipProvider>
                    <Tooltip>
                        <TooltipTrigger>
                            <DialogTrigger asChild>
                                {props.trigger}
                            </DialogTrigger>
                        </TooltipTrigger>
                        <TooltipContent>
                            <p>Add new project</p>
                        </TooltipContent>
                    </Tooltip>
                </TooltipProvider>
                <DialogContent
                    className='sm:max-w-[425px]'
                    onCloseAutoFocus={e => {
                        e.preventDefault();
                    }}
                >
                    <DialogHeader className='border-b pb-4'>
                        <DialogTitle>New Project</DialogTitle>
                    </DialogHeader>
                    <div className='w-full'>
                        <Form {...form}>
                            <form
                                onSubmit={form.handleSubmit(onSubmit)}
                                className='space-y-4 flex flex-col items-end'
                            >
                                <FormField
                                    control={form.control}
                                    name='name'
                                    render={({ field }) => (
                                        <FormItem className='w-full'>
                                            <FormLabel>Name*</FormLabel>
                                            <FormControl>
                                                <Input
                                                    disabled={
                                                        mutation.isSuccess
                                                    }
                                                    className='disabled:cursor-default'
                                                    {...field}
                                                />
                                            </FormControl>
                                        </FormItem>
                                    )}
                                />
                                <ErrorMessage
                                    errors={form.formState.errors}
                                    name='name'
                                />
                                {!mutation.isSuccess && (
                                    <Button
                                        type='submit'
                                        className='w-1/4'
                                        disabled={mutation.isPending}
                                    >
                                        Create
                                    </Button>
                                )}
                            </form>
                        </Form>
                        {mutation.isSuccess && (
                            <div className='mt-4'>
                                <p className='mb-4 text-red-500 text-sm text-center'>
                                    Your project&lsquo;s <b>secret key</b> is
                                    below. Please save it somewhere safe and
                                    accessible. It is needed to authenticate
                                    your client&lsquo;s requests. You{' '}
                                    <b>will not</b> see it again after this
                                    dialog closes.
                                </p>
                                <Textarea
                                    className='bg-accent cursor-pointer resize-none text-center'
                                    value={mutation.data.private_key}
                                    onClick={onPrivateKeyClick}
                                />
                            </div>
                        )}
                    </div>
                </DialogContent>
            </Dialog>
        </div>
    );
}
