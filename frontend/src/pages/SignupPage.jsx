import React from "react";
import { Link } from "react-router-dom";

const SignupPage = () => {
  return (
    <div className="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-sm">
        <img
          alt="Your Company"
          src="https://tailwindcss.com/plus-assets/img/logos/mark.svg?color=orange&shade=500"
          className="mx-auto h-10 w-auto"
        />
        <h2 className="mt-10 text-center text-2xl/9 font-bold tracking-tight text-black">
          Create your account
        </h2>
      </div>

      <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
        <form action="#" method="POST" className="space-y-6">
          {/* Full Name Field */}
          <div className="relative">
            <input
              id="name"
              name="name"
              type="text"
              required
              className="peer block w-full rounded-md bg-white/5 px-3 pt-5 pb-2 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder-transparent focus:outline-2 focus:-outline-offset-2 focus:outline-secondary sm:text-sm/6"
              placeholder="Full Name"
            />
            <span className="absolute left-3 top-2 text-sm text-gray-500 transition-all peer-placeholder-shown:top-5 peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-400 peer-focus:top-2 peer-focus:text-sm peer-focus:text-secondary">
              Full Name
            </span>
          </div>

          {/* Email Field */}
          <div className="relative">
            <input
              id="email"
              name="email"
              type="email"
              required
              className="peer block w-full rounded-md bg-white/5 px-3 pt-5 pb-2 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder-transparent focus:outline-2 focus:-outline-offset-2 focus:outline-secondary sm:text-sm/6"
              placeholder="Email Address"
            />
            <span className="absolute left-3 top-2 text-sm text-gray-500 transition-all peer-placeholder-shown:top-5 peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-400 peer-focus:top-2 peer-focus:text-sm peer-focus:text-secondary">
              Email Address
            </span>
          </div>

          {/* Password Field */}
          <div className="relative">
            <input
              id="password"
              name="password"
              type="password"
              required
              className="peer block w-full rounded-md bg-white/5 px-3 pt-5 pb-2 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder-transparent focus:outline-2 focus:-outline-offset-2 focus:outline-secondary sm:text-sm/6"
              placeholder="Password"
            />
            <span className="absolute left-3 top-2 text-sm text-gray-500 transition-all peer-placeholder-shown:top-5 peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-400 peer-focus:top-2 peer-focus:text-sm peer-focus:text-secondary">
              Password
            </span>
          </div>

          {/* Submit Button */}
          <div>
            <button
              type="submit"
              className="flex w-full justify-center rounded-md bg-tertiary px-3 py-1.5 text-sm/6 font-semibold text-black hover:bg-secondary focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:secondary"
            >
              Sign up
            </button>
          </div>
        </form>

        <p className="mt-10 text-center text-sm/6 text-gray-400">
          Already have an account?{" "}
          <Link
            to="/auth/login"
            className="font-semibold text-tertiary hover:text-secondary"
          >
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
};

export default SignupPage;