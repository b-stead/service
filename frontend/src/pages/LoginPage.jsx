import React from "react";
import { Link } from "react-router-dom";

const LoginPage = () => {
    return (
        <>
            {/*
          This example requires updating your template:
  
          ```
          <html class="h-full bg-gray-900">
          <body class="h-full">
          ```
        */}
            <div className="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
                <div className="sm:mx-auto sm:w-full sm:max-w-sm">
                    <img
                        alt="Your Company"
                        src="https://tailwindcss.com/plus-assets/img/logos/mark.svg?color=orange&shade=500"
                        className="mx-auto h-10 w-auto"
                    />
                    <h2 className="mt-10 text-center text-2xl/9 font-bold tracking-tight text-black">Sign in to your account</h2>
                </div>
  
                <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
                    <form action="#" method="POST" className="space-y-6">
                        <div>
                            <label htmlFor="email" className="block text-sm/6 font-medium text-black">
                                Email address
                            </label>
                            <div className="mt-2">
                                <input
                                    id="email"
                                    name="email"
                                    type="email"
                                    required
                                    autoComplete="email"
                                    className="block w-full rounded-md bg-white/5 px-3 py-1.5 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-secondary sm:text-sm/6"
                                />
                            </div>
                        </div>
  
                        <div>
                            <div className="flex items-center justify-between">
                                <label htmlFor="password" className="block text-sm/6 font-medium text-black">
                                    Password
                                </label>
                                <div className="text-sm">
                                    <a href="#" className="font-semibold text-tertiary hover:text-secondary">
                                        Forgot password?
                                    </a>
                                </div>
                            </div>
                            <div className="mt-2">
                                <input
                                    id="password"
                                    name="password"
                                    type="password"
                                    required
                                    autoComplete="current-password"
                                    className="block w-full rounded-md bg-white/5 px-3 py-1.5 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-secondary sm:text-sm/6"
                                />
                            </div>
                        </div>
  
                        <div>
                            <button
                                type="submit"
                                className="flex w-full justify-center rounded-md bg-tertiary px-3 py-1.5 text-sm/6 font-semibold text-black hover:bg-secondary focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:secondary"
                            >
                                Sign in
                            </button>
                        </div>
                    </form>
  
                    <p className="mt-10 text-center text-sm/6 text-gray-400">
                        Not a member?{' '}
                        <Link
                            to="/auth/signup"
                            className="font-semibold text-tertiary hover:text-secondary"
                        >
                            Start a 14 day free trial
                        </Link>
                    </p>
                </div>
            </div>
        </>
    )
};

  export default LoginPage;