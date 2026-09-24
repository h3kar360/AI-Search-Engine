import React, { useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { signInWithEmailAndPassword } from "firebase/auth";
import { auth } from "../../config/firebase";

const LoginForm = () => {
    const [email, setEmail] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const [isLoading, setIsLoading] = useState<boolean>(false);

    const navigate = useNavigate();

    const login = async (e: React.SubmitEvent) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            const userCredentials = await signInWithEmailAndPassword(
                auth,
                email,
                password,
            );
            const user = userCredentials.user;

            if (user) navigate("/");
        } catch (error) {
            console.error(error);
        } finally {
            setIsLoading(true);
        }
    };

    return (
        <form
            onSubmit={login}
            className="w-full max-w-md rounded-2xl bg-surface p-8 shadow-xl flex flex-col gap-5"
        >
            <div className="mb-2">
                <h1 className="text-center text-3xl font-semibold tracking-tight">
                    Sign in
                </h1>

                <p className="mt-2 text-center text-sm text-muted">
                    Welcome back. Sign in to continue.
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
                    onChange={(e) => setEmail(e.target.value)}
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
                    onChange={(e) => setPassword(e.target.value)}
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
                disabled={isLoading}
            >
                Sign in
            </button>

            <p className="text-center text-sm text-muted">
                Don't have an account yet?
                <NavLink
                    to="/signup"
                    className="pl-1 text-brand hover:text-brand-hover hover:underline"
                >
                    Create an account
                </NavLink>
            </p>
        </form>
    );
};

export default LoginForm;
