import React from 'react'
import {
    SidebarInset,
    SidebarProvider,
    SidebarTrigger,
  } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"
import AppHeader from '@/components/app-header'


function layout({children}) {
  return (
    <SidebarProvider>
        <AppSidebar />
        <SidebarInset>
            <AppHeader />
            <div className='p-5'>
              {children}
            </div>
        </SidebarInset>
    </SidebarProvider>
  )
}

export default layout