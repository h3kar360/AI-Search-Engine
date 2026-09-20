import { useState } from "react";
import { HiArrowSmUp } from "react-icons/hi";

import type {
    KeyboardEvent,
    SetStateAction,
    SubmitEvent,
    Dispatch,
} from "react";
import type { Message } from "../../types/chat";

interface ChatInfo {
    messages: Array<Message>;
    setMessages: Dispatch<SetStateAction<Array<Message>>>;
}

const ChatInput = ({ messages, setMessages }: ChatInfo) => {
    const [input, setInput] = useState<string>("");
    const [isLoading, setIsLoading] = useState<boolean>(false);

    const handleSubmit = async () => {
        if (!input.trim() || isLoading) return;

        // only for guests
        const guestMessage =
            "context:\n" +
            messages
                .map((message) => `${message.role}: ${message.content}`)
                .join("\n") +
            `\n\nThis is the query:${input}`;

        // convert state to form data
        const formData = new FormData();
        formData.append("user_message", guestMessage);

        const humanMessage: Message = {
            role: "human",
            content: input,
        };

        const aiMessage: Message = {
            role: "ai",
            content: "",
        };

        setInput("");

        // set human message (which is the user query) added into the messages, and initialize the AI message
        setMessages((prevMessages) => [
            ...prevMessages,
            humanMessage,
            aiMessage,
        ]);

        try {
            setIsLoading(true);

            const response = await fetch(
                `${import.meta.env.VITE_API_URL}/api/v1/conversations/chat`,
                {
                    method: "POST",
                    body: formData,
                },
            );

            if (!response.ok)
                throw new Error(`HTTP Error, status=${response.status}`);
            if (!response.body) throw new Error("No response body received");

            // open streaming
            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            let buffer = "";

            while (true) {
                const { done, value } = await reader.read();

                if (done) break;

                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split("\n");

                buffer = lines.pop() || "";

                for (const line of lines) {
                    if (!line.startsWith("data: ")) {
                        console.log(line);
                        continue;
                    }

                    try {
                        const data = JSON.parse(line.slice(6));

                        if (data.type === "custom") {
                            const { log } = data;

                            setMessages((prevMessages): Array<Message> => {
                                if (prevMessages.length === 0)
                                    return prevMessages;

                                const pastMessages = prevMessages.slice(0, -1);
                                const lastMessage = prevMessages.at(-1);

                                if (!lastMessage || lastMessage.role !== "ai")
                                    return prevMessages;

                                return [
                                    ...pastMessages,
                                    {
                                        ...lastMessage,
                                        logs: [
                                            ...(lastMessage.logs || []),
                                            log,
                                        ],
                                        status: "thinking",
                                    },
                                ];
                            });
                        } else if (
                            data.type === "messages" &&
                            data.message !== ""
                        ) {
                            const { message, role, node, additional_kwargs } =
                                data;

                            setMessages((prevMessages): Array<Message> => {
                                if (prevMessages.length === 0)
                                    return prevMessages;

                                const pastMessages = prevMessages.slice(0, -1);
                                const lastMessage = prevMessages.at(-1);

                                if (!lastMessage || lastMessage.role !== "ai")
                                    return prevMessages;

                                if (
                                    role == "AIMessageChunk" &&
                                    message.length > 0 &&
                                    node == "generate_answer"
                                ) {
                                    return [
                                        ...pastMessages,
                                        {
                                            ...lastMessage,
                                            content:
                                                lastMessage.content +
                                                message[0].text,
                                            status: "responding",
                                        },
                                    ];
                                } else if (role == "ai") {
                                    return [
                                        ...pastMessages,
                                        {
                                            ...lastMessage,
                                            content: message[0].text || message,
                                            logs: [],
                                            sources:
                                                additional_kwargs?.sources ||
                                                [],
                                            status: "completed",
                                        },
                                    ];
                                }

                                return [...prevMessages];
                            });
                        }

                        buffer += decoder.decode();
                    } catch (error) {
                        console.error(error);
                    }
                }
            }
        } catch (error) {
            console.error(error);
        } finally {
            setIsLoading(false);
        }
    };

    const sendChat = async (e: SubmitEvent) => {
        e.preventDefault();
        await handleSubmit();
    };

    const handleKeyDown = async (e: KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key == "Enter" && !e.shiftKey) {
            e.preventDefault();
            await handleSubmit();
        }
    };

    return (
        <div className="relative w-full">
            <div
                className="absolute -top-15 left-0 right-0 h-15 bg-gradient-to-t from-canvas via-canvas/70 to-transparent pointer-events-none z-10"
                aria-hidden="true"
            />

            <form
                onSubmit={sendChat}
                className="relative z-20 w-full max-w-3xl mx-auto py-5 px-4 bg-canvas"
            >
                <div className="flex justify-center items-end bg-surface rounded-2xl p-5 border border-border-subtle/50 shadow-2xl">
                    <textarea
                        name="chatMessage"
                        placeholder="Ask anything..."
                        className="bg-transparent text-lg w-full h-28
                                    resize-none outline-none focus:ring-0 border-none
                                    placeholder:text-muted
                                    scrollbar-thin scrollbar-thumb-border-subtle/40 scrollbar-track-transparent"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                    />
                    <button
                        type="submit"
                        disabled={!input.trim() || isLoading}
                        className="ml-5 p-3 bg-brand hover:bg-brand-hover 
                                    disabled:opacity-40 disabled:hover:bg-brand text-white 
                                    rounded-full transition-all cursor-pointer border-none flex items-center justify-center"
                    >
                        <HiArrowSmUp className="text-xl" />
                    </button>
                </div>
            </form>
        </div>
    );
};

export default ChatInput;
