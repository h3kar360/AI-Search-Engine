import { useEffect, useRef, useState } from "react";
import { useListeningAuth } from "../../context/AuthContext";

import { GiMagicLamp } from "react-icons/gi";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";

import type { Message } from "../../types/chat";
import type { SetStateAction, Dispatch } from "react";

interface ChatInfo {
    messages: Array<Message>;
    setMessages: Dispatch<SetStateAction<Array<Message>>>;
    id: string | null;
}

const ChatPanel = ({ messages, setMessages, id }: ChatInfo) => {
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const bottomRef = useRef<HTMLDivElement>(null);
    const { user } = useListeningAuth();

    useEffect(() => {
        const getConversationHistory = async () => {
            setIsLoading(true);

            try {
                if (!user) return;

                const token = await user.getIdToken();

                const response = await fetch(
                    `${import.meta.env.VITE_API_URL}/api/${import.meta.env.VITE_API_VERSION}/conversations/${id}`,
                    {
                        method: "GET",
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    },
                );

                if (!response.ok)
                    throw new Error("Error fetching chat history");

                const { chats } = await response.json();

                setMessages(chats);
            } catch (error) {
                console.error(error);
            } finally {
                setIsLoading(false);
            }
        };

        getConversationHistory();
    }, [user, id]);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({
            behavior: "smooth",
        });
    }, [messages]);

    return (
        <div className="w-full flex-1 p-6 flex flex-col gap-10 scrollbar-thin scrollbar-thumb-border-subtle/40 scrollbar-track-transparent lg:text-lg sm:text-sm overflow-y-auto">
            {messages.length === 0 ? (
                <div className="w-full h-full flex flex-col justify-center items-center gap-4 text-center text-4xl">
                    <GiMagicLamp size="3em" />
                    <div>Anything on your mind today?</div>
                </div>
            ) : (
                <div className="w-full max-w-3xl mx-auto">
                    {messages.map((message, index) =>
                        message.role === "human" ? (
                            <div
                                className="flex justify-end w-full"
                                key={index}
                            >
                                <div className="px-6 py-4 bg-surface rounded-4xl my-2">
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
                                <div>
                                    <Markdown
                                        remarkPlugins={[remarkGfm, remarkMath]}
                                        rehypePlugins={[rehypeKatex]}
                                    >
                                        {message.content}
                                    </Markdown>
                                </div>
                                <div className="flex flex-row gap-2 py-4 flex-wrap">
                                    {message.sources?.map((source, index) => (
                                        <a
                                            key={index}
                                            href={source}
                                            target="_blank"
                                            className="bg-surface py-2 px-4 rounded-4xl text-gray-400 text-sm max-w-60 truncate"
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
