import { NavLink } from "react-router-dom";

const SignupForm = () => {
    const signup = () => {};

    return (
        <form
            onSubmit={signup}
            className="w-full max-w-md rounded-2xl bg-surface p-8 shadow-xl flex flex-col gap-5"
        >
            <div className="mb-2">
                <h1 className="text-center text-3xl font-semibold tracking-tight">
                    Sign Up
                </h1>

                <p className="mt-2 text-center text-sm text-muted">
                    Welcome new user. Sign up to continue.
                </p>
            </div>

            <div className="flex flex-col gap-2">
                <label htmlFor="email" className="text-sm font-medium">
                    Email
                </label>

                <input
                    id="email"
                    type="email"
                    name="email"
                    placeholder="you@example.com"
                    className="
                        rounded-xl
                        bg-inputs
                        px-4 py-3
                        text-sm
                        outline-none
                        placeholder:text-muted/60
                        transition
                        focus:ring-2
                        focus:ring-brand/40
                    "
                />
            </div>

            <div className="flex flex-col gap-2">
                <label htmlFor="password" className="text-sm font-medium">
                    Password
                </label>

                <input
                    id="password"
                    type="password"
                    name="password"
                    placeholder="Enter your password"
                    className="
                        rounded-xl
                        bg-inputs
                        px-4 py-3
                        text-sm
                        outline-none
                        placeholder:text-muted/60
                        transition
                        focus:ring-2
                        focus:ring-brand/40
                    "
                />
            </div>

            <button
                type="submit"
                className="
                    mt-2
                    rounded-xl
                    bg-brand
                    py-3
                    font-medium
                    transition
                    hover:bg-brand-hover
                    active:scale-[0.98]
                "
            >
                Sign up
            </button>

            <p className="text-center text-sm text-muted">
                Already have an account?
                <NavLink
                    to="/login"
                    className="pl-1 text-brand hover:text-brand-hover hover:underline"
                >
                    log in to your account
                </NavLink>
            </p>
        </form>
    );
};

export default SignupForm;
