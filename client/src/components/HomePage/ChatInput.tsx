import { useState } from "react";
import { HiArrowSmUp } from "react-icons/hi";

import type { KeyboardEvent, SubmitEvent } from "react";

const ChatInput = () => {
    const [input, setInput] = useState<string>("");

    const sendChat = async (e?: SubmitEvent) => {
        e?.preventDefault();
        if (!input.trim()) return;

        // sth later

        setInput("");
    };

    const handleKeyDown = async (e: KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key == "Enter" && !e.shiftKey) {
            e.preventDefault();
            await sendChat();
        }
    };

    return (
        <div>
            <form onSubmit={sendChat} className="w-full px-100 py-10">
                <div className="flex justify-center items-end bg-surface rounded-2xl p-5">
                    <textarea
                        name="chatbox"
                        placeholder="Ask anything..."
                        className="bg-transparent text-base w-full h-28
                                resize-none outline-none focus:ring-0 focus:border-none border-none
                                placeholder:text-muted
                                scrollbar-thin scrollbar-thumb-border-subtle/40 scrollbar-track-transparent"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                    ></textarea>
                    <button
                        type="submit"
                        disabled={!input.trim()}
                        className="ml-5 p-3 bg-brand hover:bg-brand-hover 
                                disabled:opacity-40 disabled:hover:bg-brand text-white 
                                rounded-full transition-all cursor-pointer border-none flex items-center justify-center"
                    >
                        <HiArrowSmUp />
                    </button>
                </div>
            </form>
        </div>
    );
};

export default ChatInput;
