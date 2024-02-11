'use client';

import { apiClient, getErrorToast, getSuccessToast } from '@/lib/api';
import { RocketIcon } from '@radix-ui/react-icons';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import Footer from '../footer';
import { Button } from '../primitives/button';
import { Input } from '../primitives/input';
import { Label } from '../primitives/label';
import { Toaster } from '../primitives/toaster';
import { useToast } from '../primitives/use-toast';

const emailRegex = new RegExp('.+@.+..+');

export default function ForgotPassword() {
    const router = useRouter();
    const [email, setEmail] = useState('');
    const { toast } = useToast();
    const onResetClick = async () => {
        if (!email?.length) {
            return;
        }
        if (!emailRegex.test(email)) {
            toast(getErrorToast('Invalid email'));
            return;
        }

        try {
            await apiClient.users.resetPassword({ email });
            toast(
                getSuccessToast(
                    'If the entered email address was valid, an email was sent containing instructions to reset your password.'
                )
            );
        } catch (e: any) {
            toast(getErrorToast(e));
        }
    };

    useEffect(() => {
        apiClient.auth
            .loginTest()
            .then(() => {
                router.push('/');
            })
            .catch(() => {});
    }, [router]);

    return (
        <div className='flex-1 flex flex-col container items-center w-3/4'>
            <header className='sticky top-0 z-50 w-full bg-accent rounded-b-sm'>
                <div className='container flex h-10 max-w-screen-2xl items-center'>
                    <div className='flex flex-1 items-center flex-shrink'>
                        <Button
                            variant='ghost'
                            className='focus-visible:bg-white p-0 mr-6'
                            onClick={() => {
                                window.location.replace('/login');
                            }}
                        >
                            <RocketIcon />
                            <h1 className='font-bold text-lg pl-2 cursor-pointer'>
                                Flagship
                            </h1>
                        </Button>
                    </div>
                </div>
            </header>
            <div className='flex flex-col flex-1 justify-center items-center size-full'>
                <div className='size-[400px]'>
                    <div className='flex justify-center'>
                        <h1 className='text-xl'>Reset password</h1>
                    </div>
                    <div className='mt-8'>
                        <Label htmlFor='email'>Email</Label>
                        <Input
                            className='mt-2'
                            type='email'
                            name='email'
                            onChange={e => setEmail(e.currentTarget.value)}
                        ></Input>
                    </div>
                    <div className='flex items-center justify-end mt-8'>
                        <Link
                            className='mr-4 text-sm hover:underline'
                            href='/login'
                        >
                            Return to login
                        </Link>
                        <Button
                            disabled={!email?.length}
                            onClick={onResetClick}
                        >
                            Reset password
                        </Button>
                    </div>
                </div>
            </div>
            <Footer />
            <Toaster />
        </div>
    );
}
