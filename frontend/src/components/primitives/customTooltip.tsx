import { InfoCircledIcon } from '@radix-ui/react-icons';
import {
    Tooltip,
    TooltipContent,
    TooltipProvider,
    TooltipTrigger
} from './tooltip';

interface TooltipProps {
    text: string[] | readonly string[];
    trigger?: any;
}

export default function CustomTooltip(props: TooltipProps) {
    return (
        <TooltipProvider>
            <Tooltip>
                <TooltipTrigger type='button'>
                    {props.trigger || <InfoCircledIcon className='ml-1' />}
                </TooltipTrigger>
                <TooltipContent className='m-0 p-0 bg-accent border'>
                    <div className='bg-accent m-2 p-1 rounded-md'>
                        {props.text.map((line, i) => (
                            <p key={i}>{line}</p>
                        ))}
                    </div>
                </TooltipContent>
            </Tooltip>
        </TooltipProvider>
    );
}
