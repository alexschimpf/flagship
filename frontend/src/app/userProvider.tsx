import { User } from "@/api";
import { apiClient } from "@/utils/api";
import { useEffect, useState } from "react";
import { userContext } from "./userContext";

export const UserProvider = ({children}: any) => {
    const [user, setUser] = useState<User | undefined>(undefined);

    useEffect(() => {
        const storedUser = window.sessionStorage.getItem('current-user');
        if (storedUser) {
            setUser(JSON.parse(storedUser));
        } else {
            apiClient.users.getMe().then((data: User) => {
                window.sessionStorage.setItem('current-user', JSON.stringify(data));
                setUser(data);
            });
        }
    }, [])

   const { Provider } = userContext;
   return(
       <Provider value={user}>
           {children}
       </Provider>
   )
}
