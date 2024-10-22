import React, { useRef, useState, useEffect } from 'react';
import '../styles/chatbot.css'; // Ensure the path is correct

interface Message {
    sender: 'user' | 'bot';
    content: string;
}

const Chatbot: React.FC = () => {
    const [isOpen, setIsOpen] = useState<boolean>(false);
    const [messages, setMessages] = useState<Message[]>([]);
    const [inputText, setInputText] = useState<string>('');
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const toggleChat = () => setIsOpen(!isOpen);

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setInputText(event.target.value);
    };

    const sendMessage = () => {
        if (!inputText.trim()) return;
        const newMessage: Message = { sender: 'user', content: inputText };
        setMessages([...messages, newMessage]);
        handleResponse();
        setInputText('');
    };

    const handleResponse = () => {
        // Define a list of responses
        const responses = [
            "Don't ask me, I don't know.",
            "You don't deserve to know that secret.",
            "Play more games and I'll tell you."
        ];
    
        // Randomly pick one response from the list
        const randomResponse = responses[Math.floor(Math.random() * responses.length)];
    
        const botMessage: Message = {
            sender: 'bot',
            content: randomResponse
        };
    
        // Set the message after a delay to simulate typing or processing time
        setTimeout(() => {
            setMessages(msgs => [...msgs, botMessage]);
        }, 1000);
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
                            <div key={index} className={`message ${msg.sender}`}>
                                {msg.content}
                            </div>
                        ))}
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
