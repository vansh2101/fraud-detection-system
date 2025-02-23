"use client"
import React, {useState} from "react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"


export function InsuranceForm({
  className,
  ...props
}) {

  const [loading, setLoading] = useState(false)
  const [submitted, setSubmitted] = useState(false)

  const submit = () => {
    setLoading(true)
    setTimeout(() => {
      setSubmitted(true)
    }, 2500)
  }

  return (
    <div className={cn("flex flex-col gap-6", className)} {...props}>
      <Card className="overflow-hidden">
        <CardContent className="max-h-3/4">
          {loading && !submitted && 
            <div className="h-96 flex flex-col items-center justify-center">
              <div className='w-10 aspect-square border-[6px] border-r-primary rounded-full animate-spin' />
            </div>
          }

          {submitted &&
            <div className="h-96 flex flex-col items-center justify-center">
              <h1 className="text-2xl font-bold">
                Submitted Successfully!!
              </h1>
            </div>
          }

          {
            !loading && 
          <form className="p-6 md:p-8">
            <div className="flex flex-col gap-6">
              <div className="flex flex-col items-center text-center">
                <h1 className="text-2xl font-bold">File Claim</h1>
                <p className="text-balance text-muted-foreground">
                  Submit Documents for Filing a Claim
                </p>
              </div>
              <div className="grid gap-2">
                <Label htmlFor="name">Your Name</Label>
                <Input
                  id="name"
                  type="text"
                  required
                />
              </div>
              <div className="grid gap-2">
                <div className="flex items-center">
                  <Label htmlFor="policy">Policy Number</Label>
                </div>
                <Input id="policy" type="text" required />
              </div>
              <div className="grid gap-2">
                <div className="flex items-center">
                  <Label htmlFor="claim">Claim Type</Label>
                </div>
                <Select>
                  <SelectTrigger className="w-full">
                    <SelectValue placeholder="Claim Type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="light">Health</SelectItem>
                    <SelectItem value="dark">Automobile</SelectItem>
                    <SelectItem value="system">Theft</SelectItem>
                    <SelectItem value="system">Travel</SelectItem>
                    <SelectItem value="system">Property</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="grid gap-2">
                <div className="flex items-center">
                  <Label htmlFor="reason">Claim Reason</Label>
                </div>
                <Input id="reason" type="text" required />
              </div>
                
              <div className="grid gap-2">
                <div className="flex items-center">
                  <Label htmlFor="id">Government ID</Label>
                </div>
                <Input id="id" type="file" required />
              </div>
              <div className="grid gap-2">
                <div className="flex items-center">
                  <Label htmlFor="doc">Other Documents</Label>
                </div>
                <Input id="doc" type="file" required />
              </div>
              <Button type="submit" className="w-full" onClick={submit}>
                Submit
              </Button>
            </div>
          </form>
          }
        </CardContent>
      </Card>
    </div>
  )
}
