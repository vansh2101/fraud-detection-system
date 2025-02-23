import React from 'react'
import { InsuranceForm } from '@/components/insurance-form'

export default function page() {
  return (
    <div className="flex min-h-svh flex-col items-center justify-center bg-muted p-6 md:p-10">
        <div className="w-full max-w-sm md:max-w-3xl">
            <InsuranceForm />
        </div>
    </div>
  )
}
