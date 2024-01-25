export const getLocalTimeString = (dateTimeStr: string): string => {
    return new Date(dateTimeStr).toLocaleString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        timeZoneName: 'short'
    }).replace(', ', ' ');
}
