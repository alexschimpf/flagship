import { User } from "@/api";
import { createContext } from "react";

export const userContext = createContext<User | undefined>(undefined);
