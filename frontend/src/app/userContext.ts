import { User } from "@/api";
import { createContext } from "react";

export const UserContext = createContext<User | undefined>(undefined);
