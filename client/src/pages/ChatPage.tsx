import { useState, type Dispatch, type SetStateAction } from "react";
import { useIsMobile } from "../hooks/IsMobile";

import ChatPanel from "../components/ChatComponents/ChatPanel";
import ChatInput from "../components/ChatComponents/ChatInput";
import SideBar from "../components/ChatComponents/SideBar";

import type { Message } from "../types/chat";
import { useParams } from "react-router-dom";

interface SideBarProp {
    isSidebarOpen: boolean;
    setIsSidebarOpen: Dispatch<SetStateAction<boolean>>;
}

const ChatPage = ({ isSidebarOpen, setIsSidebarOpen }: SideBarProp) => {
    const { id } = useParams();
    const isMobile = useIsMobile();
    const [messages, setMessages] = useState<Array<Message>>([]);

    return (
        <section className="w-full h-[calc(100vh-3.75rem)] flex overflow-hidden">
            <SideBar
                isSidebarOpen={isSidebarOpen}
                setIsSidebarOpen={setIsSidebarOpen}
            />

            <div
                className={`flex-1 min-w-0 flex flex-col ${isSidebarOpen && isMobile ? "hidden" : ""}`}
            >
                <ChatPanel
                    messages={messages}
                    setMessages={setMessages}
                    id={id || null}
                />
                <ChatInput
                    messages={messages}
                    setMessages={setMessages}
                    id={id || null}
                />
            </div>
        </section>
    );
};
export default ChatPage;
