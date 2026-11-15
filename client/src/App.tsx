import { useState, useEffect } from "react";
import {
    Route,
    createBrowserRouter,
    createRoutesFromElements,
    RouterProvider,
} from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import MainLayout from "./layouts/MainLayout";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import ChatPage from "./pages/ChatPage";

const App = () => {
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);

    useEffect(() => {
        const coldStartOnStartUp = async () => {
            try {
                // health check
                await fetch(import.meta.env.VITE_API_URL, {
                    method: "GET",
                });
            } catch (error) {
                alert(
                    "Please help us cold start the server. This will take a minute...",
                );
                window.location.href = import.meta.env.VITE_API_URL;
            }
        };

        coldStartOnStartUp();
    }, []);

    const router = createBrowserRouter(
        createRoutesFromElements(
            <Route path="/" element={<MainLayout />}>
                <Route
                    index
                    element={
                        <HomePage
                            isSidebarOpen={isSidebarOpen}
                            setIsSidebarOpen={setIsSidebarOpen}
                        />
                    }
                />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/signup" element={<SignupPage />} />
                <Route
                    path="/conversations/:id"
                    element={
                        <ChatPage
                            isSidebarOpen={isSidebarOpen}
                            setIsSidebarOpen={setIsSidebarOpen}
                        />
                    }
                />
            </Route>,
        ),
    );

    return (
        <AuthProvider>
            <RouterProvider router={router} />
        </AuthProvider>
    );
};

export default App;
