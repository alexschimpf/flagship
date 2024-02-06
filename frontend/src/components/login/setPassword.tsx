import { apiClient } from "@/lib/api";
import { RocketIcon } from "@radix-ui/react-icons";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import Footer from "../footer";
import { Button } from "../primitives/button";
import { Input } from "../primitives/input";
import { Label } from "../primitives/label";

export default function SetPassword() {
    const router = useRouter();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [passwordRepeat, setPasswordRepeat] = useState('');
    const params = useSearchParams();
    const error = params.get('error') || '';
    const token = params.get('token') || 'none';

    useEffect(() => {
        apiClient.auth.loginTest().then(() => {
            router.push('/');
        }).catch(() => { });
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
                                window.location.replace('http://localhost:3000/login');
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
                <form className='size-[400px]' method='POST' action='http://localhost:8000/users/password/set'>
                    <div className='flex flex-col justify-center items-center'>
                        <h1 className='text-xl'>Set password</h1>
                    </div>
                    <div className='mt-8'>
                        <Label htmlFor='email'>Email</Label>
                        <Input className='mt-2' type='email' name='email' onChange={e => setEmail(e.currentTarget.value)}></Input>
                    </div>
                    <div className='mt-4'>
                        <Label htmlFor='password'>Password</Label>
                        <Input className='mt-2' type='password' name='password' onChange={e => setPassword(e.currentTarget.value)}></Input>
                    </div>
                    <div className='mt-4'>
                        <Label htmlFor='password-repeat'>Repeat Password</Label>
                        <Input className='mt-2' type='password' name='password_repeat' onChange={e => setPasswordRepeat(e.currentTarget.value)}></Input>
                    </div>
                    <Input type='hidden' name='token' value={token} />
                    {error.length > 0 &&
                        <div className='flex justify-center mt-8'>
                            <p className='text-sm text-red-600 p-3 rounded-md'>{error}</p>
                        </div>
                    }
                    <div className='flex items-center justify-end mt-8'>
                        <Link className='mr-4 text-sm hover:underline' href='/login'>Go to login</Link>
                        <Button disabled={!email || !password || !passwordRepeat}>Set Password</Button>
                    </div>
                </form>
            </div>
            <Footer />
        </div>
    );
};
