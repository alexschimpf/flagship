import { CreateContextField } from "@/api";
import { apiClient, getErrorMessage } from "@/lib/api";
import { contextFieldValueTypes } from "@/lib/constants";
import { ErrorMessage } from "@hookform/error-message";
import { zodResolver } from "@hookform/resolvers/zod";
import { ArrowLeftIcon, CheckCircledIcon, ExclamationTriangleIcon } from "@radix-ui/react-icons";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import parseHTML from 'html-react-parser';
import { useParams, useRouter } from "next/navigation";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Button } from "../primitives/button";
import CustomTooltip from "../primitives/customTooltip";
import { Form, FormControl, FormField, FormItem, FormLabel } from "../primitives/form";
import { Input } from "../primitives/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../primitives/select";
import { Textarea } from "../primitives/textarea";
import { useToast } from "../primitives/use-toast";



const formSchema = z.object({
    name: z.string().min(1).max(128),
    fieldKey: z.string().min(1).max(64),
    valueType: z.string().min(1, {
        message: 'Please select a value type'
    }),
    description: z.string().max(256).optional(),
    enumDef: z.string().refine((def: any) => {
        try {
            JSON.parse(def);
        } catch (e) {
            return false;
        }

        return true;
    }, { message: 'Invalid JSON' }).optional()
});

export default function () {
    const params = useParams<{ projectId: string; }>();
    const router = useRouter();
    const queryClient = useQueryClient();
    const { toast } = useToast();

    // TODO: Figure out hwo to do with with the form
    const [valueType, setValueType] = useState(1);

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            name: '',
            fieldKey: '',
            description: ''
        }
    });

    const projectId = parseInt(params.projectId);

    const mutation = useMutation({
        mutationFn: (contextField: CreateContextField) => {
            return apiClient.contextFields.createContextField(projectId, contextField);
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
            queryClient.invalidateQueries({ queryKey: [`projects/${projectId}/context-fields`] });
            toast({
                variant: 'success',
                title: (
                    <div className='flex flex-row items-center'>
                        <CheckCircledIcon />
                        <p className='text-black ml-2 font-bold'>Success!</p>
                    </div>
                ),
                description: 'Context field was successfully created.',
            });
            router.replace(`/project/${projectId}/context-fields`);
        }
    });

    const onSubmit = (values: z.infer<typeof formSchema>) => mutation.mutate({
        name: values.name,
        field_key: values.fieldKey,
        value_type: parseInt(values.valueType),
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
                    <h1 className='text-center text-lg font-bold'>New Context Field</h1>
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
                            name='fieldKey'
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Field Key*</FormLabel>
                                    <CustomTooltip text={[
                                        'This is the exact key which will be supplied in your context.',
                                        'This cannot be changed after the context field is created.'
                                    ]} />
                                    <FormControl>
                                        <Input {...field} />
                                    </FormControl>
                                </FormItem>
                            )}
                        />
                        <ErrorMessage errors={form.formState.errors} name='fieldKey' />
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
                        <ErrorMessage errors={form.formState.errors} name='description' />
                        <FormField
                            control={form.control}
                            name='valueType'
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Value Type*</FormLabel>
                                    <Select
                                        onValueChange={(v) => {
                                            // Clear enumDef if value type is non-enum
                                            if (![5, 9].includes(parseInt(v))) {
                                                form.resetField('enumDef');
                                            }
                                            setValueType(parseInt(v));
                                            field.onChange(v);
                                        }}
                                        defaultValue={field.value}
                                    >
                                        <FormControl>
                                            <SelectTrigger>
                                                <SelectValue placeholder='Select a value type' />
                                            </SelectTrigger>
                                        </FormControl>
                                        <SelectContent>
                                            {Object.entries(contextFieldValueTypes).map(([value, label]) => (
                                                <SelectItem value={value}>{label}</SelectItem>
                                            ))}
                                        </SelectContent>
                                    </Select>
                                </FormItem>
                            )}
                        />
                        <ErrorMessage errors={form.formState.errors} name='valueType' />
                        {[5, 9].includes(valueType) &&
                            <FormField
                                control={form.control}
                                name='enumDef'
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Enum Definition*</FormLabel>
                                        <CustomTooltip text={[
                                            'For context fields with an enum value type, you must define the enum with JSON.',
                                            'The JSON must have string keys and either integer or string values.',
                                            'The keys will be used as display names in feature flag conditions.',
                                            'The values should match what your actual context values will look like for this field.'
                                        ]} />
                                        <FormControl>
                                            <Textarea {...field} />
                                        </FormControl>
                                    </FormItem>
                                )}
                            />
                        }
                        <ErrorMessage errors={form.formState.errors} name='enumDef' />
                        <div className='flex justify-end'>
                            <Button type='submit' className='w-1/5 mt-8' disabled={mutation.isPending}>Create</Button>
                        </div>
                    </form>
                </Form>
            </div>
        </div>
    );
}
