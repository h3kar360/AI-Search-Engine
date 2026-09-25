import { useState } from "react";

import ChatPanel from "../components/HomePage/ChatPanel";
import ChatInput from "../components/HomePage/ChatInput";
import SideBar from "../components/HomePage/SideBar";

import type { Message } from "../types/chat";

const HomePage = () => {
    const [messages, setMessages] = useState<Array<Message>>([]);

    return (
        <section className="w-full h-[calc(100vh-3.75rem)] flex">
            <div>
                <SideBar />
            </div>
            <div className="flex flex-col w-full">
                <ChatPanel messages={messages} />
                <ChatInput messages={messages} setMessages={setMessages} />
            </div>
        </section>
    );
};

export default HomePage;
