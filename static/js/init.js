require.config({
    packages: [
        {
            name: 'crypto-js',
            location: 'static/js/lib/bower_components/crypto-js',
            main: 'index'
        }
    ]
});

var SHA256 = null;

require(["crypto-js/sha256"], function (SHA256_lib) {
    SHA256 = SHA256_lib
});

var server_bridge = new ServerBridge();
var request_handler = new RequestHandler(server_bridge);
