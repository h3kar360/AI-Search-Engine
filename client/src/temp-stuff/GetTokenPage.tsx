import { useState, useEffect } from "react";
import { useListeningAuth } from "../context/AuthContext";

const GetTokenPage = () => {
    const { user } = useListeningAuth();
    const [token, setToken] = useState<string>("");

    useEffect(() => {
        const getToken = async () => {
            if (!user) return;

            const token = await user.getIdToken();
            setToken(token);
            console.log(token);
        };

        getToken();
    }, [user]);

    return <div>{token}</div>;
};

export default GetTokenPage;
