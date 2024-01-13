'use client';

import {
	Dialog,
	DialogContent,
	DialogHeader,
	DialogTitle,
	DialogTrigger,
} from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { PlusCircledIcon } from '@radix-ui/react-icons'
import { apiClient } from '@/utils/api'
import { useState } from 'react'
import * as z from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
} from '@/components/ui/form'
 

const formSchema = z.object({
    name: z.string()
});

  
export default function NewProjectDialog() {
    const [privateKey, setPrivateKey] = useState('');
    const [submitted, setSubmitted] = useState(false);

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            name: ''
        }
    });
    const onSubmit = (values: z.infer<typeof formSchema>) => {
        setSubmitted(true);
        apiClient.projects.createProject({
            name: values.name
        }).then((resp) => {
            setPrivateKey(resp.private_key);
        }).catch((resp) => {
            setSubmitted(false);
        });
    };

	return (
        <div>
            <Dialog>
                <DialogTrigger asChild>
                    <Button variant='ghost' className='hover:bg-accent px-2 size-12'>
                        <PlusCircledIcon className='size-8 cursor-pointer' />
                    </Button>
                </DialogTrigger>
                <DialogContent className='sm:max-w-[425px]'>
                    <DialogHeader>
                        <DialogTitle>New Project</DialogTitle>
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
                                                <Input disabled={!!privateKey} className='disabled:cursor-default' placeholder='' {...field} />
                                            </FormControl>
                                        </FormItem>
                                    )}
                                />
                                {!privateKey &&
                                    <Button type='submit' className='w-1/4' disabled={submitted}>Create</Button>
                                }
                            </form>
                        </Form>
                        {privateKey &&
                            <div className='mt-4'>
                                <p className='mb-4 text-red-500 text-sm text-center'>Your project's <b>secret key</b> is below. Please save it somewhere safe and accessible. It is needed to authenticate your client's requests. You <b>will not</b> see it again after this dialog closes.</p>
                                <Textarea className='bg-accent cursor-pointer resize-none text-center' value={privateKey}></Textarea>
                            </div>
                        }
                    </div>
                </DialogContent>
            </Dialog>
        </div>
    )
}
