import { useState } from "react"
import axios from "axios"

const API = "http://localhost:8000"

export default function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const [sessionId] = useState("user_" + Date.now())

  const sendMessage = async () => {
    if (!input.trim() || loading) return

    const userMsg = { role: "user", content: input }
    setMessages(prev => [...prev, userMsg])
    setInput("")
    setLoading(true)

    try {
      const res = await axios.post(`${API}/chat`, {
        message: input,
        session_id: sessionId
      })

      const agentMsg = {
        role: "assistant",
        content: res.data.answer,
        steps: res.data.steps
      }
      setMessages(prev => [...prev, agentMsg])
    } catch (err) {
      setMessages(prev => [...prev, {
        role: "assistant",
        content: "Error: Could not connect to backend."
      }])
    }
    setLoading(false)
  }

  const uploadDoc = async () => {
    const text = prompt("Paste your document text:")
    if (!text) return
    const docId = "doc_" + Date.now()
    await axios.post(`${API}/upload?doc_id=${docId}&text=${encodeURIComponent(text)}`)
    alert("Document uploaded!")
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h2 style={styles.title}>AutoAssist Agent</h2>
        <button onClick={uploadDoc} style={styles.uploadBtn}>Upload Doc</button>
      </div>

      <div style={styles.messages}>
        {messages.length === 0 && (
          <div style={styles.welcome}>Ask me anything. I can search documents, analyze data, and browse the web.</div>
        )}
        {messages.map((msg, i) => (
          <div key={i} style={msg.role === "user" ? styles.userMsg : styles.agentMsg}>
            <div style={styles.msgContent}>{msg.content}</div>
            {msg.steps && msg.steps.length > 0 && (
              <div style={styles.steps}>
                {msg.steps.map((step, j) => (
                  <div key={j} style={styles.step}>
                    🔧 Used <b>{step.tool}</b>: {JSON.stringify(step.input)}
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
        {loading && <div style={styles.agentMsg}>Thinking...</div>}
      </div>

      <div style={styles.inputRow}>
        <input
          style={styles.input}
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && sendMessage()}
          placeholder="Ask me anything..."
        />
        <button onClick={sendMessage} style={styles.sendBtn} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  )
}

const styles = {
  container: { display: "flex", flexDirection: "column", height: "100vh", maxWidth: 800, margin: "0 auto", fontFamily: "sans-serif" },
  header: { display: "flex", justifyContent: "space-between", alignItems: "center", padding: "16px", borderBottom: "1px solid #eee" },
  title: { margin: 0, fontSize: 20 },
  uploadBtn: { padding: "8px 16px", background: "#6366f1", color: "white", border: "none", borderRadius: 8, cursor: "pointer" },
  messages: { flex: 1, overflowY: "auto", padding: 16, display: "flex", flexDirection: "column", gap: 12 },
  welcome: { textAlign: "center", color: "#999", marginTop: 40 },
  userMsg: { alignSelf: "flex-end", background: "#6366f1", color: "white", padding: "10px 14px", borderRadius: "18px 18px 4px 18px", maxWidth: "70%" },
  agentMsg: { alignSelf: "flex-start", background: "#f3f4f6", padding: "10px 14px", borderRadius: "18px 18px 18px 4px", maxWidth: "80%" },
  msgContent: { lineHeight: 1.5 },
  steps: { marginTop: 8, fontSize: 12, color: "#666" },
  step: { padding: "4px 0" },
  inputRow: { display: "flex", gap: 8, padding: 16, borderTop: "1px solid #eee" },
  input: { flex: 1, padding: "10px 14px", borderRadius: 8, border: "1px solid #ddd", fontSize: 14 },
  sendBtn: { padding: "10px 20px", background: "#6366f1", color: "white", border: "none", borderRadius: 8, cursor: "pointer" }
}