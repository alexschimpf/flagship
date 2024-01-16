import { MagnifyingGlassIcon } from '@radix-ui/react-icons'
import { Input } from '@/components/ui/input'

export interface SearchBarProps {
    className?: string
}


export default function(props: SearchBarProps) {
    return (
        <div 
            className={`flex items-center justify-center ${props.className || ''}`}
            style={{
                marginLeft: '-7px'
            }}
        >
            <MagnifyingGlassIcon className={'relative left-7 top-2 transform -translate-y-1/2'} />
            <Input className='pl-10' placeholder='Search for projects...' />
        </div>
    )
}
