const http = require('http');
const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname);
const srv = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]);
  if (p === '/') p = '/track_builder.html';
  const fp = path.normalize(path.join(root, p));
  fs.readFile(fp, (e, d) => {
    if (e) { res.writeHead(404); return res.end('404'); }
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(d);
  });
});
srv.listen(8765, () => console.log('serving on 8765 at ' + root));
