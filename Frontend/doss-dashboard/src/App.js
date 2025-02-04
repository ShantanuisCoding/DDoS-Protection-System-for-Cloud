import { useEffect, useState } from "react";

function App() {
    const [alerts, setAlerts] = useState([]);

    useEffect(() => {
        fetch("http://localhost:5000/detect_ddos")
            .then(res => {
                if (!res.ok) {
                    throw new Error('Network response was not ok');
                }
                return res.json();
            })
            .then(data => setAlerts(data.blocked_ips))
            .catch(error => console.error('Fetch error:', error));
    }, []);

    return (
        <div>
            <h2>DDoS Attack Alerts</h2>
            <ul>
                {alerts.map((ip, index) => (
                    <li key={index}>Blocked IP: {ip}</li>
                ))}
            </ul>
        </div>
    );
}

export default App;
