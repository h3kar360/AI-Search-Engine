import { useState, type Dispatch, type SetStateAction } from "react";
import { useListeningAuth } from "../context/AuthContext";

import ChatPanel from "../components/ChatComponents/ChatPanel";
import ChatInput from "../components/ChatComponents/ChatInput";
import SideBar from "../components/ChatComponents/SideBar";
import { GiMagicLamp } from "react-icons/gi";

import type { Message } from "../types/chat";

interface SideBarProp {
    isSidebarOpen: boolean;
    setIsSidebarOpen: Dispatch<SetStateAction<boolean>>;
}

const HomePage = ({ isSidebarOpen, setIsSidebarOpen }: SideBarProp) => {
    const { user } = useListeningAuth();

    const [messages, setMessages] = useState<Array<Message>>([]);

    return (
        <section className="w-full h-[calc(100vh-3.75rem)] flex">
            <SideBar
                isSidebarOpen={isSidebarOpen}
                setIsSidebarOpen={setIsSidebarOpen}
            />
            {user ? (
                <div className="w-full h-full flex flex-col justify-center items-center gap-4 text-center text-4xl">
                    <GiMagicLamp size="3em" />
                    <div>Chat in an existing conversation</div>
                </div>
            ) : (
                <div className="flex-1 min-w-0 flex flex-col">
                    <ChatPanel
                        messages={messages}
                        setMessages={setMessages}
                        id={null}
                    />
                    <ChatInput
                        messages={messages}
                        setMessages={setMessages}
                        id={null}
                    />
                </div>
            )}
        </section>
    );
};

export default HomePage;
