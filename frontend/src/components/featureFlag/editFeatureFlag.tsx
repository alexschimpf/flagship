'use client';

import { CreateOrUpdateFeatureFlag, FeatureFlag } from '@/api';
import { UserContext } from '@/context/userContext';
import { apiClient, getErrorToast, getSuccessToast } from '@/lib/api';
import { Permission, hasPermission } from '@/lib/permissions';
import { ErrorMessage } from '@hookform/error-message';
import { zodResolver } from '@hookform/resolvers/zod';
import { ArrowLeftIcon } from '@radix-ui/react-icons';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Loader2 } from 'lucide-react';
import { useParams, useRouter } from 'next/navigation';
import { useContext, useState } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { Button } from '../primitives/button';
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel
} from '../primitives/form';
import { Input } from '../primitives/input';
import { Switch } from '../primitives/switch';
import { useToast } from '../primitives/use-toast';
import { ConditionGroup } from './featureFlagConditionGroup';
import FeatureFlagConditions from './featureFlagConditions';

const formSchema = z.object({
    name: z.string().min(1).max(128),
    description: z.string().max(256).optional(),
    enabled: z.boolean()
});

// TODO: Show spinner while context fields are loading
export default function EditFeatureFlag() {
    const params = useParams<{ projectId: string; featureFlagId: string }>();
    const currentUser = useContext(UserContext);
    const router = useRouter();
    const queryClient = useQueryClient();
    const { toast } = useToast();
    const projectId = parseInt(params.projectId);
    const featureFlagId = parseInt(params.featureFlagId);
    const contextFieldsQuery = useQuery({
        queryKey: [`/projects/${projectId}/context-fields`],
        queryFn: () => apiClient.contextFields.getContextFields(projectId)
    });
    const featureFlagQuery = useQuery({
        queryKey: [`/projects/${projectId}/feature-flags/${featureFlagId}`],
        queryFn: () => {
            const promise = apiClient.featureFlags.getFeatureFlag(
                featureFlagId,
                projectId
            );
            promise.then((data: FeatureFlag) => {
                const conditions = data.conditions;
                const conditionsWithIds: any[] = [];
                for (const group of conditions) {
                    const groupWithId: any = {
                        id: Math.random(),
                        conditions: []
                    };
                    for (const condition of group) {
                        groupWithId.conditions.push({
                            id: Math.random(),
                            ...condition
                        });
                    }
                    conditionsWithIds.push(groupWithId);
                }
                setConditions(conditionsWithIds);
            });
            return promise;
        }
    });
    const featureFlag: FeatureFlag = featureFlagQuery?.data || ({} as any);
    const contextFields = contextFieldsQuery?.data?.items || [];
    const [conditions, setConditions] = useState<ConditionGroup[] | undefined>(
        undefined
    );
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        values: {
            name: featureFlag?.name || '',
            description: featureFlag?.description || '',
            enabled: featureFlag?.enabled || false
        },
        shouldFocusError: false // TODO: FInd better solution
    });

    const mutation = useMutation({
        mutationFn: (featureFlag: CreateOrUpdateFeatureFlag) => {
            return apiClient.featureFlags.updateFeatureFlag(
                featureFlagId,
                projectId,
                featureFlag
            );
        },
        onError: error => {
            toast(getErrorToast(error));
        },
        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: [`projects/${projectId}/feature-flags`]
            });
            toast(getSuccessToast('Feature flag was successfully updated.'));
            router.push(`/project/${projectId}/feature-flags`);
        }
    });

    const getProperConditions = (c: ConditionGroup[]) => {
        // Basically just stripping out ids
        const properConditions: any[] = [];
        for (const group of c) {
            properConditions.push(
                group.conditions.map(condition => ({
                    context_key: condition.context_key,
                    operator: condition.operator,
                    value: condition.value
                }))
            );
        }
        return properConditions;
    };

    const onSubmit = (values: z.infer<typeof formSchema>) => {
        mutation.mutate({
            name: values.name,
            description: values.description,
            enabled: values.enabled,
            conditions: getProperConditions(conditions as any)
        });
    };
    const onBackClick = () =>
        router.push(`/project/${projectId}/feature-flags`);
    const onConditionsChange = (c: ConditionGroup[]) => {
        setConditions(c);
    };

    const isFetching =
        featureFlagQuery.isFetching || contextFieldsQuery.isFetching;

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
                <div className='flex'>
                    <h1 className='text-center text-lg font-bold mt-2'>
                        Edit Feature Flag
                    </h1>
                </div>
                <div className='flex-1'></div>
            </div>
            {!isFetching && (
                <div className='w-full flex items-center justify-center'>
                    <Form {...form}>
                        <form
                            onSubmit={form.handleSubmit(onSubmit)}
                            className='space-y-4 flex flex-col w-full items-center'
                        >
                            <div className='w-1/2'>
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
                                <FormField
                                    control={form.control}
                                    name='description'
                                    render={({ field }) => (
                                        <FormItem className='mt-4'>
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
                                <FormField
                                    control={form.control}
                                    name='enabled'
                                    render={({ field }) => (
                                        <FormItem>
                                            <div className='flex flex-col mt-4'>
                                                <FormLabel className='mb-3'>
                                                    Enabled
                                                </FormLabel>
                                                <FormControl>
                                                    <Switch
                                                        checked={field.value}
                                                        onCheckedChange={
                                                            field.onChange
                                                        }
                                                    />
                                                </FormControl>
                                            </div>
                                        </FormItem>
                                    )}
                                />
                            </div>
                            {contextFields?.length > 0 &&
                                conditions !== undefined && (
                                    <div className='w-3/5'>
                                        <div className='w-full flex justify-center'>
                                            <FormLabel className='text-center'>
                                                Conditions
                                            </FormLabel>
                                        </div>
                                        <div className='mt-4'>
                                            <FeatureFlagConditions
                                                contextFields={contextFields}
                                                conditions={conditions}
                                                onChange={onConditionsChange}
                                            />
                                        </div>
                                    </div>
                                )}
                            {hasPermission(
                                currentUser,
                                Permission.UPDATE_FEATURE_FLAG
                            ) && (
                                <div className='w-1/2 flex justify-end'>
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
            {isFetching && (
                <div className='absolute top-[calc(50%-41px)] left-1/2'>
                    <Loader2 className='animate-spin' size={48} />
                </div>
            )}
        </div>
    );
}
