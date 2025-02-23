"use client"

import * as React from "react"
import {
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
} from "@tanstack/react-table"
import { ArrowUpDown, ChevronDown, MoreHorizontal } from "lucide-react"
import { Badge } from "./ui/badge"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Input } from "@/components/ui/input"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import Link from "next/link"

const data = [
  {
    policy_no: "47184",
    Name: "Meraj Khan",
    Email: "meraj@gmail.com",
    Phone: "+91 9876543210",
    ClaimAmount: "Rs. 30,000",
    PaidAmount: "Rs. 25,000",
    ClaimStatus: "Not Reviewed",
    ClaimReason: "Criminal Damage",
    VehicleNo: "RY52 APF",
    Location: "188 Lincoln Street",
    Date: "21/08/2017",
  },

  {
    policy_no: "47183",
    Name: "Phillip",
    Email: "perry4d@gmail.com",
    Phone: "(103)222-1420",
    ClaimAmount: "$500",
    PaidAmount: "$338",
    ClaimStatus: "Under Review",
    ClaimReason: "Shoplifting",
    VehicleNo: "-",
    Location: "188 Lincoln Street",
    Date: "21/08/2017",
  },

  {
    policy_no: "47182",
    Name: "Harry",
    Email: "harry@gmail.com",
    Phone: "(106)438-2013",
    ClaimAmount: "$100",
    PaidAmount: "$93",
    ClaimStatus: "Validated",
    ClaimReason: "Burglary",
    VehicleNo: "-",
    Location: "188 Lincoln Street",
    Date: "21/08/2017",
  },
  {
    policy_no: "47181",
    Name: "Deborah",
    Email: "deborah@gmail.com",
    Phone: "(106)592-7420",
    ClaimAmount: "$230",
    PaidAmount: "$200",
    ClaimStatus: "Suspected",
    ClaimReason: "Criminal Damage",
    VehicleNo: "RY52 APF",
    Location: "188 Lincoln Street",
    Date: "21/08/2017",
  },
]

export const columns = [
  {
    id: "select",
    header: ({ table }) => (
      <Checkbox
        checked={
          table.getIsAllPageRowsSelected() ||
          (table.getIsSomePageRowsSelected() && "indeterminate")
        }
        onCheckedChange={(value) => table.toggleAllPageRowsSelected(!!value)}
        aria-label="Select all"
      />
    ),
    cell: ({ row }) => (
      <Checkbox
        checked={row.getIsSelected()}
        onCheckedChange={(value) => row.toggleSelected(!!value)}
        aria-label="Select row"
      />
    ),
    enableSorting: false,
    enableHiding: false,
  },
  {
    accessorKey: "policy_no",
    header: "Policy No.",
    cell: ({ row }) => (
      <div className="capitalize">{row.getValue("policy_no")}</div>
    ),
  },
  {
    accessorKey: "Name",
    header: "Client Name",
    cell: ({ row }) => (
      <div className="capitalize">{row.getValue("Name")}</div>
    ),
  },
  {
    accessorKey: "Email",
    header: "Client Email",
    cell: ({ row }) => (
      <div className="truncate">{row.getValue("Email")}</div>
    ),
  },
  {
    accessorKey: "Phone",
    header: "Client Phone",
    cell: ({ row }) => (
      <div className="truncate">{row.getValue("Phone")}</div>
    ),
  },
  {
    accessorKey: "ClaimAmount",
    header: "Claim Amount",
    cell: ({ row }) => (
      <div className="">{row.getValue("ClaimAmount")}</div>
    ),
  },
  {
    accessorKey: "PaidAmount",
    header: "Paid Amount",
    cell: ({ row }) => (
      <div className="truncate">{row.getValue("PaidAmount")}</div>
    ),
  },
  {
    accessorKey: "ClaimReason",
    header: "Claim Reason",
    cell: ({ row }) => (
      <div className="truncate">{row.getValue("ClaimReason")}</div>
    ),
  },
  {
    accessorKey: "VehicleNo",
    header: "Vehicle No.",
    cell: ({ row }) => (
      <div className="truncate">{row.getValue("VehicleNo")}</div>
    ),
  },
  {
    accessorKey: "ClaimStatus",
    header: "Claim Status",
    cell: ({ row }) => {
      const val = row.getValue("ClaimStatus")
      return (
        <Badge variant={val === "Suspected" ? "destructive" : val === "Not Reviewed" ? "secondary" : "default"}>{val}</Badge>
      )
    },
  },
  // {
  //   accessorKey: "email",
  //   header: ({ column }) => {
  //     return (
  //       <Button
  //         variant="ghost"
  //         onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
  //       >
  //         Email
  //         <ArrowUpDown />
  //       </Button>
  //     )
  //   },
  //   cell: ({ row }) => <div className="lowercase">{row.getValue("email")}</div>,
  // },
  // {
  //   accessorKey: "amount",
  //   header: () => <div className="text-right">Amount</div>,
  //   cell: ({ row }) => {
  //     const amount = parseFloat(row.getValue("amount"))

  //     // Format the amount as a dollar amount
  //     const formatted = new Intl.NumberFormat("en-US", {
  //       style: "currency",
  //       currency: "USD",
  //     }).format(amount)

  //     return <div className="text-right font-medium">{formatted}</div>
  //   },
  // },
  {
    id: "actions",
    enableHiding: false,
    cell: ({ row }) => {
      const payment = row.original

      return (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="h-8 w-8 p-0">
              <span className="sr-only">Open menu</span>
              <MoreHorizontal />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuLabel>Actions</DropdownMenuLabel>
            <DropdownMenuItem
              onClick={() => navigator.clipboard.writeText(payment.policy_no)}
            >
              Copy Policy No.
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <Link href={`/claims/reports/${payment.policy_no}`}>
              <DropdownMenuItem>Run Validation Check</DropdownMenuItem>
            </Link>
            {/* <DropdownMenuItem>View payment details</DropdownMenuItem> */}
          </DropdownMenuContent>
        </DropdownMenu>
      )
    },
  },
]

export function DataTable() {
  const [sorting, setSorting] = React.useState([])
  const [columnFilters, setColumnFilters] = React.useState(
    []
  )
  const [columnVisibility, setColumnVisibility] =
    React.useState({})
  const [rowSelection, setRowSelection] = React.useState({})

  const table = useReactTable({
    data,
    columns,
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    onColumnVisibilityChange: setColumnVisibility,
    onRowSelectionChange: setRowSelection,
    state: {
      sorting,
      columnFilters,
      columnVisibility,
      rowSelection,
    },
  })

  return (
    <div className="w-full">
      <div className="flex items-center py-4">
        <Input
          placeholder="Filter clients..."
          value={(table.getColumn("Name")?.getFilterValue()) ?? ""}
          onChange={(event) =>
            table.getColumn("Name")?.setFilterValue(event.target.value)
          }
          className="max-w-sm"
        />
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" className="ml-auto">
              Columns <ChevronDown />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            {table
              .getAllColumns()
              .filter((column) => column.getCanHide())
              .map((column) => {
                return (
                  <DropdownMenuCheckboxItem
                    key={column.id}
                    className="capitalize"
                    checked={column.getIsVisible()}
                    onCheckedChange={(value) =>
                      column.toggleVisibility(!!value)
                    }
                  >
                    {column.id}
                  </DropdownMenuCheckboxItem>
                )
              })}
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => {
                  return (
                    <TableHead key={header.id}>
                      {header.isPlaceholder
                        ? null
                        : flexRender(
                            header.column.columnDef.header,
                            header.getContext()
                          )}
                    </TableHead>
                  )
                })}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => (
                <TableRow
                  key={row.id}
                  data-state={row.getIsSelected() && "selected"}
                >
                  {row.getVisibleCells().map((cell) => (
                    <TableCell key={cell.id}>
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext()
                      )}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="h-24 text-center"
                >
                  No results.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
      <div className="flex items-center justify-end space-x-2 py-4">
        <div className="flex-1 text-sm text-muted-foreground">
          {table.getFilteredSelectedRowModel().rows.length} of{" "}
          {table.getFilteredRowModel().rows.length} row(s) selected.
        </div>
        <div className="space-x-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => table.previousPage()}
            disabled={!table.getCanPreviousPage()}
          >
            Previous
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => table.nextPage()}
            disabled={!table.getCanNextPage()}
          >
            Next
          </Button>
        </div>
      </div>
    </div>
  )
}
