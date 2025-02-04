import { onCLS, onFID, onFCP, onLCP, onTTFB } from 'web-vitals';

const reportWebVitals = (onPerfEntry) => {
  if (onPerfEntry && onPerfEntry instanceof Function) {
    onCLS(onPerfEntry);  // Callback for CLS metric
    onFID(onPerfEntry);  // Callback for FID metric
    onFCP(onPerfEntry);  // Callback for FCP metric
    onLCP(onPerfEntry);  // Callback for LCP metric
    onTTFB(onPerfEntry); // Callback for TTFB metric
  }
};

export default reportWebVitals;

