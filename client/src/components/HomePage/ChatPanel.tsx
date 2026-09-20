import { useEffect, useRef } from "react";

import { GiMagicLamp } from "react-icons/gi";

import type { Message } from "../../types/chat";

interface ChatInfo {
    messages: Array<Message>;
}

const ChatPanel = ({ messages }: ChatInfo) => {
    const bottomRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({
            behavior: "smooth",
        });
    }, [messages]);

    return (
        <div className="w-full flex-1 p-6 flex flex-col gap-10 scrollbar-thin scrollbar-thumb-border-subtle/40 scrollbar-track-transparent text-lg overflow-y-auto">
            {messages.length === 0 ? (
                <div className="w-full h-full flex flex-col justify-center items-center gap-4 text-center text-4xl">
                    <GiMagicLamp size="3em" />
                    <div>Anything on your mind today?</div>
                </div>
            ) : (
                <div className="px-100">
                    {messages.map((message, index) =>
                        message.role === "human" ? (
                            <div
                                className="flex justify-end w-full"
                                key={index}
                            >
                                <div className="px-6 py-4 bg-surface rounded-4xl">
                                    {message.content}
                                </div>
                            </div>
                        ) : (
                            <div key={index}>
                                <div className="flex flex-col gap-1 text-gray-400 pb-4">
                                    {message.logs?.map((log, index) => (
                                        <div key={index}>{"> " + log}</div>
                                    ))}
                                </div>
                                <div>{message.content}</div>
                                <div className="flex flex-row gap-2 py-4 flex-wrap">
                                    {message.sources?.map((source, index) => (
                                        <a
                                            key={index}
                                            href={source}
                                            target="_blank"
                                            className="bg-surface py-2 px-4 rounded-4xl text-gray-400 text-sm"
                                        >
                                            {source}
                                        </a>
                                    ))}
                                </div>
                            </div>
                        ),
                    )}
                </div>
            )}
            <div ref={bottomRef}></div>
        </div>
    );
};

export default ChatPanel;
