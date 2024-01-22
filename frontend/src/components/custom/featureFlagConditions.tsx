import { ContextField } from "@/api"
import { contextFieldValueTypeOperators } from "@/utils/api"
import { Cross1Icon, PlusCircledIcon } from "@radix-ui/react-icons"
import { useEffect, useState } from "react"
import { Button } from "../ui/button"
import { Condition } from "./featureFlagCondition"
import FeatureFlagConditionGroup from "./featureFlagConditionGroup"

interface FeatureFlagConditionsProps {
    contextFields: ContextField[]
    conditions: Condition[][]
    onChange: (conditions: Condition[][]) => void
}

export default (props: FeatureFlagConditionsProps) => {
    const getDefaultCondition = (): Condition => {
        return {
            context_key: props.contextFields[0].field_key,
            operator: contextFieldValueTypeOperators[props.contextFields[0].value_type][0],
            value: ''
        }
    }

    const [conditions, setConditions] = useState(props.conditions);

    // TODO: Is this needed?
    useEffect(() => {
        props.onChange(conditions)
    }, [])

    const onGroupChange = (id: number, group: Condition[]) => {
        const newConditions = conditions.slice(0, id).concat([group]).concat(conditions.slice(id+1)).filter((x) => x?.length);
        setConditions(newConditions);
        props.onChange(newConditions);
    };
    const onAdd = () => {
        const newConditions = conditions.concat([[getDefaultCondition()]]);
        setConditions(newConditions);
        props.onChange(newConditions);
    };
    const onRemove = (id: number) => {
        const newConditions = conditions.slice(0, id).concat(conditions.slice(id+1));
        setConditions(newConditions);
        props.onChange(newConditions);
    };

    return (
        <div className='flex flex-col w-full'>
            {conditions.map((group, i) => (
                <div key={crypto.randomUUID()} className='flex flex-col'>
                    <div className='flex justify-end'>
                        <Button variant='ghost' className='p-4 w-12' onClick={() => onRemove(i)}>
                            <Cross1Icon />
                        </Button>
                    </div>
                    <FeatureFlagConditionGroup
                        id={i}
                        contextFields={props.contextFields}
                        onChange={onGroupChange}
                        group={group}
                    />
                    {
                        i < conditions.length - 1 ? <p>Or</p> : null
                    }
                </div>
            ))}
            <Button variant='ghost' className='p-4 w-12' onClick={onAdd}>
                <PlusCircledIcon />
            </Button>
        </div>
    )
}
