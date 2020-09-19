src = """
window.pywebview = {
    token: '%s',
    platform: '%s',
    api: {},

    _createApi: function(funcList) {
        for (var i = 0; i < funcList.length; i++) {
            var funcName = funcList[i].func;
            var params = funcList[i].params;

            var funcBody =
                "var __id = (Math.random() + '').substring(2); " +
                "var promise = new Promise(function(resolve, reject) { " +
                    "window.pywebview._checkValue('" + funcName + "', resolve, reject, __id); " +
                "}); " +
                "window.pywebview._bridge.call('" + funcName + "', JSON.stringify(arguments), __id); " +
                "return promise;"

            window.pywebview.api[funcName] = new Function(params, funcBody)
            window.pywebview._returnValues[funcName] = {}
        }
    },

    _bridge: {
        call: function (funcName, params, id) {
            switch(window.pywebview.platform) {
                case 'cef':
                case 'qtwebkit':
                    return window.external.call(funcName, params, id);
                case 'qtwebengine':
                    new QWebChannel(qt.webChannelTransport, function(channel) {
                        channel.objects.external.call(funcName, JSON.stringify(params), id);
                    });
                    break;
                case 'gtk':
                    document.title = JSON.stringify({"type": "invoke", "uid": "%s", "function": funcName, "param": params, "id": id});
                    break;
            }
        }
    },

    _checkValue: function(funcName, resolve, reject, id) {
         var check = setInterval(function () {
            var returnObj = window.pywebview._returnValues[funcName][id];
            if (returnObj) {
                var value = returnObj.value;
                var isError = returnObj.isError;

                delete window.pywebview._returnValues[funcName][id];
                clearInterval(check);

                if (isError) {
                    var pyError = JSON.parse(value);
                    var error = new Error(pyError.message);
                    error.name = pyError.name;
                    error.stack = pyError.stack;

                    reject(error);
                } else {
                    resolve(JSON.parse(value));
                }
            }
         }, 100)
    },

    _returnValues: {}
}
window.pywebview._createApi(%s);
window.dispatchEvent(new CustomEvent('pywebviewready'));
"""
