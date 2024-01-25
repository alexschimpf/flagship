'use client';

import { InviteUser } from '@/api';
import { Button } from '@/components/primitives/button';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from '@/components/primitives/dialog';
import { ScrollArea } from '@/components/primitives/scroll-area';
import {
    ToggleGroup,
    ToggleGroupItem,
} from '@/components/primitives/toggle-group';
import {
    Tooltip,
    TooltipContent,
    TooltipProvider,
    TooltipTrigger,
} from '@/components/primitives/tooltip';
import { useToast } from '@/components/primitives/use-toast';
import { apiClient, getErrorMessage } from '@/lib/api';
import { userRoles } from "@/lib/constants";
import { zodResolver } from '@hookform/resolvers/zod';
import { CheckCircledIcon, ExclamationTriangleIcon } from '@radix-ui/react-icons';
import {
    useMutation, useQuery, useQueryClient
} from '@tanstack/react-query';
import parseHTML from 'html-react-parser';
import { Loader2 } from 'lucide-react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import CustomTooltip from '../primitives/customTooltip';
import { Form, FormControl, FormField, FormItem, FormLabel } from '../primitives/form';
import { Input } from '../primitives/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../primitives/select';

const formSchema = z.object({
    email: z.string().min(1).max(320),
    name: z.string().min(1).max(128),
    role: z.string().min(1),
    projects: z.array(z.string()).min(1)
});

class InviteMemberDialogProps {
    trigger: any;
}

export default function (props: InviteMemberDialogProps) {
    const { toast } = useToast();

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            email: '',
            name: '',
            role: '',
            projects: []
        }
    });

    const queryClient = useQueryClient();
    const projectsQuery = useQuery({
        queryKey: ['projects'],
        queryFn: () => apiClient.projects.getProjects()
    });

    const projects = projectsQuery.data?.items || [];

    const mutation = useMutation({
        mutationFn: (user: InviteUser) => {
            return apiClient.users.inviteUser(user);
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
            queryClient.invalidateQueries({ queryKey: ['users'] });
            toast({
                variant: 'success',
                title: (
                    <div className='flex flex-row items-center'>
                        <CheckCircledIcon />
                        <p className='text-black ml-2 font-bold'>Success!</p>
                    </div>
                ),
                description: 'Member was sucessfully invited.',
            });
        }
    });

    const onSubmit = (values: z.infer<typeof formSchema>) => mutation.mutate({
        email: values.email,
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
                            {props.trigger}
                        </DialogTrigger>
                    </TooltipTrigger>
                    <TooltipContent>
                        <p>Invite member</p>
                    </TooltipContent>
                </Tooltip>
            </TooltipProvider>
            <DialogContent className='sm:max-w-[425px]' onCloseAutoFocus={(e) => { e.preventDefault(); }}>
                <DialogHeader>
                    <DialogTitle>Invite Member</DialogTitle>
                </DialogHeader>
                <div className='w-full'>
                    <Form {...form}>
                        <form onSubmit={form.handleSubmit(onSubmit)} className='space-y-4 flex flex-col items-end'>
                            <FormField
                                control={form.control}
                                name='email'
                                render={({ field }) => (
                                    <FormItem className='w-full'>
                                        <FormLabel>Email</FormLabel>
                                        <FormControl>
                                            <Input {...field} />
                                        </FormControl>
                                    </FormItem>
                                )}
                            />
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
                                        <CustomTooltip text={[
                                            'Read only users can view feature flags.',
                                            'Standard users can manage feature flags.',
                                            'Admins can manage feature flags, manage context fields, and view audit logs.',
                                            'Owners can do anything, including user management.'
                                        ]} />
                                        <Select onValueChange={field.onChange} defaultValue={field.value}>
                                            <FormControl>
                                                <SelectTrigger>
                                                    <SelectValue placeholder='Select a role' />
                                                </SelectTrigger>
                                            </FormControl>
                                            <SelectContent>
                                                {Object.entries(userRoles).map(([roleId, roleName]) => (
                                                    <SelectItem value={roleId.toString()}>{roleName}</SelectItem>
                                                ))}
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
                                            <ToggleGroup type='multiple' onValueChange={field.onChange}>
                                                <ScrollArea className='w-full rounded-md border min-h-20 max-h-40 p-2'>
                                                    {projectsQuery.isFetching &&
                                                        <div className='flex items-center justify-center size-full'>
                                                            <Loader2 className='animate-spin text-center' size={48} />
                                                        </div>
                                                    }
                                                    {projectsQuery.isSuccess && !projectsQuery.isFetching &&
                                                        projects.map((project) => (
                                                            <ToggleGroupItem className='m-0.5' value={project.project_id.toString()}>
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
                            {!mutation.isSuccess &&
                                <Button type='submit' className='w-1/4' disabled={mutation.isPending}>Invite</Button>
                            }
                        </form>
                    </Form>
                </div>
            </DialogContent>
        </Dialog>
    );
}