import React, { useState, useEffect } from 'react';

function App() {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  useEffect(() => {
    fetchServices();
    const interval = setInterval(fetchServices, 30000);
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
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '16px' }}>
          <h2>Services</h2>
          <button onClick={fetchServices} style={{ backgroundColor: '#3B82F6', color: 'white', padding: '8px 16px', borderRadius: '6px' }}>
            Refresh
          </button>
        </div>

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
                  display: 'flex',
                  justifyContent: 'space-between',
                  padding: '16px 20px',
                  borderBottom: index < services.length - 1 ? '1px solid #E5E7EB' : 'none'
                }}
              >
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
