"use client";
import { useState, useRef, useEffect } from "react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

const SUGGESTED_QUESTIONS = [
  "What are the hospital visiting hours?",
  "What should I know about ibuprofen?",
  "How do I manage a fever at home?",
  "How do I book an appointment?",
];

export default function MediAssist() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function sendMessage(text?: string) {
    const query = text || input.trim();
    if (!query || loading) return;
    setInput("");
    setLoading(true);

    const newMessages: Message[] = [
      ...messages,
      { role: "user", content: query },
    ];
    setMessages(newMessages);

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/chat`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            message: query,
            history: messages.slice(-6),
          }),
        }
      );

      const reader = response.body!.getReader();
      const decoder = new TextDecoder();
      let assistantText = "";

      setMessages([...newMessages, { role: "assistant", content: "" }]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value);
        const lines = chunk.split("\n");
        for (const line of lines) {
          if (line.startsWith("data: ") && !line.includes("[DONE]")) {
            try {
              const data = JSON.parse(line.replace("data: ", ""));
              if (data.text) {
                assistantText += data.text;
                setMessages((prev) => {
                  const updated = [...prev];
                  updated[updated.length - 1] = {
                    role: "assistant",
                    content: assistantText,
                  };
                  return updated;
                });
              }
            } catch {}
          }
        }
      }
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Sorry, something went wrong. Please try again.",
        },
      ]);
    }
    setLoading(false);
  }

  return (
    <div className="flex flex-col h-screen" style={{ background: "#f0f4f8" }}>

      {/* Header */}
      <div style={{
        background: "linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%)",
        padding: "16px 24px",
        display: "flex",
        alignItems: "center",
        gap: "12px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.2)"
      }}>
        <div style={{
          width: "42px", height: "42px",
          background: "rgba(255,255,255,0.2)",
          borderRadius: "12px",
          display: "flex", alignItems: "center", justifyContent: "center",
          fontSize: "22px"
        }}>🏥</div>
        <div>
          <h1 style={{ color: "#ffffff", fontSize: "18px", fontWeight: "700", margin: 0 }}>
            MediAssist
          </h1>
          <p style={{ color: "rgba(255,255,255,0.75)", fontSize: "12px", margin: 0 }}>
            AI-powered healthcare knowledge assistant
          </p>
        </div>
        <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: "6px" }}>
          <div style={{ width: "8px", height: "8px", background: "#4ade80", borderRadius: "50%" }}></div>
          <span style={{ color: "rgba(255,255,255,0.75)", fontSize: "12px" }}>Online</span>
        </div>
      </div>

      {/* Chat area */}
      <div style={{ flex: 1, overflowY: "auto", padding: "24px 16px" }}>
        <div style={{ maxWidth: "720px", margin: "0 auto" }}>

          {messages.length === 0 && (
            <div style={{ textAlign: "center", marginTop: "48px" }}>
              <div style={{
                width: "72px", height: "72px",
                background: "linear-gradient(135deg, #1e3a5f, #2563eb)",
                borderRadius: "20px",
                display: "flex", alignItems: "center", justifyContent: "center",
                margin: "0 auto 16px",
                fontSize: "32px"
              }}>🏥</div>
              <h2 style={{ fontSize: "24px", fontWeight: "700", color: "#1e293b", marginBottom: "8px" }}>
                How can I help you today?
              </h2>
              <p style={{ color: "#64748b", fontSize: "14px", marginBottom: "32px" }}>
                Ask about medications, symptoms, appointments, or hospital policies.
              </p>
              <div style={{
                display: "grid", gridTemplateColumns: "1fr 1fr",
                gap: "12px", maxWidth: "560px", margin: "0 auto"
              }}>
                {SUGGESTED_QUESTIONS.map((q) => (
                  <button
                    key={q}
                    onClick={() => sendMessage(q)}
                    style={{
                      textAlign: "left",
                      padding: "14px 16px",
                      background: "#ffffff",
                      border: "1.5px solid #e2e8f0",
                      borderRadius: "12px",
                      fontSize: "13px",
                      color: "#1e293b",
                      cursor: "pointer",
                      transition: "all 0.15s",
                      fontWeight: "500",
                      lineHeight: "1.4"
                    }}
                    onMouseEnter={e => {
                      (e.target as HTMLElement).style.borderColor = "#2563eb";
                      (e.target as HTMLElement).style.background = "#eff6ff";
                    }}
                    onMouseLeave={e => {
                      (e.target as HTMLElement).style.borderColor = "#e2e8f0";
                      (e.target as HTMLElement).style.background = "#ffffff";
                    }}
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          )}

          <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
            {messages.map((msg, i) => (
              <div key={i} style={{
                display: "flex",
                justifyContent: msg.role === "user" ? "flex-end" : "flex-start",
                gap: "10px",
                alignItems: "flex-start"
              }}>
                {msg.role === "assistant" && (
                  <div style={{
                    width: "34px", height: "34px", flexShrink: 0,
                    background: "linear-gradient(135deg, #1e3a5f, #2563eb)",
                    borderRadius: "10px",
                    display: "flex", alignItems: "center", justifyContent: "center",
                    fontSize: "16px", marginTop: "2px"
                  }}>🏥</div>
                )}
                <div style={{
                  maxWidth: "75%",
                  padding: "12px 16px",
                  borderRadius: msg.role === "user" ? "18px 18px 4px 18px" : "18px 18px 18px 4px",
                  background: msg.role === "user"
                    ? "linear-gradient(135deg, #1e3a5f, #2563eb)"
                    : "#ffffff",
                  color: msg.role === "user" ? "#ffffff" : "#1e293b",
                  fontSize: "14px",
                  lineHeight: "1.6",
                  boxShadow: msg.role === "user"
                    ? "0 2px 8px rgba(37,99,235,0.3)"
                    : "0 2px 8px rgba(0,0,0,0.08)",
                  whiteSpace: "pre-wrap",
                  border: msg.role === "assistant" ? "1px solid #e2e8f0" : "none"
                }}>
                  {msg.content || (
                    <span style={{ display: "flex", gap: "4px" }}>
                      {[0, 1, 2].map(i => (
                        <span key={i} style={{
                          width: "6px", height: "6px",
                          background: "#94a3b8",
                          borderRadius: "50%",
                          display: "inline-block",
                          animation: `bounce 1s infinite ${i * 0.15}s`
                        }}/>
                      ))}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
          <div ref={bottomRef} />
        </div>
      </div>

      {/* Disclaimer */}
      <div style={{ textAlign: "center", padding: "6px 16px" }}>
        <p style={{ fontSize: "11px", color: "#94a3b8", margin: 0 }}>
          MediAssist provides general information only. Always consult a healthcare professional for medical advice.
        </p>
      </div>

      {/* Input area */}
      <div style={{
        background: "#ffffff",
        borderTop: "1px solid #e2e8f0",
        padding: "16px",
        boxShadow: "0 -2px 8px rgba(0,0,0,0.06)"
      }}>
        <div style={{
          maxWidth: "720px", margin: "0 auto",
          display: "flex", gap: "10px", alignItems: "center"
        }}>
          <input
            style={{
              flex: 1,
              border: "2px solid #e2e8f0",
              borderRadius: "12px",
              padding: "12px 16px",
              fontSize: "14px",
              outline: "none",
              color: "#1e293b",
              background: "#f8fafc",
              transition: "border-color 0.15s",
              fontFamily: "inherit"
            }}
            placeholder="Ask a health question..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            onFocus={e => (e.target.style.borderColor = "#2563eb")}
            onBlur={e => (e.target.style.borderColor = "#e2e8f0")}
            disabled={loading}
          />
          <button
            onClick={() => sendMessage()}
            disabled={loading || !input.trim()}
            style={{
              background: loading || !input.trim()
                ? "#94a3b8"
                : "linear-gradient(135deg, #1e3a5f, #2563eb)",
              color: "#ffffff",
              border: "none",
              borderRadius: "12px",
              padding: "12px 24px",
              fontSize: "14px",
              fontWeight: "600",
              cursor: loading || !input.trim() ? "not-allowed" : "pointer",
              transition: "opacity 0.15s",
              fontFamily: "inherit",
              whiteSpace: "nowrap"
            }}
          >
            {loading ? "..." : "Send →"}
          </button>
        </div>
      </div>

      <style>{`
        @keyframes bounce {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-4px); }
        }
      `}</style>
    </div>
  );
}