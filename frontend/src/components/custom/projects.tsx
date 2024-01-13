import { Input } from '@/components/ui/input'
import NewProjectDialog from '@/components/custom/new-project-dialog'
import { MagnifyingGlassIcon } from '@radix-ui/react-icons'


export default function() {
    return (
        <div className='flex flex-col items-center justify-center'>
            <div className='w-1/2 flex items-center justify-center pb-4'>
                <MagnifyingGlassIcon className='size-5 relative left-7 top-2.5 transform -translate-y-1/2' />
                <Input className='pl-10' placeholder='Search for projects...' />
            </div>
            <div className='flex flex-col items-center rounded-sm border-accent size-5/6 border-2 p-4'>
                <p className='text-center pb-2'>Oops, you don't have any projects yet.</p>
                <p className='text-center pb-2'>Create one now!</p>
                <NewProjectDialog />
            </div>
        </div>
    )
}
