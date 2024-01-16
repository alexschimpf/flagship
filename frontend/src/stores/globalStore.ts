import { create } from 'zustand'

enum Page {
    Projects = 'projects',
    Members = 'members',
    AuditLogs = 'audit-logs'
}

interface GlobalState {
    currPage: Page   
    setCurrPage: (page: Page) => void
}

const useGlobalStore = create<GlobalState>()((set) => ({
    currPage: Page.Projects,
    setCurrPage: (page: Page) => set(() => ({ currPage: page }))
}));

export { useGlobalStore, Page };
