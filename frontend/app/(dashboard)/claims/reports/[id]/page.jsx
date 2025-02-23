"use client"

import React, {useEffect, useState} from 'react'
import { Badge } from '@/components/ui/badge'

export default function page({ params }) {
    const [loading, setLoading] = useState(true)
    const [txt, setTxt] = useState('Reading Documents')
    const vars = React.use(params)

    useEffect(() => {
        fetch('http://localhost:8000/validate-claim', {
            method: 'GET'
        })

        setTimeout(() => {
            setTxt('Analyzing Documents')
        }, 1500)

        setTimeout(() => {
            setTxt('Extracting Data')
        }, 3000)

        setTimeout(() => {
            setTxt('Validating Data')
        }, 6000)

        setTimeout(() => {
            setTxt('Generating Report')
        }, 8000)

        setTimeout(() => {
            setLoading(false)
        }, 11000)
    }, [])

    if (loading) {
        return (
            <div className='w-full h-[70vh] flex items-center justify-center gap-3'>
                <div className='w-10 aspect-square border-[6px] border-r-primary rounded-full animate-spin' />
                {txt}...
            </div>
        )
    }

    return (
        <div className='flex flex-col gap-7'>
            <div className='flex items-center gap-8'>
                <div className='text-sm flex flex-col items-center gap-1'>
                    <img src='/pfp.png' className='rounded' />
                    (extracted from govt. id.)
                </div>

                <div>
                    <label className='text-sm font-bold'>
                        First Name:
                    </label>
                    <p className='mb-5'>
                        Meraj
                    </p>

                    <label className='text-sm font-bold'>
                        Last Name:
                    </label>
                    <p>
                        Khan
                    </p>
                </div>

                <div>
                    <label className='text-sm font-bold'>
                        Phone No.:
                    </label>
                    <p className='mb-5'>
                        +91 9876543210
                    </p>

                    <label className='text-sm font-bold'>
                        Email:
                    </label>
                    <p>
                        meraj@gmail.com
                    </p>
                </div>

                <div>
                    <label className='text-sm font-bold'>
                        Age:
                    </label>
                    <p className='mb-5'>
                        37
                    </p>

                    <label className='text-sm font-bold'>
                        State:
                    </label>
                    <p>
                        Uttar Pradesh
                    </p>
                </div>

                <div>
                    <label className='text-sm font-bold'>
                        Aadhaar No.:
                    </label>
                    <p className='mb-5'>
                        2943 6593 3461
                    </p>

                    <label className='text-sm font-bold'>
                        Policy Number:
                    </label>
                    <p>
                        {vars.id}
                    </p>
                </div>

                <div>
                    <label className='text-sm font-bold'>
                        Claim Amount:
                    </label>
                    <p className='mb-5'>
                        Rs. 30,000
                    </p>

                    <label className='text-sm font-bold'>
                        Paid Amount:
                    </label>
                    <p>
                        Rs. 25,000
                    </p>
                </div>
            </div>

            <div className='flex flex-col gap-2'>
                <div className='flex items-center gap-3'>
                    <label className='font-bold text-sm'>
                        Claim Reason:
                    </label>

                    <p>
                        Criminal Damage
                    </p>
                </div>

                <div className='flex items-center gap-3'>
                    <label className='font-bold text-sm'>
                        Validation Conclusion   :
                    </label>

                    <Badge variant={"destructive"}>
                        Suspected
                    </Badge>
                </div>

                <div className='flex items-center gap-3'>
                    <label className='font-bold text-sm'>
                        Fraud Pattern Detected:
                    </label>

                    <p>
                        Automobile Scam
                    </p>
                </div>

                <div className='flex items-center gap-3'>
                    <label className='font-bold text-sm'>
                        Similar Claim IDs:
                    </label>

                    <p>
                        47180
                    </p>
                </div>
            </div>

            <h1 className='text-lg font-bold'>
                Document Previews:
            </h1>
            <div className='flex items-center justify-center gap-10'>
                <img src="/aadhaar.webp" className='w-1/3 rounded blur-sm' />

                <img src="/bill.jpg" className='w-1/3 rounded blur-sm' />
            </div>
        </div>
    )
}
