"use client"
import * as React from "react"
import { GalleryVerticalEnd } from "lucide-react"
import { usePathname } from "next/navigation"

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
  SidebarRail,
} from "@/components/ui/sidebar"


// This is sample data.
const data = {
  navMain: [
    {
      title: "General",
      url: "#",
      items: [
        {
          title: "Dashboard",
          url: "/dashboard",
        }
      ],
    },
    {
      title: "Claims",
      url: "#",
      items: [
        {
          title: "All Claims",
          url: "/claims/all",
        },
        {
          title: "Suspicions",
          url: "#",
        },
        {
          title: "Reports",
          url: "/claims/reports",
        },
      ],
    },
    {
      title: "User",
      url: "#",
      items: [
        {
          title: "Account",
          url: "#",
        },
        {
          title: "Tasks",
          url: "#",
        },
        {
          title: "Reminders",
          url: "#",
        },
      ],
    },
    // {
    //   title: "Architecture",
    //   url: "#",
    //   items: [
    //     {
    //       title: "Accessibility",
    //       url: "#",
    //     },
    //     {
    //       title: "Fast Refresh",
    //       url: "#",
    //     },
    //     {
    //       title: "Next.js Compiler",
    //       url: "#",
    //     },
    //     {
    //       title: "Supported Browsers",
    //       url: "#",
    //     },
    //     {
    //       title: "Turbopack",
    //       url: "#",
    //     },
    //   ],
    // },
    // {
    //   title: "Community",
    //   url: "#",
    //   items: [
    //     {
    //       title: "Contribution Guide",
    //       url: "#",
    //     },
    //   ],
    // },
  ],
}

export function AppSidebar({ ...props }) {
  const pathname = usePathname()

  return (
    <Sidebar {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg" asChild>
              <a href="#">
                {/* <div className="flex aspect-square size-8 items-center justify-center rounded-lg text-sidebar-primary-foreground"> */}
                  {/* <GalleryVerticalEnd className="size-4" /> */}
                {/* </div>
                <div className="flex flex-col gap-0.5 leading-none">
                  <span className="font-semibold">SBI Life</span>
                  <span className="">Insurance Claims</span>
                </div> */}
                <img src="/sbi_life_logo.png" alt="SBI Life" className="w-3/5" />
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarMenu>
            {data.navMain.map((item) => (
              <SidebarMenuItem key={item.title}>
                <SidebarMenuButton asChild>
                  <a href={item.url} className="font-medium">
                    {item.title}
                  </a>
                </SidebarMenuButton>
                {item.items?.length ? (
                  <SidebarMenuSub>
                    {item.items.map((item) => (
                      <SidebarMenuSubItem key={item.title}>
                        <SidebarMenuSubButton asChild isActive={pathname == item.url}>
                          <a href={item.url}>{item.title}</a>
                        </SidebarMenuSubButton>
                      </SidebarMenuSubItem>
                    ))}
                  </SidebarMenuSub>
                ) : null}
              </SidebarMenuItem>
            ))}
          </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>
      <SidebarRail />
    </Sidebar>
  )
}
