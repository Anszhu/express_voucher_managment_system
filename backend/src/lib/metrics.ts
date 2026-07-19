import { performance } from 'node:perf_hooks';

const startedAt = performance.now();
const requests = new Map<string, number>();
const errors = new Map<string, number>();
let durationTotalMs = 0;
let durationCount = 0;

export const recordRequest = (method: string, statusCode: number, durationMs: number) => {
  const key = `${method}:${statusCode}`;
  requests.set(key, (requests.get(key) ?? 0) + 1);
  if (statusCode >= 500) errors.set(method, (errors.get(method) ?? 0) + 1);
  durationTotalMs += durationMs;
  durationCount += 1;
};

export const metricsText = () => {
  const lines = [
    '# HELP voucher_process_uptime_seconds Process uptime in seconds.', '# TYPE voucher_process_uptime_seconds gauge', `voucher_process_uptime_seconds ${process.uptime().toFixed(3)}`,
    '# HELP voucher_process_memory_bytes Process memory usage.', '# TYPE voucher_process_memory_bytes gauge', `voucher_process_memory_bytes ${process.memoryUsage().rss}`,
    '# HELP voucher_http_request_duration_ms_mean Mean HTTP request duration in milliseconds.', '# TYPE voucher_http_request_duration_ms_mean gauge', `voucher_http_request_duration_ms_mean ${durationCount ? (durationTotalMs / durationCount).toFixed(3) : 0}`,
    '# HELP voucher_http_requests_total Total HTTP requests.', '# TYPE voucher_http_requests_total counter'
  ];
  for (const [key, count] of requests) { const [method, status] = key.split(':'); lines.push(`voucher_http_requests_total{method="${method}",status="${status}"} ${count}`); }
  lines.push('# HELP voucher_http_errors_total Total HTTP server errors.', '# TYPE voucher_http_errors_total counter');
  for (const [method, count] of errors) lines.push(`voucher_http_errors_total{method="${method}"} ${count}`);
  return `${lines.join('\n')}\n`;
};

export const runtimeSnapshot = () => ({ uptimeSeconds: Number(process.uptime().toFixed(2)), memory: process.memoryUsage(), cpu: process.cpuUsage(), processStartedMsAgo: Number((performance.now() - startedAt).toFixed(2)) });
