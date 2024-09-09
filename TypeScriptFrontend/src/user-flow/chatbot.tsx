import React, { useRef, useState, useEffect } from 'react';
import '../../styles/chatbot.css'; // Ensure the path is correct
import config from '../env-config';

import Markdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface Message {
    role: 'user' | 'assistant' | 'system';
    content: string;
    refusal?: string;
}

const INTRO_CHAT: Message = {role: "assistant", content: "Hi, I'm here to help you with any questions about Durb! Ask me anything..."}

const Chatbot: React.FC = () => {
    const [isOpen, setIsOpen] = useState<boolean>(false);
    const [messages, setMessages] = useState<Message[]>([INTRO_CHAT]);
    const [inputText, setInputText] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const toggleChat = () => setIsOpen(!isOpen);

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setInputText(event.target.value);
    };

    const sendMessage = async () => {
        if (!inputText.trim()) return;
        const newMessage: Message = { role: 'user', content: inputText };
        setMessages([...messages, newMessage]);
        setInputText('');
        setLoading(true);

        try {
            const token = localStorage.getItem('userToken');
            const response = await fetch(`${config.userBackend}chat/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: newMessage.content
            });
            const data = await response.json();
            if (!response.ok) {
                throw new Error('Failed to connect to the server.');
            }

            const botResponse: Message = data.response;
            setMessages(msgs => [...msgs, botResponse]);
        } catch (error) {
            console.error('Failed to connect to the server:', error);
            const errorResponse: Message = {
                role: 'assistant',
                content: 'Sorry, I am unable to process your request at the moment.'
            };
            setMessages(msgs => [...msgs, errorResponse]);
        } finally {
            setLoading(false);
        }
    };

    const resetChat = async () => {
        setMessages([INTRO_CHAT]);

        try {
            const token = localStorage.getItem('userToken');
            fetch(`${config.userBackend}chat/reset`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });
        } catch (error) {
            console.error('Failed to connect to the server:', error);
        }
    }

    // Scroll to the bottom of the messages container whenever messages update
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    useEffect(() => {

        async function loadChat() {
            setLoading(true);
            try {
                const token = localStorage.getItem('userToken');
                const response = await fetch(`${config.userBackend}chat/`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                });
                const data = await response.json();
                if (!response.ok) {
                    throw new Error('Failed to connect to the server.');
                }

                let chat: Message[] = data;
                chat = chat.filter((msg: Message) => msg.role != 'system');
                setMessages(chat);
            } catch (error) {
                console.error('Failed to connect to the server:', error);
                const errorResponse: Message = {
                    role: 'assistant',
                    content: 'Sorry, I am unable to process your request at the moment.'
                };
                setMessages(msgs => [...msgs, errorResponse]);
            } finally {
                setLoading(false);
            }
        }

        loadChat();
    }, []);


    return (
        <div className={`chatbot ${isOpen ? 'open' : 'closed'}`}>
            {isOpen ? (
                <div className="chat-window">
                    <div className="header">
                        <span className="header-title">Ask me anything</span>
                        <div className="btn-container">
                            <button onClick={resetChat} className="btn reset-btn">Reset</button>
                            <button onClick={toggleChat} className="btn close-btn">Close</button>
                        </div>
                    </div>
                    <div className="messages">
                        {messages.map((msg, index) => (
                            <div key={index} className={`message-ctr ${msg.role}`}>
                                <Markdown key={index} className={`message ${msg.role}`} remarkPlugins={[remarkGfm]}>
                                    {msg.content}
                                </Markdown>
                            </div>
                        ))}
                        {loading && <div className="message assistant">...</div>}
                        <div ref={messagesEndRef} />
                    </div>
                    <div className="input-area">
                        <input
                            type="text"
                            placeholder="Ask me anything..."
                            className="chat-input"
                            value={inputText}
                            onChange={handleInputChange}
                            onKeyDown={event => event.key === 'Enter' && sendMessage()}
                        />
                        <button onClick={sendMessage} className="send-btn">Send</button>
                    </div>
                </div>
            ) : (
                <button onClick={toggleChat} className="chat-toggle">Any Questions?</button>
            )}
        </div>
    );
};

export default Chatbot;
