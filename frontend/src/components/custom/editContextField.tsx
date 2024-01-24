import { ContextField, UpdateContextField } from "@/api";
import { apiClient, contextFieldValueTypes, getErrorMessage } from "@/utils/api";
import { zodResolver } from "@hookform/resolvers/zod";
import { ArrowLeftIcon, CheckCircledIcon, ExclamationTriangleIcon } from "@radix-ui/react-icons";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import parseHTML from 'html-react-parser';
import { useParams, useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Button } from "../ui/button";
import { Form, FormControl, FormField, FormItem, FormLabel } from "../ui/form";
import { Input } from "../ui/input";
import { Label } from "../ui/label";
import { Textarea } from "../ui/textarea";
import { useToast } from "../ui/use-toast";



const formSchema = z.object({
    name: z.string().min(1).max(128),
    description: z.string().max(256),
    enumDef: z.string().refine((def: any) => {
        try {
            JSON.parse(def);
        } catch(e) {
            return false;
        }

        return true;
    }, { message: 'Invalid JSON' }).optional()
});

export default function() {
    const params = useParams<{ projectId: string, contextFieldId: string }>();
    const router = useRouter();
    const queryClient = useQueryClient();
    const { toast } = useToast();

    const projectId = parseInt(params.projectId);
    const contextFieldId = parseInt(params.contextFieldId);

    const query = useQuery({
        queryKey: [`projects/${projectId}/context-fields/${contextFieldId}`], 
        queryFn: () => apiClient.contextFields.getContextField(contextFieldId, projectId)
    });

    const contextField: ContextField = query?.data || {} as any;
    const valueType = contextField?.value_type ? contextFieldValueTypes[contextField.value_type] : '';

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        values: {
            name: contextField?.name || '',
            description: contextField?.description || '',
            enumDef: contextField?.enum_def ? JSON.stringify(contextField.enum_def, null, 2) : undefined
        }
    });

    const mutation = useMutation({
        mutationFn: (contextField: UpdateContextField) => {
            return apiClient.contextFields.updateContextField(contextFieldId, projectId, contextField);
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
            queryClient.invalidateQueries({queryKey: [`projects/${projectId}/context-fields`]});
            queryClient.invalidateQueries({queryKey: [`projects/${projectId}/context-fields/${contextFieldId}`]});
            toast({
                variant: 'success',
                title: (
                    <div className='flex flex-row items-center'>
                        <CheckCircledIcon />
                        <p className='text-black ml-2 font-bold'>Success!</p>
                    </div>
                ),
                description: 'Context field was successfully updated.',
            })
        }
    });

    const onSubmit = (values: z.infer<typeof formSchema>) => mutation.mutate({
        name: values.name,
        description: values.description,
        enum_def: values.enumDef ? JSON.parse(values.enumDef) : null
    });
    const onBackClick = () => router.replace(`/project/${projectId}/context-fields`);

    return (
        <div className='flex flex-col w-full justify-center'>
            <div className='flex items-center justify-center mt-4 mb-8 h-10'>
                <div className='flex-1'>
                    <Button variant='ghost' className='hover:bg-accent px-2 size-9' onClick={onBackClick}>
                        <ArrowLeftIcon className='size-8 cursor-pointer' />
                    </Button>
                </div>
                <div className='flex-1'>
                    <h1 className='text-center text-lg font-bold'>Edit Context Field</h1>
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
                        <div>
                            <Label>Field Key</Label>
                            <Input className='mt-2' value={contextField?.field_key || ''} disabled />
                        </div>
                        <FormField
                            control={form.control}
                            name='description'
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Description</FormLabel>
                                    <FormControl>
                                        <Input {...field} />
                                    </FormControl>
                                </FormItem>
                            )}
                        />
                        <div>
                            <Label>Value Type</Label>
                            <Input className='mt-2' value={valueType} disabled />
                        </div>
                        {[5, 9].includes(contextField?.value_type) &&
                        <FormField
                            control={form.control}
                            name='enumDef'
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Enum Definition</FormLabel>
                                    <FormControl>
                                        <Textarea {...field} />
                                    </FormControl>
                                </FormItem>
                            )}
                        />
                        }
                        <Button type='submit' className='w-1/5' disabled={mutation.isPending}>Save</Button>
                    </form>
                </Form>
            </div>
        </div>
    )
}
