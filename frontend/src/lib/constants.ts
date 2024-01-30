export const userRoles: Record<number, string> = {
    1: 'Read only',
    2: 'Standard',
    3: 'Admin',
    4: 'Owner'
};
export const userStatuses: Record<number, string> = {
    1: 'Invited',
    2: 'Activated'
};
export const contextFieldValueTypes: Record<number, string> = {
    1: 'String',
    2: 'Number',
    3: 'Integer',
    4: 'Boolean',
    5: 'Enum',
    6: 'Semantic Version',
    7: 'String List',
    8: 'Integer List',
    9: 'Enum List'
};
export const operators: Record<number, string> = {
    1: 'is',
    2: 'is not',
    3: '<',
    4: '<=',
    5: '>',
    6: '>=',
    7: 'matches',
    8: 'is one of',
    9: 'is not one of',
    10: 'has one of',
    11: 'does not have any of',
    12: 'has',
    13: 'does not have'
};
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
