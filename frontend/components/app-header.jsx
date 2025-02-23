"use client"
import React from 'react'
import { usePathname } from 'next/navigation'
import {
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbLink,
    BreadcrumbList,
    BreadcrumbPage,
    BreadcrumbSeparator,
  } from "@/components/ui/breadcrumb"
  import { Separator } from "@/components/ui/separator"
  import {
    SidebarTrigger,
  } from "@/components/ui/sidebar"

export default function AppHeader() {
  const pathname = usePathname()

  let links = pathname.split('/').splice(1)
  const last = links[links.length - 1]
  links = links.splice(0, links.length - 1)
  console.log(links)

  return (
    <header className="flex h-16 shrink-0 items-center gap-2 border-b">
        <div className="flex items-center gap-2 px-3">
            <SidebarTrigger />
            <Separator orientation="vertical" className="mr-2 h-4" />
            <Breadcrumb>
            <BreadcrumbList>
                {links.map((link, index) => 
                <div key={index} className='flex items-center gap-2'>
                <BreadcrumbItem key={index}>
                    <BreadcrumbLink href="#" className='capitalize'>{link}</BreadcrumbLink>
                </BreadcrumbItem>
                <BreadcrumbSeparator className="hidden md:block" />
                </div>
                )}

                <BreadcrumbItem>
                  <BreadcrumbPage className='capitalize'>{last}</BreadcrumbPage>
                </BreadcrumbItem>
            </BreadcrumbList>
            </Breadcrumb>
        </div>
    </header>
  )
}
