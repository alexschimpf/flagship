import { Cross1Icon } from '@radix-ui/react-icons';
import { Button } from './button';
import { Label } from './label';

interface PillProps {
    label: string | number;
    onRemove: () => void;
}

export default function Pill(props: PillProps) {
    return (
        <div className='flex justify-center items-center bg-background rounded-3xl p-2 w-fit m-1'>
            <Label className='text-[12px] font-bold'>{props.label}</Label>
            <Button
                type='button'
                variant='ghost'
                className='ml-1 rounded-3xl p-1 bg-accent translate-y-[1px] h-fit'
            >
                <Cross1Icon
                    className='cursor-pointer scale-75 hover:scale-90'
                    onClick={props.onRemove}
                />
            </Button>
        </div>
    );
}
