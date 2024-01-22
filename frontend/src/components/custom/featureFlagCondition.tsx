import { ContextField } from "@/api";
import { contextFieldValueTypeOperators, operators } from "@/utils/api";
import { useState } from "react";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../ui/select";
import Pill from "./pill";

export interface Condition {
    context_key: string;
    operator: number;
    value: any;
} 

interface FeatureFlagConditionProps {
    id: number
    contextFields: ContextField[]
    condition: Condition,
    onChange: (id: number, condition: Condition) => void
}

export default (props: FeatureFlagConditionProps) => {
    const getContextFieldFromKey = (key: string): ContextField => {
        return props.contextFields.find((x) => x.field_key === key) as ContextField;
    }

    const [contextField, setContextField] = useState(getContextFieldFromKey(props.condition.context_key));
    const [operator, setOperator] = useState(props.condition.operator);
    const [value, setValue] = useState(props.condition.value);
    const [stagedValue, setStagedValue] = useState('');

    const onContextKeyChange = (contextKey: string) => {
        const newContextField = getContextFieldFromKey(contextKey);
        setContextField(newContextField);

        // Reset other fields
        const newOperator = contextFieldValueTypeOperators[newContextField.value_type][0];
        setOperator(newOperator);
        setValue('');
        setStagedValue('');

        props.onChange(props.id, {
            context_key: contextKey,
            operator: newOperator,
            value: ''
        });
    }
    const onOperatorChange = (operator_: string) => {
        const newOperator = parseInt(operator_);
        setOperator(newOperator);

        // Reset other fields 
        setValue('');
        setStagedValue('');

        props.onChange(props.id, {
            context_key: contextField.field_key,
            operator: newOperator,
            value: ''
        });
    }
    const onStagedValueAdd = () => {
        let valueList: any[] = value?.length ? value.slice(0) : [];

        let castStagedValue: any = stagedValue;
        if (contextField.value_type === 2) {  // number
            // TODO: Show error if value is not a number
            castStagedValue = parseFloat(castStagedValue);
        } else if ([3, 8].includes(contextField.value_type)) {  // integer
            // TODO: Show error if value is not an integer
            castStagedValue = parseInt(castStagedValue);
        } else if ([5, 9].includes(contextField.value_type)) {  // enum
            // Enum values can either be strings or integers
            // Inspect the enum def to determine how to cast the value
            const enumDef = contextField.enum_def || {};
            if (typeof Object.values(enumDef)[0] === 'number') {
                castStagedValue = parseInt(castStagedValue);
            }
        }

        if (valueList.includes(castStagedValue)) {
            // Staged value was already added so just clear and do nothing
            setStagedValue('');
            return;
        }

        valueList.push(castStagedValue);

        setStagedValue('');
        setValue(valueList);

        props.onChange(props.id, {
            context_key: contextField.field_key,
            operator: operator,
            value: valueList
        });
    }
    const onListValueRemove = (v: string | number) => {
        const valueList = value.filter((x: string | number) => x !== v);
        setValue(valueList);

        props.onChange(props.id, {
            context_key: contextField.field_key,
            operator: operator,
            value: valueList.length ? valueList : ''
        })
    }

    const onBooleanValueChange = (v: string) => {
        setValue(v);
        props.onChange(props.id, {
            context_key: contextField.field_key,
            operator: operator,
            value: v === '1'
        });
    }
    const onStringValueChange = (v: string) => {
        setValue(v);
        props.onChange(props.id, {
            context_key: contextField.field_key,
            operator: operator,
            value: v
        });
    }
    const onNumberValueChange = (v: string) => {
        // TODO: Show error if value is not a number
        setValue(v);
        props.onChange(props.id, {
            context_key: contextField.field_key,
            operator: operator,
            value: parseFloat(v)
        });
    }
    const onIntegerValueChange = (v: string) => {
        // TODO: Show error if value is not an integer
        setValue(v);
        props.onChange(props.id, {
            context_key: contextField.field_key,
            operator: operator,
            value: parseInt(v)
        });
    }
    const onEnumValueChange = (v: string) => {
        setValue(v);

        // Enum values can either be strings or integers
        // Inspect the enum def to determine how to cast the value
        let castValue: string | number = v;
        const enumDef = contextField.enum_def || {};
        if (typeof Object.values(enumDef)[0] === 'number') {
            castValue = parseInt(v);
        }
        props.onChange(props.id, {
            context_key: contextField.field_key,
            operator: operator,
            value: castValue
        });
    }

    const contextKeySelect = (
        <Select defaultValue={contextField.field_key} value={contextField.field_key} onValueChange={onContextKeyChange}>
            <SelectTrigger>
                <SelectValue placeholder='Select a context field' />
            </SelectTrigger>
            <SelectContent>
                {props.contextFields.map((availableContextField) => (
                    <SelectItem 
                        key={availableContextField.field_key}
                        value={availableContextField.field_key}
                    >
                        {availableContextField.name}
                    </SelectItem>
                ))}
            </SelectContent>
        </Select>
    )

    const operatorSelect = (
        <Select defaultValue={operator.toString()} value={operator.toString()} onValueChange={onOperatorChange}>
            <SelectTrigger>
                <SelectValue placeholder='Select an operator'/>
            </SelectTrigger>
            <SelectContent>
                <div>
                {contextFieldValueTypeOperators[contextField.value_type].map((operator) => (
                    <SelectItem key={operator} value={operator.toString()}>{operators[operator]}</SelectItem>
                ))}
                </div>
            </SelectContent>
        </Select>
    )

    // TODO: Refactor this!
    const getInputSelect = () => {
        const enumDef = contextField.enum_def || {};
        const enumDefReversed = Object.fromEntries(Object.entries(enumDef).map(([k, v]) => [v, k]));
        if (contextField.value_type === 1) {  // string
            if ([8, 9].includes(operator)) {  // multi-value
                return (
                    <div className='flex items-center'>
                        <Input value={stagedValue} onChange={(e) => setStagedValue(e.target.value)} />
                        <Button className='ml-2' onClick={onStagedValueAdd} disabled={!stagedValue?.length}>Add</Button>
                        {(value || []).map((v: string) => (
                            <Pill key={v} label={v} onRemove={() => {onListValueRemove(v)}} />
                        ))}
                    </div>
                )
            } else {
                return (
                    <Input value={value} onChange={(e) => onStringValueChange(e.target.value)} />
                )
            }
        } else if (contextField.value_type === 2) {  // number
            if ([8, 9].includes(operator)) {  // multi-value
                return (
                    <div className='flex items-center'>
                        <Input type='number' value={stagedValue} onChange={(e) => setStagedValue(e.target.value)} />
                        <Button className='ml-2' onClick={onStagedValueAdd} disabled={!stagedValue?.length}>Add</Button>
                        {(value || []).map((v: number) => (
                            <Pill key={v} label={v} onRemove={() => {onListValueRemove(v)}} />
                        ))}
                    </div>
                )
            } else {
                return (
                    <Input type='number' value={value} onChange={(e) => onNumberValueChange(e.target.value)} />
                )
            }
        } else if (contextField.value_type === 3) {  // integer
            if ([8, 9].includes(operator)) {  // multi-value
                return (
                    <div className='flex items-center'>
                        <Input type='number' step={1} value={stagedValue} onChange={(e) => setStagedValue(e.target.value)} />
                        <Button className='ml-2' onClick={onStagedValueAdd} disabled={!stagedValue?.length}>Add</Button>
                        {(value || []).map((v: number) => (
                            <Pill key={v} label={v} onRemove={() => {onListValueRemove(v)}} />
                        ))}
                    </div>
                )
            } else {
                return (
                    <Input type='number' step={1}  value={value} onChange={(e) => onIntegerValueChange(e.target.value)} />
                )
            }
        } else if (contextField.value_type === 4) {  // boolean
            return (
                <Select value={value ? '1' : '0'} onValueChange={onBooleanValueChange}>
                    <SelectTrigger>
                        <SelectValue placeholder='Select a value' />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectItem value={'1'}>True</SelectItem>
                        <SelectItem value={'0'}>False</SelectItem>
                    </SelectContent>
                </Select>
            )
        } else if (contextField.value_type === 5) {  // enum
            if ([8, 9].includes(operator)) {  // multi-value
                return (
                    <div className='flex items-center'>
                        <Select value={stagedValue} onValueChange={setStagedValue}>
                            <SelectTrigger>
                                <SelectValue placeholder='Select a value' />
                            </SelectTrigger>
                            <SelectContent>
                                {Object.entries(enumDef).map(([enumKey, enumValue]) => (
                                    <SelectItem key={enumKey} value={enumValue.toString()}>{enumKey}</SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                        <Button className='ml-2' onClick={onStagedValueAdd} disabled={!stagedValue?.length}>Add</Button>
                        {(value || []).map((enumValue: string | number) => (
                            <Pill key={enumValue} label={enumDefReversed[enumValue]} onRemove={() => {onListValueRemove(enumValue)}} />
                        ))}
                    </div>
                )
            } else {
                return (
                    <Select value={value.toString()} onValueChange={onEnumValueChange}>
                        <SelectTrigger>
                            <SelectValue placeholder='Select a value' />
                        </SelectTrigger>
                        <SelectContent>
                            {Object.entries(enumDef).map(([enumKey, enumValue]) => (
                                <SelectItem key={enumKey} value={enumValue.toString()}>{enumKey}</SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                )
            }
        } else if (contextField.value_type === 6) {  // version
            return (
                <Input value={value} onChange={(e) => onStringValueChange(e.target.value)} />
            )
        } else if (contextField.value_type === 7) {  // string list
            if ([10, 11].includes(operator)) {  // multi-value
                return (
                    <div className='flex items-center'>
                        <Input value={stagedValue} onChange={(e) => setStagedValue(e.target.value)} />
                        <Button className='ml-2' onClick={onStagedValueAdd} disabled={!stagedValue?.length}>Add</Button>
                        {(value || []).map((v: string) => (
                            <Pill key={v} label={v} onRemove={() => {onListValueRemove(v)}} />
                        ))}
                    </div>
                )
            } else {
                return (
                    <Input value={value} onChange={(e) => onStringValueChange(e.target.value)} />
                )
            }
        } else if (contextField.value_type === 8) {  // integer list
            if ([10, 11].includes(operator)) {  // multi-value
                return (
                    <div className='flex items-center'>
                        <Input type='number' step={1} value={stagedValue} onChange={(e) => setStagedValue(e.target.value)} />
                        <Button className='ml-2' onClick={onStagedValueAdd} disabled={!stagedValue?.length}>Add</Button>
                        {(value || []).map((v: number) => (
                            <Pill key={v} label={v} onRemove={() => {onListValueRemove(v)}} />
                        ))}
                    </div>
                )
            } else {
                return (
                    <Input type='number' step={1}  value={value} onChange={(e) => onIntegerValueChange(e.target.value)} />
                )
            }
        } else if (contextField.value_type === 9) {  // enum list
            if ([10, 11].includes(operator)) {  // multi-value
                return (
                    <div className='flex items-center'>
                        <Select value={stagedValue} onValueChange={setStagedValue}>
                            <SelectTrigger>
                                <SelectValue placeholder='Select a value' />
                            </SelectTrigger>
                            <SelectContent>
                                {Object.entries(enumDef).map(([enumKey, enumValue]) => (
                                    <SelectItem key={enumKey} value={enumValue.toString()}>{enumKey}</SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                        <Button className='ml-2' onClick={onStagedValueAdd} disabled={!stagedValue?.length}>Add</Button>
                        {(value || []).map((enumValue: string | number) => (
                            <Pill key={enumValue} label={enumDefReversed[enumValue]} onRemove={() => {onListValueRemove(enumValue)}} />
                        ))}
                    </div>
                )
            } else {
                return (
                    <Select value={value} onValueChange={onEnumValueChange}>
                        <SelectTrigger>
                            <SelectValue placeholder='Select a value' />
                        </SelectTrigger>
                        <SelectContent>
                            {Object.entries(enumDef).map(([enumKey, enumValue]) => (
                                <SelectItem key={enumKey} value={enumValue.toString()}>{enumKey}</SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                )
            }
        }

        return null;
    }

    return (
        <div className='w-full flex justify-center items-center'>
            <div className='mr-4 flex-1'>
                {contextKeySelect}
            </div>
            <div className='mr-4 flex-1'>
                {operatorSelect}
            </div>
            <div className='flex-2'>
                {getInputSelect()}
            </div>
        </div>
    )
}
