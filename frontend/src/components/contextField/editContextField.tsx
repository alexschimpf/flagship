import { ContextField, UpdateContextField } from '@/api';
import { UserContext } from '@/context/userContext';
import { apiClient, getErrorToast, getSuccessToast } from '@/lib/api';
import { contextFieldValueTypes } from '@/lib/constants';
import { Permission, hasPermission } from '@/lib/permissions';
import { ErrorMessage } from '@hookform/error-message';
import { zodResolver } from '@hookform/resolvers/zod';
import { ArrowLeftIcon } from '@radix-ui/react-icons';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Loader2 } from 'lucide-react';
import { useParams, useRouter } from 'next/navigation';
import { useContext } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { Button } from '../primitives/button';
import CustomTooltip from '../primitives/customTooltip';
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel
} from '../primitives/form';
import { Input } from '../primitives/input';
import { Label } from '../primitives/label';
import { Textarea } from '../primitives/textarea';
import { useToast } from '../primitives/use-toast';

const formSchema = z.object({
    name: z.string().min(1).max(128),
    description: z.string().max(256).optional(),
    enumDef: z
        .string()
        .refine(
            (def: any) => {
                try {
                    JSON.parse(def);
                } catch (e) {
                    return false;
                }

                return true;
            },
            { message: 'Invalid JSON' }
        )
        .optional()
});

export default function () {
    const currentUser = useContext(UserContext);
    const params = useParams<{ projectId: string; contextFieldId: string; }>();
    const router = useRouter();
    const queryClient = useQueryClient();
    const { toast } = useToast();

    const projectId = parseInt(params.projectId);
    const contextFieldId = parseInt(params.contextFieldId);

    const query = useQuery({
        queryKey: [`projects/${projectId}/context-fields/${contextFieldId}`],
        queryFn: () =>
            apiClient.contextFields.getContextField(contextFieldId, projectId)
    });

    const contextField: ContextField = query?.data || ({} as any);
    const valueType = contextField?.value_type
        ? contextFieldValueTypes[contextField.value_type]
        : '';

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        values: {
            name: contextField?.name || '',
            description: contextField?.description || '',
            enumDef: contextField?.enum_def
                ? JSON.stringify(contextField.enum_def, null, 2)
                : undefined
        }
    });

    const mutation = useMutation({
        mutationFn: (contextField: UpdateContextField) => {
            return apiClient.contextFields.updateContextField(
                contextFieldId,
                projectId,
                contextField
            );
        },
        onError: error => {
            toast(getErrorToast(error));
        },
        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: [`projects/${projectId}/context-fields`]
            });
            queryClient.invalidateQueries({
                queryKey: [
                    `projects/${projectId}/context-fields/${contextFieldId}`
                ]
            });
            toast(getSuccessToast('Context field was successfully updated.'));
        }
    });

    const onSubmit = (values: z.infer<typeof formSchema>) =>
        mutation.mutate({
            name: values.name,
            description: values.description,
            enum_def: values.enumDef ? JSON.parse(values.enumDef) : null
        });
    const onBackClick = () =>
        router.push(`/project/${projectId}/context-fields`);

    return (
        <div className='flex flex-col w-full justify-center'>
            <div className='flex items-center justify-center mt-4 mb-8 h-10'>
                <div className='flex-1'>
                    <Button
                        variant='ghost'
                        className='hover:bg-accent px-2 size-9'
                        onClick={onBackClick}
                    >
                        <ArrowLeftIcon className='size-8 cursor-pointer' />
                    </Button>
                </div>
                <div className='flex-1'>
                    <h1 className='text-center text-lg font-bold'>
                        Edit Context Field
                    </h1>
                </div>
                <div className='flex-1'></div>
            </div>
            {!query.isFetching && (
                <div className='w-full flex items-center justify-center'>
                    <Form {...form}>
                        <form
                            onSubmit={form.handleSubmit(onSubmit)}
                            className='space-y-4 flex flex-col w-1/2'
                        >
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
                            <ErrorMessage
                                errors={form.formState.errors}
                                name='name'
                            />
                            <div>
                                <Label>Field Key</Label>
                                <Input
                                    className='mt-2'
                                    value={contextField?.field_key || ''}
                                    disabled
                                />
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
                            <ErrorMessage
                                errors={form.formState.errors}
                                name='description'
                            />
                            <div>
                                <Label>Value Type</Label>
                                <Input
                                    className='mt-2'
                                    value={valueType}
                                    disabled
                                />
                            </div>
                            {[5, 9].includes(contextField?.value_type) && (
                                <FormField
                                    control={form.control}
                                    name='enumDef'
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>
                                                Enum Definition*
                                            </FormLabel>
                                            <CustomTooltip
                                                text={[
                                                    'For context fields with an enum value type, you must define the enum with JSON.',
                                                    'The JSON must have string keys and either integer or string values.',
                                                    'The keys will be used as display names in feature flag conditions.',
                                                    'The values should match what your actual context values will look like for this field.'
                                                ]}
                                            />
                                            <FormControl>
                                                <Textarea {...field} />
                                            </FormControl>
                                        </FormItem>
                                    )}
                                />
                            )}
                            <ErrorMessage
                                errors={form.formState.errors}
                                name='enumDef'
                            />
                            {hasPermission(
                                currentUser,
                                Permission.UPDATE_CONTEXT_FIELD
                            ) && (
                                    <div className='flex justify-end'>
                                        <Button
                                            type='submit'
                                            className='w-1/5 m-8'
                                            disabled={mutation.isPending}
                                        >
                                            Save
                                        </Button>
                                    </div>
                                )}
                        </form>
                    </Form>
                </div>
            )}
            {query.isFetching && (
                <div className='absolute top-[calc(50%-41px)] left-1/2'>
                    <Loader2 className='animate-spin' size={48} />
                </div>
            )}
        </div>
    );
}
