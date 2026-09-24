import { useState } from "react";
import { NavLink } from "react-router-dom";
import { GiMagicLamp } from "react-icons/gi";
import { useListeningAuth } from "../context/AuthContext";
import { auth } from "../config/firebase";
import { signOut } from "firebase/auth";

const Navbar = () => {
    const [isHover, setIsHover] = useState<boolean>(false);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const { user } = useListeningAuth();

    const logout = async () => {
        try {
            setIsLoading(true);

            await signOut(auth);
        } catch (error) {
            console.error(error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <nav className="fixed top-0 left-0 right-0 h-15 z-50 flex items-center justify-between px-6">
            <div
                className="absolute top-0 left-0 right-0 h-24 bg-gradient-to-b from-white/30 via-white/10 to-transparent pointer-events-none -z-10"
                aria-hidden="true"
            />
            {/* Brand Logo */}
            <div className="text-2xl tracking-tight">
                <NavLink
                    to="/"
                    className="hover:opacity-90 transition-opacity flex items-center gap-1"
                >
                    <GiMagicLamp />
                    <div>Genie</div>
                </NavLink>
            </div>
            {/* Login Button */}
            {user ? (
                <div
                    className="relative cursor-pointer"
                    onMouseEnter={() => setIsHover(true)}
                    onMouseLeave={() => setIsHover(false)}
                >
                    <div className="px-4 py-2 text-sm">Hi! {user.email}</div>

                    {/* Dropdown */}
                    <div
                        className={`
                            absolute right-0 top-full z-50 pt-2
                            transition-all duration-200 ease-out
                            ${
                                isHover
                                    ? "visible translate-y-0 opacity-100"
                                    : "invisible -translate-y-1 opacity-0 pointer-events-none"
                            }
                        `}
                    >
                        <div className="rounded-lg border bg-white px-4 py-3 shadow-lg">
                            <button
                                className="rounded-2xl bg-brand px-4 py-2 text-sm
                                        transition-colors hover:bg-brand-hover"
                                onClick={logout}
                                disabled={isLoading}
                            >
                                Log out
                            </button>
                        </div>
                    </div>
                </div>
            ) : (
                <NavLink
                    to="/login"
                    className="rounded-2xl bg-brand px-4 py-2 text-sm
                   transition-colors hover:bg-brand-hover"
                >
                    Log In
                </NavLink>
            )}
        </nav>
    );
};

export default Navbar;
