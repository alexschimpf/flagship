'use client';

import { ContextField } from '@/api';
import { contextFieldValueTypeOperators } from '@/lib/constants';
import { Cross1Icon, PlusCircledIcon } from '@radix-ui/react-icons';
import { useEffect, useState } from 'react';
import { Button } from '../primitives/button';
import { Condition } from './featureFlagCondition';
import FeatureFlagConditionGroup, {
    ConditionGroup
} from './featureFlagConditionGroup';

interface FeatureFlagConditionsProps {
    contextFields: ContextField[];
    conditions: ConditionGroup[];
    onChange: (conditions: ConditionGroup[]) => void;
}

export default function FeatureFlagConditions(
    props: FeatureFlagConditionsProps
) {
    const getDefaultCondition = (): Condition => {
        return {
            id: Math.random(),
            context_key: props.contextFields[0].field_key,
            operator:
                contextFieldValueTypeOperators[
                    props.contextFields[0].value_type
                ][0],
            value: ''
        };
    };

    const [conditions, setConditions] = useState(props.conditions);

    useEffect(() => {
        props.onChange(conditions);
    }, [props, conditions]);

    const onGroupChange = (group: ConditionGroup) => {
        const newConditions = conditions
            .map(g => {
                if (g.id === group.id) {
                    return group;
                }
                return g;
            })
            .filter(x => x?.conditions.length);
        setConditions(newConditions);
        props.onChange(newConditions);
    };
    const onAdd = () => {
        const newGroup = {
            id: Math.random(),
            conditions: [getDefaultCondition()]
        };
        const newConditions = conditions.concat([newGroup]);
        setConditions(newConditions);
        props.onChange(newConditions);
    };
    const onRemove = (id: number) => {
        const newConditions = conditions.filter(group => group.id !== id);
        setConditions(newConditions);
        props.onChange(newConditions);
    };

    return (
        <div className='flex flex-col w-full'>
            {conditions.map((group, i) => (
                <div key={group.id} className='flex flex-col'>
                    <div className='outline-accent border rounded-md p-2'>
                        <div className='flex justify-end'>
                            <Button
                                type='button'
                                variant='ghost'
                                className='h-auto p-1 hover:scale-125'
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
                    {i < conditions.length - 1 ? (
                        <div className='flex justify-center'>
                            <p className='font-bold m-2 text-sm'>OR</p>
                        </div>
                    ) : null}
                </div>
            ))}
            <div className='flex justify-center'>
                <Button
                    type='button'
                    variant='ghost'
                    className='p-1 size-[32px] mt-2 hover:scale-110'
                    onClick={onAdd}
                >
                    <PlusCircledIcon className='size-5' />
                </Button>
            </div>
        </div>
    );
}
