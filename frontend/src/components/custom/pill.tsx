import { Cross1Icon } from "@radix-ui/react-icons"
import { Button } from "../ui/button"
import { Label } from "../ui/label"

interface PillProps {
    label: string | number
    onRemove: () => void
}

export default (props: PillProps) => {
    return (
        <div className='flex justify-center items-center bg-accent rounded-3xl px-4'>
            <Label>{props.label}</Label>
            <Button variant='ghost' className='ml-1.5 rounded-3xl p-0 bg-accent'>
                <Cross1Icon className='cursor-pointer scale-75' onClick={props.onRemove} />
            </Button>
        </div>
    )
}
