import ChatPanel from "../components/HomePage/ChatPanel";
import ChatInput from "../components/HomePage/ChatInput";

const HomePage = () => {
    return (
        <section className="w-full h-[calc(100vh-3.75rem)] flex flex-col">
            <ChatPanel />
            <ChatInput />
        </section>
    );
};

export default HomePage;
