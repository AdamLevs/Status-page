import React, { useState, useEffect } from 'react';

function App() {
  const [services, setServices] = useState([]);
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  useEffect(() => {
    fetchServices();
    const interval = setInterval(fetchServices, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchServices = async () => {
    try {
      const response = await fetch('/api/public');
      if (!response.ok) {
        throw new Error('Failed to fetch services');
      }
      const data = await response.json();
      setServices(data);
      setError(null);
      setLastUpdated(new Date());

      for (const service of data) {
        if (service.status === 'UP') {
          const res = await fetch(`/api/services/${service.id}/stats`);
          if (res.ok) {
            const statData = await res.json();
            setStats(prev => ({ ...prev, [service.id]: statData }));
          }
        }
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    if (status === 'UP') return '#10B981';
    if (status === 'DOWN') return '#EF4444';
    return '#FBBF24';
  };

  const getStatusText = (status) => {
    if (status === 'UP') return 'Operational';
    if (status === 'DOWN') return 'Down';
    return 'Unknown';
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <div>Loading...</div>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <header style={{ textAlign: 'center', marginBottom: '40px' }}>
        <h1>Service Status</h1>
        <p>Current operational status of services</p>
      </header>

      {error && (
        <div style={{ backgroundColor: '#FEE2E2', color: '#DC2626', padding: '12px', borderRadius: '8px', marginBottom: '20px' }}>
          Error: {error}
        </div>
      )}

      <div>
        <h2 style={{ marginBottom: '16px' }}>Services</h2>

        {services.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px' }}>
            No services configured yet
          </div>
        ) : (
          <div style={{ border: '1px solid #E5E7EB', borderRadius: '8px' }}>
            {services.map((service, index) => (
              <div
                key={index}
                style={{
                  padding: '16px 20px',
                  borderBottom: index < services.length - 1 ? '1px solid #E5E7EB' : 'none'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <h3>{service.name}</h3>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <div
                      style={{
                        width: '12px',
                        height: '12px',
                        borderRadius: '50%',
                        backgroundColor: getStatusColor(service.status)
                      }}
                    />
                    <span style={{ color: getStatusColor(service.status) }}>
                      {getStatusText(service.status)}
                    </span>
                  </div>
                </div>

                {/* Extra Monitoring Info */}
                {stats[service.id] && (
                  <div style={{ marginTop: '10px', fontSize: '0.9em', color: '#374151' }}>
                    <p>🧠 CPU Usage: {stats[service.id].cpu_usage ?? 'N/A'}%</p>
                    <p>💾 RAM Usage: {stats[service.id].memory_usage ?? 'N/A'}%</p>
                    <p>🗄️ Disk Usage: {stats[service.id].disk_usage ?? 'N/A'}%</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      <footer style={{ textAlign: 'center', marginTop: '40px' }}>
        Last updated: {lastUpdated ? lastUpdated.toLocaleString() : 'N/A'}
      </footer>
    </div>
  );
}

export default App;