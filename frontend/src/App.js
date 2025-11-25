import React from 'react';
import Dashboard from './components/Dashboard';
export default function App(){
  return (<div className='app'>
    <div className='header' style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:20}}>
      <h1>Real-Time Analytics Dashboard</h1>
      <div>Latency target: <strong>&lt;100ms</strong></div>
    </div>
    <Dashboard />
  </div>);
}
