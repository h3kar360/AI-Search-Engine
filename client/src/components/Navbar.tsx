import { NavLink } from "react-router-dom";
import { GiMagicLamp } from "react-icons/gi";

const Navbar = () => {
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
            <button className="px-4 py-2 bg-brand hover:bg-brand-hover rounded-2xl text-sm font-medium transition-colors cursor-pointer border-none">
                Log In
            </button>
        </nav>
    );
};

export default Navbar;
