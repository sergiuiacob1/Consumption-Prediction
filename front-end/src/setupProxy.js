const proxy = require('http-proxy-middleware');

module.exports = function(app) {
  app.use('/api', proxy({
    target: 'https://90766ec6.ngrok.io',
    changeOrigin: true,
    onProxyReq(proxyReq) {
      if (proxyReq.getHeader('origin')) {
        proxyReq.setHeader('origin', 'https://90766ec6.ngrok.io')
      }
    },
    pathRewrite: { '^/api': '' },
    logLevel: 'debug',
  }));
};