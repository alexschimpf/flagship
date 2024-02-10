'use client';

import { ContextField } from '@/api';
import { contextFieldValueTypeOperators } from '@/lib/constants';
import { Cross1Icon, PlusCircledIcon } from '@radix-ui/react-icons';
import { useState } from 'react';
import { Button } from '../primitives/button';
import FeatureFlagCondition, { Condition } from './featureFlagCondition';

export interface ConditionGroup {
    id: number;
    conditions: Condition[];
}

interface FeatureFlagConditionGroupProps {
    contextFields: ContextField[];
    group: ConditionGroup;
    onChange: (group: ConditionGroup) => void;
}

export default function FeatureFlagConditionGroup(props: FeatureFlagConditionGroupProps) {
    const [group, setGroup] = useState(props.group);

    const id = props.group.id;

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

    const onConditionChange = (condition: Condition) => {
        const newConditions = group.conditions.map(c => {
            if (c.id === condition.id) {
                return condition;
            }
            return c;
        });
        const newGroup = {
            id: id,
            conditions: newConditions
        };
        setGroup(newGroup);
        props.onChange(newGroup);
    };
    const onAdd = () => {
        const newConditions = group.conditions.concat([getDefaultCondition()]);
        const newGroup = {
            id: id,
            conditions: newConditions
        };
        setGroup(newGroup);
        props.onChange(newGroup);
    };
    const onRemove = (conditionId: number) => {
        const newConditions = group.conditions.filter(
            c => c.id !== conditionId
        );
        const newGroup = {
            id: id,
            conditions: newConditions
        };
        setGroup(newGroup);
        props.onChange(newGroup);
    };

    return (
        <div className='flex flex-col w-full'>
            {group.conditions.map((condition, i) => (
                <div key={condition.id} className='ml-1'>
                    <div className='flex items-center'>
                        <div className='flex-auto outline-accent border-4 rounded-xl bg-accent max-w-{90%}'>
                            <FeatureFlagCondition
                                contextFields={props.contextFields}
                                onChange={onConditionChange}
                                condition={condition}
                            />
                        </div>
                        <div className='flex-none'>
                            <Button
                                type='button'
                                variant='ghost'
                                className='h-fit p-1 ml-2 hover:scale-125'
                                onClick={() => onRemove(condition.id)}
                            >
                                <Cross1Icon className='size-3' />
                            </Button>
                        </div>
                    </div>
                    {i < group.conditions.length - 1 ? (
                        <div className='flex justify-center'>
                            <p className='font-bold m-2 text-sm'>AND</p>
                        </div>
                    ) : null}
                </div>
            ))}
            <div className='flex justify-center items-start'>
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
};
