import { useEffect, useRef, useState, useLayoutEffect } from "react";
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
    newMessage: boolean;
    setNewMessage: Dispatch<SetStateAction<boolean>>;
    messages: Array<Message>;
    setMessages: Dispatch<SetStateAction<Array<Message>>>;
    id: string | null;
}

const ChatPanel = ({
    newMessage,
    setNewMessage,
    messages,
    setMessages,
    id,
}: ChatInfo) => {
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [page, setPage] = useState<number>(1);
    const [hasMore, setHasMore] = useState<boolean>(true);
    const bottomRef = useRef<HTMLDivElement>(null);
    const chatRef = useRef<HTMLDivElement>(null);
    const prevScrollRef = useRef<{ height: number; top: number } | null>(null);
    const { user } = useListeningAuth();

    // initial chat history render
    useEffect(() => {
        const getConversationHistory = async () => {
            setIsLoading(true);

            try {
                if (!user) return;

                const token = await user.getIdToken();

                const response = await fetch(
                    `${import.meta.env.VITE_API_URL}/api/${import.meta.env.VITE_API_VERSION}/conversations/${id}?page=1&limit=10`,
                    {
                        method: "GET",
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    },
                );

                if (!response.ok)
                    throw new Error("Error fetching chat history");

                const { chats, pagination } = await response.json();

                setMessages(chats);
                setPage(pagination.next_page);
                setHasMore(pagination.has_more);
                setNewMessage((prevBool) => !prevBool);
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
    }, [newMessage]);

    useLayoutEffect(() => {
        const chatPanel = chatRef.current;
        const previous = prevScrollRef.current;

        if (!chatPanel || !previous) return;

        const heightDifference = chatPanel.scrollHeight - previous.height;

        chatPanel.scrollTop = previous.top + heightDifference;

        prevScrollRef.current = null;
    }, [messages]);

    const handleScroll = async () => {
        const chatPanel = chatRef.current;

        if (!chatPanel) return;

        const scrollTop = chatPanel.scrollTop;

        if (scrollTop <= 50 && hasMore) {
            setIsLoading(true);

            prevScrollRef.current = {
                height: chatPanel.scrollHeight,
                top: chatPanel.scrollTop,
            };

            try {
                if (!user) return;

                const token = await user.getIdToken();

                const response = await fetch(
                    `${import.meta.env.VITE_API_URL}/api/${import.meta.env.VITE_API_VERSION}/conversations/${id}?page=${page}&limit=10`,
                    {
                        method: "GET",
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    },
                );

                if (!response.ok)
                    throw new Error("Error fetching chat history");

                const { chats, pagination } = await response.json();

                setMessages((currMessages) => [...chats, ...currMessages]);
                setPage(pagination.next_page);
                setHasMore(pagination.has_more);
            } catch (error) {
                console.error(error);
            } finally {
                setIsLoading(false);
            }
        }
    };

    return (
        <div
            className="w-full flex-1 p-6 flex flex-col gap-10 scrollbar-thin scrollbar-thumb-border-subtle/40 scrollbar-track-transparent lg:text-lg sm:text-sm overflow-y-auto"
            ref={chatRef}
            onScroll={handleScroll}
        >
            {isLoading ? <p>loading chats...</p> : <p></p>}
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
