import React from "react";
import { Link } from "react-router-dom";

const LoginPage = () => {
  return (
    <div className="flex min-h-full flex-col justify-center bg-quinary px-6 py-12 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-sm">
        <img
          alt="Your Company"
          src="https://tailwindcss.com/plus-assets/img/logos/mark.svg?color=519c4b"
          className="mx-auto h-10 w-auto"
        />
        <h2 className="mt-10 text-center text-2xl font-bold tracking-tight text-white">
          Sign in to your account
        </h2>
      </div>

      <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
        <form action="#" method="POST" className="space-y-6">
          <div className="relative">
            <input
              id="email"
              name="email"
              type="email"
              required
              className="peer block w-full rounded-md bg-white px-3 pt-5 pb-2 text-base text-accent_dark outline-1 -outline-offset-1 outline-white/10 placeholder-transparent focus:outline-2 focus:-outline-offset-2 focus:outline-secondary sm:text-sm"
              placeholder="Email Address"
            />
            <span className="absolute pointer-events-none left-3 top-2 text-sm text-black transition-all peer-placeholder-shown:top-3 peer-placeholder-shown:text-base peer-placeholder-shown:text-accent_dark peer-focus:top-0 peer-focus:text-sm peer-focus:text-accent_dark">
              Email Address
            </span>
          </div>

          <div className="relative">
            <input
              id="password"
              name="password"
              type="password"
              required
              className="peer block w-full rounded-md bg-white px-3 pt-5 pb-2 text-base text-accent_dark outline-1 -outline-offset-1 outline-white/10 placeholder-transparent focus:outline-2 focus:-outline-offset-2 focus:outline-secondary sm:text-sm"
              placeholder="Password"
            />
            <span className="absolute pointer-events-none left-3 top-2 text-sm text-black transition-all peer-placeholder-shown:top-3 peer-placeholder-shown:text-base peer-placeholder-shown:text-accent_dark peer-focus:top-0 peer-focus:text-sm peer-focus:text-accent_dark">
              Password
            </span>
          </div>

          <div>
            <button
              type="submit"
              className="flex w-full justify-center rounded-md bg-primary px-3 py-1.5 text-sm font-semibold text-white hover:bg-tertiary focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-secondary"
            >
              Sign in
            </button>
          </div>
        </form>

        <p className="mt-10 text-center text-sm text-white">
          Not a member?{" "}
          <Link
            to="/auth/signup"
            className="font-semibold text-accent_light hover:text-primary"
          >
            Start a 14 day free trial
          </Link>
        </p>
      </div>
    </div>
  );
};

export default LoginPage;