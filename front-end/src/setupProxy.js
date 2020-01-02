const proxy = require('http-proxy-middleware');

module.exports = function (app) {
  const API_URL = 'https://90766ec6.ngrok.io';

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