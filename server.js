const http = require('http');
const fs = require('fs');
const path = require('path');

const HOST = '127.0.0.1';
const PORT = 3000;

const server = http.createServer((request, response) => {
    console.log(__dirname);
    var filePath = '.' + request.url;
    if (filePath == './') {
        filePath = path.resolve(__dirname, './client/public/index.html');
    }

    var headers = {'Content-Type': 'text/html'};
    var encoding = 'utf-8';
    fs.readFile(filePath, (error, content) => {
        if (error) {
            console.log(error);
            if (error.code == 'ENOENT') {
                var pathTo404 = path.resolve(__dirname, './client/templates/404.html');
                console.log(pathTo404);
                fs.readFile(pathTo404, (error, content) => {
                    console.log(error);
                    console.log(headers);
                    response.writeHead(404, headers);
                    response.end(content, encoding);
                });
            }
        }
        else {
            response.writeHead(200, headers);
            response.end(content, encoding);
        }
    });

});

server.listen(PORT, HOST, () => {
    console.log('Vanilla HTTP static server Running at http://${HOST}:${PORT}')
});
