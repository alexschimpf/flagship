'use client';

import { UpdateUser } from '@/api';
import { Button } from '@/components/ui/button';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from '@/components/ui/dialog';
import { ScrollArea } from '@/components/ui/scroll-area';
import {
    ToggleGroup,
    ToggleGroupItem,
} from '@/components/ui/toggle-group';
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
    useMutation, useQuery, useQueryClient
} from '@tanstack/react-query';
import { Loader2 } from 'lucide-react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { Form, FormControl, FormField, FormItem, FormLabel } from '../ui/form';
import { Input } from '../ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';

const formSchema = z.object({
    name: z.string().min(1).max(128),
    role: z.string().min(1),
    projects: z.array(z.string()).min(1)
});

class EditMemberDialogProps {
    userId!: number
    trigger: any
}

  
export default function(props: EditMemberDialogProps) {
    const { toast } = useToast();

    const userQuery = useQuery({
        queryKey: [`users/${props.userId}`], 
        queryFn: () => apiClient.users.getUser(props.userId)
    });

    const user: any = userQuery?.data || {};

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        values: {
            name: user?.name || '',
            role: (user?.role || '').toString(),
            projects: (user?.projects || []).map((project: number) => project.toString())
        }
    });

    const queryClient = useQueryClient(); 
    const projectsQuery = useQuery({
        queryKey: ['projects'], 
        queryFn: () => apiClient.projects.getProjects()
    });

    const projects = projectsQuery.data?.items || [];

    const mutation = useMutation({
        mutationFn: (user: UpdateUser) => {
            return apiClient.users.updateUser(props.userId, {
                name: user.name,
                role: user.role,
                projects: user.projects
            });
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
            queryClient.invalidateQueries({queryKey: ['users']});
            queryClient.invalidateQueries({queryKey: [`users/${props.userId}`]});
            toast({
                variant: 'success',
                title: (
                    <div className='flex flex-row items-center'>
                        <CheckCircledIcon />
                        <p className='text-black ml-2 font-bold'>Success!</p>
                    </div>
                ),
                description: 'Member was sucessfully updated.',
            })
        }
    });

    const onSubmit = (values: z.infer<typeof formSchema>) => mutation.mutate({
        name: values.name,
        role: parseInt(values.role),
        projects: values.projects.map((value) => parseInt(value))
    });

    const onOpenChange = () => {
        form.reset();
        mutation.reset();
    };

	return (
        <Dialog onOpenChange={onOpenChange}>
            <TooltipProvider>
                <Tooltip>
                    <TooltipTrigger>
                        <DialogTrigger asChild>
                        { props.trigger }
                        </DialogTrigger>
                    </TooltipTrigger>
                    <TooltipContent>
                        <p>Update member</p>
                    </TooltipContent>
                </Tooltip>
            </TooltipProvider>
            <DialogContent className='sm:max-w-[425px]' onCloseAutoFocus={(e) => { e.preventDefault() }}>
                <DialogHeader>
                    <DialogTitle>Update Member</DialogTitle>
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
                                            <Input {...field} />
                                        </FormControl>
                                    </FormItem>
                                )}
                            />
                            <FormField
                                control={form.control}
                                name='role'
                                render={({ field }) => (
                                    <FormItem className='w-full'>
                                        <FormLabel>Role</FormLabel>
                                        <Select onValueChange={field.onChange} defaultValue={field.value}>
                                            <FormControl>
                                                <SelectTrigger>
                                                    <SelectValue placeholder='Select a role' />
                                                </SelectTrigger>
                                            </FormControl>
                                            <SelectContent>
                                                <SelectItem value='1'>Read only</SelectItem>
                                                <SelectItem value='2'>Standard</SelectItem>
                                                <SelectItem value='3'>Admin</SelectItem>
                                                <SelectItem value='4'>Owner</SelectItem>
                                            </SelectContent>
                                        </Select>
                                    </FormItem>
                                )}
                            />
                            <FormField
                                control={form.control}
                                name='projects'
                                render={({ field }) => (
                                    <FormItem className='w-full'>
                                        <FormLabel>Projects</FormLabel>
                                        <FormControl className='flex flex-col items-center justify-center'>
                                            <ToggleGroup type='multiple' onValueChange={field.onChange} value={field.value}>
                                                <ScrollArea className='w-full rounded-md border min-h-20 max-h-40 p-2'>
                                                    {projectsQuery.isFetching && 
                                                        <div className='flex items-center justify-center size-full'>
                                                            <Loader2 className='animate-spin text-center' size={48} />
                                                        </div>
                                                    }
                                                    {projectsQuery.isSuccess && !projectsQuery.isFetching &&
                                                        projects.map((project) => (
                                                            <ToggleGroupItem value={project.project_id.toString()}>
                                                                <p>{project.name}</p>
                                                            </ToggleGroupItem>
                                                        ))
                                                    }
                                                </ScrollArea>
                                            </ToggleGroup>
                                        </FormControl>
                                    </FormItem>
                                )}
                            />
                            <Button type='submit' className='w-1/4' disabled={mutation.isPending}>Save</Button>
                        </form>
                    </Form>
                </div>
            </DialogContent>
        </Dialog>
    )
}
