'use client';

import { ArrowLeftIcon } from '@radix-ui/react-icons';
import { useRouter } from 'next/navigation';
import { Button } from './primitives/button';

export default function Help() {
    const router = useRouter();
    const onBackClick = () => router.push('/');

    return (
        <div className='flex flex-col w-full justify-center'>
            <div className='flex items-center justify-center mt-4 h-10 mb-8'>
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
                        Help
                    </h1>
                </div>
                <div className='flex-1'></div>
            </div>
            <div className='flex flex-col w-3/4 justify-center'>
                <div className='mb-8'>
                    <h1 className='text-2xl font-bold w-full mb-4'>What is Flagship?</h1>
                    <p>Flagship is an open-source feature flag management platform.</p>
                    <p>It gives you all the tools to effectively manage your feature flags.</p>
                </div>
                <hr className='mb-8' />
                <div className='mb-8'>
                    <h1 className='text-2xl font-bold w-full mb-4'>Projects</h1>
                    <p>A project should usually map to a single system/application.</p>
                    <p>Each project has its own context fields and feature flags (explained below).</p>
                    <p>Flagship allows you to control which users have access to which projects.</p>
                    <p>Projects can be viewed and managed via the home page.</p>
                    <h1 className='text-lg font-bold w-full my-4'>Private Keys</h1>
                    <p>Each project should be assigned at least one private key.</p>
                    <p>{"A private key must be used when authenticating your client's requests to Flagship."}</p>
                    <p>Private keys are always active and can be used at any time (unless deleted), so rotating private keys is simple.</p>
                    <p>It probably goes without saying, but these should be stored securely.</p>
                </div>
                <hr className='mb-8' />
                <div className='mb-8'>
                    <h1 className='text-2xl font-bold w-full mb-4'>Context Fields</h1>
                    <p>Context fields are the fields you plan to send to Flagship when determining which feature flags are enabled for a particular user.</p>
                    <p>These fields give Flagship context about the user, environment, or whatever else suits you.</p>
                    <br />
                    <p>For example, if you wanted to control which users of your application have access to a feature flag, you could create a context field for a user ID. This user ID would then be passed to Flagship when you want to get which feature flags are enabled for a user.</p>
                    <br />
                    <p>Feature flags (explained below) can be enabled/disabled under certain conditions. These conditions reference your context fields.</p>
                    <br />
                    <p>Context fields must be assigned a value type. For example, your user ID field may be an integer.</p>
                    <p>{"Enums can also be used for your value types if you want to give more user friendly names to a field's values. For example, if your users are assigned to groups, you may pass group IDs to Flagship. However, it would be easier to manage your feature flag conditions if these IDs were mapped to human-friendly names."}</p>
                </div>
                <hr className='mb-8' />
                <div className='mb-8'>
                    <h1 className='text-2xl font-bold w-full mb-4'>Feature Flags</h1>
                    <p>{"Feature flags allows you to control access to your system's features."}</p>
                    <p>Each feature flag has its own set of conditions.</p>
                    <br />
                    <p>{'For example, you may have a feature flag "DARK_THEME" with conditions like:'}</p>
                    <p>{"`country` IS 'US' AND `user_id` IS ONE OF 1, 2, 3"}</p>
                    <br />
                    <p>{"Conditions reference the context fields you've created for your project."}</p>
                    <p>{'Different "operators" are available for each context field when used in feature flag conditions.'}</p>
                    <br />
                    <p>For example, STRING value types can be used with operatos: IS, IS NOT, IS ONE OF, IS NOT ONE OF, MATCHES</p>
                    <p>{'On the other hand, INTEGER value types can be used with operatos: IS, IS NOT, IS ONE OF, IS NOT ONE OF, <, <=, >, >='}</p>
                </div>
                <hr className='mb-8' />
                <div className='mb-8'>
                    <h1 className='text-2xl font-bold w-full mb-4'>User Management</h1>
                    <p>Users (referred to as Members) can managed within Flagship.</p>
                    <p>Each user is assigned a role and one or more projects.</p>
                    <p>The following roles are available:</p>
                    <div className='ml-10 my-2'>
                        <ul className='list-disc'>
                            <li>Owner: Can do anything, including user management</li>
                            <li>Admin: Can manage feature flags, manage context fields, and view audit logs</li>
                            <li>Standard: Can manage feature flags</li>
                            <li>Read only: Can view feature flags</li>
                        </ul>
                    </div>
                    <p>Users must be invited from within Flagship by owners.</p>
                    <p>When the app is set up, a starting owner must be added to the database. At least one owner must always exist.</p>
                </div>
                <hr className='mb-8' />
                <div className='mb-8'>
                    <h1 className='text-2xl font-bold w-full mb-4'>Audit Logs</h1>
                    <p>Audit logs help to keep track of changes/actions done by users.</p>
                    <p>System-wide audit logs can be viewed by owners.</p>
                    <p>Admins and owners can view audit logs specific to individual feature flag and context field.</p>
                </div>
            </div>
        </div>
    );
}
