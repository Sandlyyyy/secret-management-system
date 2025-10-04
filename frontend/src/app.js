import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [requests, setRequests] = useState([]);
  const [newRequest, setNewRequest] = useState({
    secret_name: '',
    secret_type: 'database',
    justification: ''
  });

  useEffect(() => {
    fetchRequests();
  }, []);

  const fetchRequests = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/secret-requests');
      setRequests(response.data);
    } catch (error) {
      console.error('Error fetching requests:', error);
    }
  };

  const createRequest = async () => {
    try {
      await axios.post('http://localhost:8000/api/secret-requests', newRequest);
      setNewRequest({ secret_name: '', secret_type: 'database', justification: '' });
      fetchRequests();
    } catch (error) {
      console.error('Error creating request:', error);
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h1>🔐 Secret Management System - Demo</h1>
      
      <div style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ccc' }}>
        <h3>Create Secret Request</h3>
        <input
          type="text"
          placeholder="Secret Name"
          value={newRequest.secret_name}
          onChange={(e) => setNewRequest({...newRequest, secret_name: e.target.value})}
          style={{ margin: '5px', padding: '8px' }}
        />
        <select
          value={newRequest.secret_type}
          onChange={(e) => setNewRequest({...newRequest, secret_type: e.target.value})}
          style={{ margin: '5px', padding: '8px' }}
        >
          <option value="database">Database</option>
          <option value="api">API Key</option>
          <option value="ssh">SSH Key</option>
        </select>
        <textarea
          placeholder="Justification"
          value={newRequest.justification}
          onChange={(e) => setNewRequest({...newRequest, justification: e.target.value})}
          style={{ margin: '5px', padding: '8px', width: '300px' }}
        />
        <button onClick={createRequest} style={{ margin: '5px', padding: '8px 16px' }}>
          Create Request
        </button>
      </div>

      <div>
        <h3>Secret Requests</h3>
        <table border="1" style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Secret Name</th>
              <th>Type</th>
              <th>Status</th>
              <th>Created</th>
            </tr>
          </thead>
          <tbody>
            {requests.map(req => (
              <tr key={req.id}>
                <td>{req.id}</td>
                <td>{req.secret_name}</td>
                <td>{req.secret_type}</td>
                <td>{req.status}</td>
                <td>{new Date(req.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;