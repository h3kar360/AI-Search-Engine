import { useState } from "react";

import ChatPanel from "../components/HomePage/ChatPanel";
import ChatInput from "../components/HomePage/ChatInput";

import type { Message } from "../types/chat";

const HomePage = () => {
    const [messages, setMessages] = useState<Array<Message>>([]);

    return (
        <section className="w-full h-[calc(100vh-3.75rem)] flex flex-col">
            <ChatPanel messages={messages} />
            <ChatInput messages={messages} setMessages={setMessages} />
        </section>
    );
};

export default HomePage;
