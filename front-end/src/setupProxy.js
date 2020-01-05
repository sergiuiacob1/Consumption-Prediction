const proxy = require('http-proxy-middleware');

module.exports = function (app) {
  const API_URL = 'http://45543eed.ngrok.io';
  // const API_URL = 'http://localhost:3001';

  app.use('/api', proxy({
    target: API_URL,
    changeOrigin: true,
    onProxyReq(proxyReq) {
      if (proxyReq.getHeader('origin')) {
        proxyReq.setHeader('origin', API_URL)
      }
    },
    pathRewrite: { '^/api': '' },
    logLevel: 'debug',
  }));
};