import { ContextValueType, Operator, UserRole, UserStatus } from "@/api";

const reverseEnum = (obj: any, valueFn?: (v: any) => any): any => {
    const reversedEntries =
        Object.entries(
            obj
        ).filter(
            ([k, v]) => isNaN(Number(k))
        ).map(
            ([k, v]) => [v, valueFn ? valueFn(k) : k]
        );
    return Object.fromEntries(reversedEntries);
};

const capitalize = (s: string) => {
    s = s.replaceAll('_', ' ');
    return s.split(' ').map((w) => w.charAt(0).toUpperCase() + w.substring(1).toLowerCase()).join(' ');
};

const lower = (s: string) => {
    return s.replaceAll('_', ' ').toLowerCase();
};

export const userRoles: Record<number, string> =
    reverseEnum(UserRole, (v: string): any => capitalize(v));

export const userStatuses: Record<number, string> =
    reverseEnum(UserStatus, (v: string): any => capitalize(v));

export const contextFieldValueTypes: Record<number, string> =
    reverseEnum(ContextValueType, (v: string): any => capitalize(v));

export const operators: Record<number, string> =
    reverseEnum(Operator, (v: string): any => lower(v));

export const contextFieldValueTypeOperators: Record<number, number[]> = {
    1: [1, 2, 7, 8, 9],
    2: [1, 2, 3, 4, 5, 6, 8, 9],
    3: [1, 2, 3, 4, 5, 6, 8, 9],
    4: [1, 2],
    5: [1, 2, 8, 9],
    6: [1, 2, 3, 4, 5, 6],
    7: [10, 11, 12, 13],
    8: [10, 11, 12, 13],
    9: [10, 11, 12, 13]
};
