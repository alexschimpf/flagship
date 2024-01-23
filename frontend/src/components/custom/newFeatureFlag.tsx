import { CreateOrUpdateFeatureFlag } from "@/api";
import { apiClient, getErrorMessage } from "@/utils/api";
import { zodResolver } from "@hookform/resolvers/zod";
import { ArrowLeftIcon, CheckCircledIcon, ExclamationTriangleIcon } from "@radix-ui/react-icons";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import parseHTML from 'html-react-parser';
import { useParams, useRouter } from "next/navigation";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Button } from "../ui/button";
import { Form, FormControl, FormField, FormItem, FormLabel } from "../ui/form";
import { Input } from "../ui/input";
import { Switch } from '../ui/switch';
import { useToast } from "../ui/use-toast";
import { ConditionGroup } from "./featureFlagConditionGroup";
import FeatureFlagConditions from "./featureFlagConditions";



const formSchema = z.object({
    name: z.string().min(1).max(128),
    description: z.string().max(256),
    enabled: z.boolean()
});

// TODO: Show spinner while context fields are loading
export default function() {
    const params = useParams<{ projectId: string }>();
    const router = useRouter();
    const queryClient = useQueryClient();
    const { toast } = useToast();
    const projectId = parseInt(params.projectId);
    const contextFieldsQuery = useQuery({
        queryKey: [`/projects/${projectId}/context-fields`], 
        queryFn: () =>  apiClient.contextFields.getContextFields(projectId)

    });
    const contextFields = contextFieldsQuery?.data?.items || [];
    const [conditions, setConditions] = useState<ConditionGroup[]>([]);
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            name: '',
            description: '',
            enabled: false
        },
        shouldFocusError: false  // TODO: FInd better solution
    });

    const mutation = useMutation({
        mutationFn: (featureFlag: CreateOrUpdateFeatureFlag) => {
            return apiClient.featureFlags.createFeatureFlag(projectId, featureFlag);
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
            queryClient.invalidateQueries({queryKey: [`projects/${projectId}/feature-flags`]});
            toast({
                variant: 'success',
                title: (
                    <div className='flex flex-row items-center'>
                        <CheckCircledIcon />
                        <p className='text-black ml-2 font-bold'>Success!</p>
                    </div>
                ),
                description: 'Feature flag was successfully created.',
            })
            router.replace(`/project/${projectId}/feature-flags`);
        }
    });

    const getProperConditions = (c: ConditionGroup[]) => {
        // Basically just stripping out ids
        const properConditions: any[] = [];
        for (const group of c) {
            properConditions.push(group.conditions.map((condition) => ({
                context_key: condition.context_key,
                operator: condition.operator,
                value: condition.value
            })));
        }
        return properConditions;
    }

    const onSubmit = (values: z.infer<typeof formSchema>) => {
        mutation.mutate({
            name: values.name,
            description: values.description,
            enabled: values.enabled,
            conditions: getProperConditions(conditions)
        });
    }
    const onBackClick = () => router.replace(`/project/${projectId}/feature-flags`);
    const onConditionsChange = (c: ConditionGroup[]) => {
        console.log(JSON.stringify(getProperConditions(c)));
        setConditions(c);
    }

    return (
        <div className='flex flex-col w-full justify-center'>
            <div className='flex items-center justify-center mt-4 mb-8 h-10'>
                <div className='flex-1'>
                    <Button variant='ghost' className='hover:bg-accent px-2 size-9' onClick={onBackClick}>
                        <ArrowLeftIcon className='size-8 cursor-pointer' />
                    </Button>
                </div>
                <div className='flex-1'>
                    <h1 className='text-center text-lg font-bold'>New Feature Flag</h1>
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
                        <FormField
                            control={form.control}
                            name='enabled'
                            render={({ field }) => (
                                <FormItem>
                                    <div className='flex flex-col'>
                                        <FormLabel className='mb-3'>Enabled</FormLabel>
                                        <FormControl>
                                            <Switch checked={field.value} onCheckedChange={field.onChange} />
                                        </FormControl>
                                    </div>
                                </FormItem>
                            )}
                        />
                        {contextFields?.length > 0 &&
                            <div className='w-full'>
                                <FormLabel>Conditions</FormLabel>
                                <FeatureFlagConditions contextFields={contextFields} conditions={conditions} onChange={onConditionsChange} />
                            </div>
                        }
                        <Button type='submit' className='w-1/5' disabled={mutation.isPending}>Create</Button>
                    </form>
                </Form>
            </div>
        </div>
    )
}
