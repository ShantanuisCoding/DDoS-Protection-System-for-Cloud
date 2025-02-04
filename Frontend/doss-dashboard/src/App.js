import { useEffect, useState } from "react";

function App() {
    const [alerts, setAlerts] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch("http://localhost:5000/detect_ddos")
            .then(res => {
                if (!res.ok) {
                    throw new Error(`HTTP error! Status: ${res.status}`);
                }
                return res.json();
            })
            .then(data => setAlerts(data.blocked_ips || [])) // Handle undefined response
            .catch(err => setError(err.message)); // Catch API errors
    }, []);

    return (
        <div>
            <h2>DDoS Attack Alerts</h2>
            {error && <p style={{ color: "red" }}>Error: {error}</p>}
            <ul>
                {alerts.length > 0 ? (
                    alerts.map((ip, index) => <li key={index}>Blocked IP: {ip}</li>)
                ) : (
                    <p>No blocked IPs detected.</p>
                )}
            </ul>
        </div>
    );
}

export default App;

// <!-- sudo hping3 -S --flood -p 80 192.168.1.1 -->