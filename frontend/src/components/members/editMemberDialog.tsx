'use client';

import { UpdateUser } from '@/api';
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
import { useToast } from '@/components/primitives/use-toast';
import { UserContext } from '@/context/userContext';
import { apiClient, getErrorMessage } from '@/lib/api';
import { userRoles } from "@/lib/constants";
import { Permission, hasPermission } from '@/lib/permissions';
import { ErrorMessage } from '@hookform/error-message';
import { zodResolver } from '@hookform/resolvers/zod';
import { CheckCircledIcon, ExclamationTriangleIcon } from '@radix-ui/react-icons';
import {
    useMutation, useQuery, useQueryClient
} from '@tanstack/react-query';
import parseHTML from 'html-react-parser';
import { Loader2 } from 'lucide-react';
import { useContext } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import CustomTooltip from '../primitives/customTooltip';
import { Form, FormControl, FormField, FormItem, FormLabel } from '../primitives/form';
import { Input } from '../primitives/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../primitives/select';

const formSchema = z.object({
    name: z.string().min(1).max(128),
    role: z.string().min(1, {
        message: 'User must be assigned a role'
    }),
    projects: z.array(z.string()).min(1, {
        message: 'User must be assigned to at least one project'
    })
});

class EditMemberDialogProps {
    userId!: number;
    trigger: any;
}

export default function (props: EditMemberDialogProps) {
    const { toast } = useToast();

    const currentUser = useContext(UserContext);

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
                description: <p>{parseHTML(getErrorMessage(error))}</p>,
            });
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['users'] });
            queryClient.invalidateQueries({ queryKey: [`users/${props.userId}`] });
            toast({
                variant: 'success',
                title: (
                    <div className='flex flex-row items-center'>
                        <CheckCircledIcon />
                        <p className='text-black ml-2 font-bold'>Success!</p>
                    </div>
                ),
                description: 'Member was sucessfully updated.',
            });
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
            <DialogTrigger asChild>
                {props.trigger}
            </DialogTrigger>
            <DialogContent className='sm:max-w-[425px]' onCloseAutoFocus={(e) => { e.preventDefault(); }}>
                <DialogHeader>
                    <DialogTitle>Edit Member</DialogTitle>
                </DialogHeader>
                <div className='w-full'>
                    <Form {...form}>
                        <form onSubmit={form.handleSubmit(onSubmit)} className='space-y-4 flex flex-col items-end'>
                            <FormField
                                control={form.control}
                                name='name'
                                render={({ field }) => (
                                    <FormItem className='w-full'>
                                        <FormLabel>Name*</FormLabel>
                                        <FormControl>
                                            <Input {...field} />
                                        </FormControl>
                                    </FormItem>
                                )}
                            />
                            <ErrorMessage errors={form.formState.errors} name='name' />
                            <FormField
                                control={form.control}
                                name='role'
                                render={({ field }) => (
                                    <FormItem className='w-full'>
                                        <FormLabel>Role*</FormLabel>
                                        <CustomTooltip text={[
                                            'Read only: Can view feature flags.',
                                            'Standard: Can manage feature flags.',
                                            'Admin: Can manage feature flags, manage context fields, and view audit logs.',
                                            'Owner: Can do anything, including user management.'
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
                            <ErrorMessage errors={form.formState.errors} name='role' />
                            <FormField
                                control={form.control}
                                name='projects'
                                render={({ field }) => (
                                    <FormItem className='w-full'>
                                        <FormLabel>Projects*</FormLabel>
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
                                                            <ToggleGroupItem
                                                                key={project.project_id}
                                                                className='m-0.5'
                                                                value={project.project_id.toString()}
                                                            >
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
                            <ErrorMessage errors={form.formState.errors} name='projects' />
                            {(
                                hasPermission(currentUser, Permission.UPDATE_USER) ||
                                currentUser?.user_id === user.user_id
                            ) &&
                                <Button type='submit' className='w-1/4' disabled={mutation.isPending}>Save</Button>
                            }
                        </form>
                    </Form>
                </div>
            </DialogContent>
        </Dialog>
    );
}
