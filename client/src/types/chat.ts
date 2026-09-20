export interface Message {
    role: "human" | "ai";
    content: string;
    logs?: Array<string>;
    sources?: Array<string>;
    status?: "thinking" | "completed" | "error" | "responding";
}

export type ConversationState = "idle" | "loading" | "error";
