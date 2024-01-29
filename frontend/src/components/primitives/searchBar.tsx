import { Input } from '@/components/primitives/input';
import { MagnifyingGlassIcon } from '@radix-ui/react-icons';
import { ChangeEventHandler } from 'react';

export interface SearchBarProps {
    placeholder: string;
    onChange?: ChangeEventHandler<HTMLInputElement>;
    className?: string;
}

export default function (props: SearchBarProps) {
    return (
        <div
            className={`flex items-center justify-center ${props.className || ''}`}
            style={{
                marginLeft: '-7px'
            }}
        >
            <MagnifyingGlassIcon
                className={'relative left-7 top-2 transform -translate-y-1/2'}
            />
            <Input className='pl-10' placeholder={props.placeholder} onChange={props.onChange} />
        </div>
    );
}
