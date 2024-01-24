import { UpdateUser, User } from "@/api";
import { apiClient, getErrorMessage, userRoles } from "@/utils/api";
import { zodResolver } from "@hookform/resolvers/zod";
import { ArrowLeftIcon, CheckCircledIcon, ExclamationTriangleIcon } from "@radix-ui/react-icons";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import parseHTML from 'html-react-parser';
import { Loader2 } from "lucide-react";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Button } from "../ui/button";
import { Form, FormControl, FormField, FormItem, FormLabel } from "../ui/form";
import { Input } from "../ui/input";
import { ScrollArea } from "../ui/scroll-area";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../ui/select";
import { ToggleGroup, ToggleGroupItem } from "../ui/toggle-group";
import { useToast } from "../ui/use-toast";

const formSchema = z.object({
    name: z.string().min(1).max(128),
    role: z.string().min(1),
    projects: z.array(z.string()).min(1)
});

export default function() {
    const router = useRouter();
    const queryClient = useQueryClient();
    const { toast } = useToast();

    const userQuery = useQuery({
        queryKey: ['me'], 
        queryFn: () => apiClient.users.getMe()
    });
    const projectsQuery = useQuery({
        queryKey: ['projects'], 
        queryFn: () => apiClient.projects.getProjects()
    });

    const user = userQuery?.data;
    const projects = projectsQuery.data?.items || [];

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        values: {
            name: user?.name || '',
            role: user?.role?.toString() || '',
            projects: user?.projects.map((projectId) => projectId.toString()) || []
        }
    });

    const resetPasswordMutation = useMutation({
        mutationFn: () => {
            return apiClient.users.resetPassword({
                email: user?.email as string
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
                description: 'Password reset email was sent.',
            })
        }
    });

    const mutation = useMutation({
        mutationFn: (userRequest: UpdateUser) => {
            // TODO: Probably don't need this after testing
            const availableProjectIds = projects.map((project) => project.project_id);
            userRequest.projects = userRequest.projects.filter((projectId) => availableProjectIds.includes(projectId))
            return apiClient.users.updateUser(user?.user_id as number, userRequest);
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
        onSuccess: (data: User) => {
            queryClient.invalidateQueries({queryKey: ['me']});
            queryClient.invalidateQueries({queryKey: [`users`]});
            
            sessionStorage.setItem('current-user', JSON.stringify(data));

            toast({
                variant: 'success',
                title: (
                    <div className='flex flex-row items-center'>
                        <CheckCircledIcon />
                        <p className='text-black ml-2 font-bold'>Success!</p>
                    </div>
                ),
                description: 'Your account was successfully updated.',
            })
        }
    });

    const onSubmit = (values: z.infer<typeof formSchema>) => mutation.mutate({
        name: values.name,
        role: parseInt(values.role),
        projects: values.projects.map((projectId) => parseInt(projectId))
    });
    const onResetPasswordClick = () => resetPasswordMutation.mutate()
    const onBackClick = () => router.replace('/');

    return (
        <div className='flex flex-col w-full justify-center'>
            <div className='flex items-center justify-center mt-4 mb-8 h-10'>
                <div className='flex-1'>
                    <Button variant='ghost' className='hover:bg-accent px-2 size-9' onClick={onBackClick}>
                        <ArrowLeftIcon className='size-8 cursor-pointer' />
                    </Button>
                </div>
                <div className='flex-1'>
                    <h1 className='text-center text-lg font-bold'>My Account</h1>
                </div>
                <div className='flex-1'>
                </div>
            </div>
            <div className='w-full flex items-center justify-center'>
                <Form {...form}>
                    <form onSubmit={form.handleSubmit(onSubmit)} className='space-y-4 flex flex-col w-1/2'>
                        <FormField
                            control={form.control}
                            name='name'
                            render={({ field }) => (
                                <FormItem>
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
                                    <Select onValueChange={field.onChange} defaultValue={field.value} value={field.value}>
                                        <FormControl>
                                            <SelectTrigger>
                                                <SelectValue placeholder='Select a role' />
                                            </SelectTrigger>
                                        </FormControl>
                                        <SelectContent>
                                        {Object.entries(userRoles).map(([roleId, roleName]) => (
                                            <SelectItem value={roleId}>{roleName}</SelectItem>
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
                                        <ToggleGroup type='multiple' onValueChange={field.onChange} value={field.value}>
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
                        <div className='flex justify-end'>
                            <Button 
                                type='button'
                                className='w-1/5 mr-2'
                                disabled={resetPasswordMutation.isPending}
                                onClick={() => onResetPasswordClick()}
                            >
                                Reset Password
                            </Button>
                            <Button type='submit' className='w-1/5' disabled={mutation.isPending}>
                                Save
                            </Button>
                        </div>
                    </form>
                </Form>
            </div>
        </div>
    )
}
