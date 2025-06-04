import React, { useEffect, useState } from "react";
import { getFollowUps } from "./api";

const App = () => {
  const [followUps, setFollowUps] = useState([]);

  useEffect(() => {
    async function fetchFollowUps() {
      const data = await getFollowUps();
      setFollowUps(data);
    }
    fetchFollowUps();
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Email Follow-Up Dashboard</h1>
      <ul>
        {followUps.map((f) => (
          <li key={f.id} className="border p-2 mb-2 rounded">
            <strong>{f.recipient}</strong> — {f.subject} <br />
            Follow-up on: <span className="text-blue-600">{f.followup_date}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default App;