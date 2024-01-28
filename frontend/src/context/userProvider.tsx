import { User } from '@/api';
import { apiClient } from '@/lib/api';
import { useEffect, useState } from 'react';
import { UserContext } from './userContext';

export const UserProvider = ({ children }: any) => {
    const [user, setUser] = useState<User | undefined>(undefined);

    useEffect(() => {
        const storedUser = window.sessionStorage.getItem('current-user');
        if (storedUser) {
            setUser(JSON.parse(storedUser));
        } else {
            apiClient.users.getMe().then((data: User) => {
                window.sessionStorage.setItem(
                    'current-user',
                    JSON.stringify(data)
                );
                setUser(data);
            });
        }
    }, []);

    return <UserContext.Provider value={user}>{children}</UserContext.Provider>;
};
