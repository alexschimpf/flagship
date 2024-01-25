import { Project } from "@/api";
import { useReducer } from "react";
import { ProjectContext } from "./projectContext";

export const ProjectProvider = ({children}: any) => {
    const [state, dispatch] = useReducer((state_: any, project: Project): any => {
        return {
            ...project
        }
    }, {});

   return(
       <ProjectContext.Provider value={{ state, dispatch }}>
           {children}
       </ProjectContext.Provider>
   )
}
