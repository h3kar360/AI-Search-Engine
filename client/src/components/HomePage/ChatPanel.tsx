import { GiMagicLamp } from "react-icons/gi";

const ChatPanel = () => {
    return (
        <div className="w-full h-full flex justify-center items-center text-4xl flex-col gap-2">
            <GiMagicLamp size="3em" />
            <div>Anything on your mind today?</div>
        </div>
    );
};

export default ChatPanel;
