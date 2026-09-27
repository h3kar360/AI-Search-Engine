import React, {
    useEffect,
    useState,
    type Dispatch,
    type SetStateAction,
} from "react";
import { useIsMobile } from "../../hooks/IsMobile";
import { useNavigate } from "react-router-dom";
import { useListeningAuth } from "../../context/AuthContext";
import { RxCross2 } from "react-icons/rx";
import { BsLayoutSidebar } from "react-icons/bs";
import { IoAdd } from "react-icons/io5";

interface Convo {
    id: string;
    title: string;
}

interface SideBarProp {
    isSidebarOpen: boolean;
    setIsSidebarOpen: Dispatch<SetStateAction<boolean>>;
}

const SideBar = ({ isSidebarOpen, setIsSidebarOpen }: SideBarProp) => {
    const [convos, setConvos] = useState<Convo[]>([]);
    const [convoTitle, setConvoTitle] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    const navigate = useNavigate();
    const isMobile = useIsMobile();
    const { user } = useListeningAuth();

    useEffect(() => {
        const getAllConvos = async () => {
            if (!user) return;

            try {
                const token = await user.getIdToken();

                const response = await fetch(
                    `${import.meta.env.VITE_API_URL}/api/${import.meta.env.VITE_API_VERSION}/conversations`,
                    {
                        method: "GET",
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    },
                );

                if (!response.ok) {
                    throw new Error("Conversations not found");
                }

                const data = await response.json();
                setConvos(data);
            } catch (error) {
                console.error(error);
            }
        };

        getAllConvos();
    }, [user, isLoading]);

    const deleteConvo = async (id: string) => {
        if (!user) return;

        setIsLoading(true);

        try {
            const token = await user.getIdToken();

            const response = await fetch(
                `${import.meta.env.VITE_API_URL}/api/${import.meta.env.VITE_API_VERSION}/conversations/${id}`,
                {
                    method: "DELETE",
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                },
            );

            if (!response.ok) {
                throw new Error("Conversation not deleted");
            }

            return navigate("/");
        } catch (error) {
            console.error(error);
        } finally {
            setIsLoading(false);
        }
    };

    const createConvo = async (e: React.SubmitEvent) => {
        e.preventDefault();

        if (!user || !convoTitle.trim()) return;

        setIsLoading(true);

        try {
            const token = await user.getIdToken();

            const response = await fetch(
                `${import.meta.env.VITE_API_URL}/api/${import.meta.env.VITE_API_VERSION}/conversations`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                    body: JSON.stringify({
                        title: convoTitle.trim(),
                    }),
                },
            );

            if (!response.ok) {
                throw new Error("Error when inserting new conversation");
            }

            const { id } = await response.json();

            setConvoTitle("");
            if (isMobile) setIsSidebarOpen(false);
            return navigate(`/conversations/${id}`);
        } catch (error) {
            console.error(error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <section
            className={`
                relative
                h-full
                shrink-0
                overflow-hidden
                border-r
                border-r-border-subtle/30
                bg-background
                transition-[width]
                duration-300
                ease-[cubic-bezier(0.22,1,0.36,1)]
                ${isSidebarOpen ? "w-80" : "w-16"}
            `}
        >
            {/* Top sidebar button */}
            <div className="h-16 w-full flex items-center px-2">
                <button
                    type="button"
                    onClick={() => setIsSidebarOpen((prev) => !prev)}
                    aria-label={
                        isSidebarOpen ? "Collapse sidebar" : "Expand sidebar"
                    }
                    aria-expanded={isSidebarOpen}
                    className="
                        w-12
                        h-12
                        shrink-0
                        rounded-xl
                        flex
                        items-center
                        justify-center
                        text-muted
                        hover:text-foreground
                        hover:bg-surface
                        cursor-pointer
                        transition-all
                        duration-200
                    "
                >
                    <BsLayoutSidebar className="text-xl" />
                </button>
            </div>
            {/* Sidebar content */}
            <div
                className={`
                    h-[calc(100%-4rem)]
                    px-4
                    pb-24
                    transition-all
                    duration-200
                    ${
                        isSidebarOpen
                            ? "opacity-100 translate-x-0"
                            : "opacity-0 translate-x-[-12px] pointer-events-none"
                    }
                `}
            >
                <div
                    className="h-full overflow-y-auto 
                    scrollbar-thin scrollbar-thumb-border-subtle/40 scrollbar-track-transparent
                    pr-4"
                >
                    <div className="flex flex-col gap-3">
                        {convos.map((convo) => (
                            <div
                                key={convo.id}
                                className="
                                    bg-input
                                    hover:bg-surface
                                    px-4
                                    py-2
                                    rounded-xl
                                    shadow-2xl
                                    border
                                    border-border-subtle/50
                                    flex
                                    justify-between
                                    items-center
                                    cursor-pointer
                                    transition-colors
                                    duration-200
                                "
                                onClick={() => {
                                    if (isMobile) setIsSidebarOpen(false);

                                    navigate(`/conversations/${convo.id}`);
                                }}
                            >
                                <p className="truncate pr-2">{convo.title}</p>

                                <button
                                    type="button"
                                    onClick={() => deleteConvo(convo.id)}
                                    disabled={isLoading}
                                    className="
                                        shrink-0
                                        cursor-pointer
                                        text-muted
                                        hover:text-foreground
                                        transition-colors
                                        duration-200
                                        disabled:opacity-30
                                    "
                                >
                                    <RxCross2 />
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
            {/* Create conversation */}
            <div className="absolute bottom-6 left-4 right-4">
                <form
                    onSubmit={createConvo}
                    className={`
                        flex
                        h-12
                        w-full
                        items-center
                        rounded-full
                        bg-surface
                        border
                        border-border-subtle/50
                        shadow-xl
                        overflow-hidden
                        transition-all
                        duration-200
                        ${
                            isSidebarOpen
                                ? "opacity-100 translate-y-0 pointer-events-auto"
                                : "opacity-0 translate-y-2 pointer-events-none"
                        }
                    `}
                >
                    <input
                        type="text"
                        value={convoTitle}
                        onChange={(e) => setConvoTitle(e.target.value)}
                        placeholder="Add a conversation..."
                        disabled={isLoading}
                        className="
                            min-w-0
                            flex-1
                            h-full
                            bg-transparent
                            px-4
                            outline-none
                            text-sm
                            placeholder:text-muted/60
                        "
                    />

                    <button
                        type="submit"
                        disabled={!convoTitle.trim() || isLoading}
                        aria-label="Create conversation"
                        className="
                            w-10
                            h-10
                            mr-1
                            shrink-0
                            rounded-full
                            flex
                            items-center
                            justify-center
                            bg-brand
                            hover:bg-brand-hover
                            text-white
                            cursor-pointer
                            transition-colors
                            duration-200
                            disabled:opacity-40
                            disabled:cursor-not-allowed
                        "
                    >
                        <IoAdd className="text-2xl" />
                    </button>
                </form>
            </div>
        </section>
    );
};

export default SideBar;
