import { ContextField } from "@/api"
import { contextFieldValueTypeOperators } from "@/utils/api"
import { Cross1Icon, PlusCircledIcon } from "@radix-ui/react-icons"
import { useState } from "react"
import { Button } from "../ui/button"
import FeatureFlagCondition, { Condition } from "./featureFlagCondition"

interface FeatureFlagConditionGroupProps {
    id: number
    contextFields: ContextField[]
    group: Condition[]
    onChange: (id: number, group: Condition[]) => void
}

export default (props: FeatureFlagConditionGroupProps) => {
    const getDefaultCondition = (): Condition => {
        return {
            context_key: props.contextFields[0].field_key,
            operator: contextFieldValueTypeOperators[props.contextFields[0].value_type][0],
            value: ''
        }
    }

    const [group, setGroup] = useState(props.group);

    const onConditionChange = (id: number, condition: Condition) => {
        const newGroup = group.slice(0, id).concat([condition]).concat(group.slice(id+1));
        setGroup(newGroup);
        props.onChange(props.id, newGroup);
    };
    const onAdd = () => {
        const newGroup = group.concat([getDefaultCondition()]);
        setGroup(newGroup);
        props.onChange(props.id, newGroup);
    };
    const onRemove = (id: number) => {
        const newGroup = group.slice(0, id).concat(group.slice(id+1));
        setGroup(newGroup);
        props.onChange(props.id, newGroup);
    }

    return (
        <div className='flex flex-col w-full'>
            {group.map((condition, i) => (
                <div key={i} className='flex'>
                    <FeatureFlagCondition
                        id={i}
                        contextFields={props.contextFields}
                        onChange={onConditionChange}
                        condition={condition}
                    />
                    {
                        i < group.length - 1 ? <p>And</p> : null
                    }
                    <Button variant='ghost' className='p-4 w-12' onClick={() => onRemove(i)}>
                        <Cross1Icon />
                    </Button>
                </div>
            ))}
            <Button variant='ghost' className='p-4 w-12' onClick={onAdd}>
                <PlusCircledIcon />
            </Button>
        </div>
    )
}
