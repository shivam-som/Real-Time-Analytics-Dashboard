import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, LineElement, PointElement, LinearScale, CategoryScale } from 'chart.js';
ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale);

export default function MetricChart({metrics, metricName}) {
  const points = metrics.filter(m => m.metric === metricName).slice(0,200).reverse();
  const labels = points.map(p => new Date(p.ts).toLocaleTimeString());
  const dataValues = points.map(p => {
    if (metricName === 'orders') return p.value.amount || 0;
    if (metricName === 'latency') return p.value.ms || 0;
    if (metricName === 'page_views') return p.value.count || 0;
    return 1;
  });
  const data = { labels, datasets: [{ label: metricName, data: dataValues, fill:false, tension:0.3 }] };
  const options = { responsive:true, plugins: { legend: { display: false } }, scales: { x: { display: false } } };
  return (<div style={{height:200}}><Line data={data} options={options} /></div>);
}
