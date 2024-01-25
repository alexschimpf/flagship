import { Project } from "@/api";
import { createContext } from "react";

export const ProjectContext = createContext<Project | undefined>(undefined);
