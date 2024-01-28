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
import { useToast } from '@/components/primitives/use-toast';
import { apiClient, getErrorToast, getSuccessToast } from '@/lib/api';
import { ErrorMessage } from '@hookform/error-message';
import { zodResolver } from '@hookform/resolvers/zod';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import * as z from 'zod';

const formSchema = z.object({
    name: z.string().min(1).max(256)
});

class EditProjectDialogProps {
    projectId!: number;
    initialName!: string;
    trigger: any;
}

export default function (props: EditProjectDialogProps) {
    const { toast } = useToast();
    const [open, setOpen] = useState(false);
    const queryClient = useQueryClient();
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            name: props.initialName
        }
    });
    const [lastSavedName, setLastSavedName] = useState(props.initialName);
    const mutation = useMutation({
        mutationFn: (name: string) => {
            return apiClient.projects.updateProject(props.projectId, {
                name: name
            });
        },
        onError: error => {
            toast(getErrorToast(error));
        },
        onSuccess: () => {
            setLastSavedName(form.getValues().name);
            queryClient.invalidateQueries({ queryKey: ['projects'] });
            toast(getSuccessToast('Project was sucessfully updated.'));
            setOpen(false);
        }
    });
    const onSubmit = (values: z.infer<typeof formSchema>) => {
        mutation.mutate(values.name);
    };
    const onOpenChange = (open: boolean) => {
        form.reset({
            name: lastSavedName
        });
        mutation.reset();
        setOpen(open);
    };

    return (
        <div>
            <Dialog onOpenChange={onOpenChange} open={open}>
                <DialogTrigger asChild>{props.trigger}</DialogTrigger>
                <DialogContent
                    className='sm:max-w-[425px]'
                    onCloseAutoFocus={e => {
                        e.preventDefault();
                    }}
                >
                    <DialogHeader>
                        <DialogTitle>Edit Project</DialogTitle>
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
                                                    className='disabled:cursor-default'
                                                    placeholder=''
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
                                <Button
                                    type='submit'
                                    className='w-1/4'
                                    disabled={
                                        mutation.isPending || mutation.isSuccess
                                    }
                                >
                                    Save
                                </Button>
                            </form>
                        </Form>
                    </div>
                </DialogContent>
            </Dialog>
        </div>
    );
}
