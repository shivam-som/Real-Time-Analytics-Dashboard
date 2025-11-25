import React, {useEffect, useState, useRef} from 'react';
import io from 'socket.io-client';
import axios from 'axios';
import MetricChart from './MetricChart';

const SOCKET_URL = process.env.REACT_APP_SOCKET_URL || 'http://localhost:5000';

export default function Dashboard(){
  const [connected, setConnected] = useState(false);
  const [metrics, setMetrics] = useState([]);
  const socketRef = useRef(null);

  useEffect(()=>{
    const socket = io(SOCKET_URL, {transports:['websocket']});
    socketRef.current = socket;
    socket.on('connect', ()=>{ setConnected(true); });
    socket.on('disconnect', ()=>{ setConnected(false); });
    socket.on('metric', (m)=>{
      setMetrics(prev => {
        const next = [m, ...prev].slice(0,500);
        return next;
      });
    });
    return ()=>{ socket.disconnect(); };
  },[]);

  useEffect(()=> {
    axios.get((process.env.REACT_APP_API_BASE || 'http://localhost:5000') + '/api/metrics/recent')
      .then(r => setMetrics(r.data.metrics || []))
      .catch(()=>{});
  },[]);

  const counts = metrics.slice(0,200).reduce((acc, m)=>{
    acc[m.metric] = (acc[m.metric]||0) + 1;
    return acc;
  }, {});

  return (<div style={{display:'grid', gridTemplateColumns:'1fr 360px', gap:16}}>
    <div>
      <div className='card' style={{marginBottom:12}}>
        <h2>Live Stream ({connected ? 'connected' : 'disconnected'})</h2>
        <div style={{display:'flex', gap:8, flexWrap:'wrap'}}>
          {Object.entries(counts).map(([k,v])=> <div key={k} style={{padding:8, borderRadius:6, background:'#f3f4f6', minWidth:100}}>{k}: <strong>{v}</strong></div>)}
        </div>
      </div>
      <div className='card' style={{marginBottom:12}}>
        <h3>Charts</h3>
        <MetricChart metrics={metrics} metricName="orders" />
        <MetricChart metrics={metrics} metricName="page_views" />
      </div>
      <div className='card' style={{marginTop:12}}>
        <h3>Raw events (most recent)</h3>
        <div style={{maxHeight:300, overflow:'auto', fontSize:13}}>
          {metrics.slice(0,200).map((m, i)=> <div key={i} style={{padding:6, borderBottom:'1px solid #eee'}}><code>{m.ts}</code> — <strong>{m.metric}</strong> — {JSON.stringify(m.value)}</div>)}
        </div>
      </div>
    </div>
    <div>
      <div className='card'>
        <h3>Controls</h3>
        <p>Socket: {connected ? '🟢' : '🔴'}</p>
        <p>Recent events: {metrics.length}</p>
        <button onClick={() => { if(socketRef.current) socketRef.current.emit('ping', {ts: new Date().toISOString()})}}>Ping</button>
      </div>
      <div style={{height:12}} />
      <div className='card' style={{marginTop:12}}>
        <h3>Aggregates (last 200)</h3>
        <pre>{JSON.stringify(counts, null, 2)}</pre>
      </div>
    </div>
  </div>);
}
