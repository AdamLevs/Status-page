import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

function App() {
  const [services, setServices] = useState([]);
  const [form, setForm] = useState({ name: '', check_type: 'HTTP', check_target: '', frequency: 60 });

  useEffect(() => {
    fetchServices();
  }, []);

  const fetchServices = () => {
    axios.get(`${API_URL}/services`)
      .then(res => setServices(res.data))
      .catch(console.error);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post(`${API_URL}/services`, form)
      .then(() => {
        fetchServices();
        setForm({ name: '', check_type: 'HTTP', check_target: '', frequency: 60 });
      })
      .catch(console.error);
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Status Page</h1>

      <form onSubmit={handleSubmit}>
        <input placeholder="Name" value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} />
        <select value={form.check_type} onChange={e => setForm({ ...form, check_type: e.target.value })}>
          <option value="HTTP">HTTP</option>
          <option value="PING">PING</option>
          <option value="TCP">TCP</option>
          <option value="DNS">DNS</option>
        </select>
        <input placeholder="Target" value={form.check_target} onChange={e => setForm({ ...form, check_target: e.target.value })} />
        <input placeholder="Frequency" type="number" value={form.frequency} onChange={e => setForm({ ...form, frequency: parseInt(e.target.value) })} />
        <button type="submit">Add Service</button>
      </form>

      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Target</th>
            <th>Frequency</th>
          </tr>
        </thead>
        <tbody>
          {services.map(service => (
            <tr key={service.id}>
              <td>{service.name}</td>
              <td>{service.check_type}</td>
              <td>{service.check_target}</td>
              <td>{service.frequency}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
