import { ContextField } from "@/api"
import { contextFieldValueTypeOperators } from "@/utils/api"
import { Cross1Icon, PlusCircledIcon } from "@radix-ui/react-icons"
import { useEffect, useState } from "react"
import { Button } from "../ui/button"
import { Condition } from "./featureFlagCondition"
import FeatureFlagConditionGroup, { ConditionGroup } from "./featureFlagConditionGroup"

interface FeatureFlagConditionsProps {
    contextFields: ContextField[]
    conditions: ConditionGroup[]
    onChange: (conditions: ConditionGroup[]) => void
}

export default (props: FeatureFlagConditionsProps) => {
    const getDefaultCondition = (): Condition => {
        return {
            id: Math.random(),
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

    const onGroupChange = (group: ConditionGroup) => {
        const newConditions = conditions.map((g) => {
            if (g.id === group.id) {
                return group;
            }
            return g;
        }).filter((x) => x?.conditions.length)
        setConditions(newConditions);
        props.onChange(newConditions);
    };
    const onAdd = () => {
        const newGroup = {
            id: Math.random(),
            conditions: [getDefaultCondition()]
        }
        const newConditions = conditions.concat([newGroup]);
        setConditions(newConditions);
        props.onChange(newConditions);
    };
    const onRemove = (id: number) => {
        const newConditions = conditions.filter((group) => group.id !== id)
        setConditions(newConditions);
        props.onChange(newConditions);
    };

    return (
        <div className='flex flex-col w-full outline-accent border rounded-md p-2'>
            {conditions.map((group, i) => (
                <div key={group.id} className='flex flex-col'>
                    <div className='outline-accent border-4 rounded-md p-4 bg-accent'>
                        <div className='flex justify-end'>
                            <Button 
                                variant='ghost'
                                className='h-auto p-2 translate-x-3 -translate-y-3 hover:scale-125'
                                onClick={() => onRemove(group.id)}
                            >
                                <Cross1Icon className='size-3' />
                            </Button>
                        </div>
                        <div>
                            <FeatureFlagConditionGroup
                                contextFields={props.contextFields}
                                onChange={onGroupChange}
                                group={group}
                            />
                        </div>
                    </div>
                    {i < conditions.length - 1 ? 
                        <div className='flex justify-center'>
                            <p className='font-bold m-2'>OR</p>
                        </div> : null
                    }
                </div>
            ))}
            <div className='flex justify-center'>
                <Button variant='ghost' className='p-3 mt-1' onClick={onAdd}>
                    <PlusCircledIcon className='size-5' />
                </Button>
            </div>
        </div>
    )
}
