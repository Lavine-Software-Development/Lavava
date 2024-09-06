import React, { useRef, useState, useEffect } from 'react';
import '../../styles/chatbot.css'; // Ensure the path is correct
import config from '../env-config';

import Markdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface Message {
    role: 'user' | 'assistant';
    content: string;
    refusal?: string;
}

const Chatbot: React.FC = () => {
    const [isOpen, setIsOpen] = useState<boolean>(false);
    const [messages, setMessages] = useState<Message[]>([]);
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

    // Scroll to the bottom of the messages container whenever messages update
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    return (
        <div className={`chatbot ${isOpen ? 'open' : 'closed'}`}>
            {isOpen ? (
                <div className="chat-window">
                    <div className="header">
                        <span className="header-title">Ask me anything</span>
                        <button onClick={toggleChat} className="close-btn">Close</button>
                    </div>
                    <div className="messages">
                        {messages.map((msg, index) => (
                            <Markdown key={index} className={`message ${msg.role}`} remarkPlugins={[remarkGfm]}>
                                {msg.content}
                            </Markdown>
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
