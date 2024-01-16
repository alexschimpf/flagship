import AuditLogs from '@/components/custom/auditLogs'
import Members from '@/components/custom/members'
import Projects from '@/components/custom/projects'
import { Toaster } from '@/components/ui/toaster'
import { Page, useGlobalStore } from '@/stores'

export default function() {
    const globalStore = useGlobalStore();

    return (
        <main className='flex-1 flex flex-col container items-center w-1/2 py-4'>
            {
                globalStore.currPage == Page.Projects && <Projects />
            }
            {
                globalStore.currPage == Page.Members && <Members />
            }
            {
                globalStore.currPage == Page.AuditLogs && <AuditLogs />
            }
            <Toaster />
        </main>
    )
}
