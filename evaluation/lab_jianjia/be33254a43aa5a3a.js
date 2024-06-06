var Demandbase = window.Demandbase || {};
(function (Demandbase) {
    "use strict";

var __extends = this && this.__extends || function() {
  var extendStatics = Object.setPrototypeOf || {
    __proto__: []
  } instanceof Array && function(d, b) {
    d.__proto__ = b;
  } || function(d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
  };
  return function(d, b) {
    extendStatics(d, b);
    function __() {
      this.constructor = d;
    }
    d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
  };
}();

var __awaiter = this && this.__awaiter || function(thisArg, _arguments, P, generator) {
  return new (P || (P = Promise))(function(resolve, reject) {
    function fulfilled(value) {
      try {
        step(generator.next(value));
      } catch (e) {
        reject(e);
      }
    }
    function rejected(value) {
      try {
        step(generator["throw"](value));
      } catch (e) {
        reject(e);
      }
    }
    function step(result) {
      result.done ? resolve(result.value) : new P(function(resolve) {
        resolve(result.value);
      }).then(fulfilled, rejected);
    }
    step((generator = generator.apply(thisArg, _arguments || [])).next());
  });
};

var __generator = this && this.__generator || function(thisArg, body) {
  var _ = {
    label: 0,
    sent: function() {
      if (t[0] & 1) throw t[1];
      return t[1];
    },
    trys: [],
    ops: []
  }, f, y, t, g;
  return g = {
    next: verb(0),
    throw: verb(1),
    return: verb(2)
  }, typeof Symbol === "function" && (g[Symbol.iterator] = function() {
    return this;
  }), g;
  function verb(n) {
    return function(v) {
      return step([ n, v ]);
    };
  }
  function step(op) {
    if (f) throw new TypeError("Generator is already executing.");
    while (_) try {
      if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 
      0) : y.next) && !(t = t.call(y, op[1])).done) return t;
      if (y = 0, t) op = [ op[0] & 2, t.value ];
      switch (op[0]) {
       case 0:
       case 1:
        t = op;
        break;

       case 4:
        _.label++;
        return {
          value: op[1],
          done: false
        };

       case 5:
        _.label++;
        y = op[1];
        op = [ 0 ];
        continue;

       case 7:
        op = _.ops.pop();
        _.trys.pop();
        continue;

       default:
        if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) {
          _ = 0;
          continue;
        }
        if (op[0] === 3 && (!t || op[1] > t[0] && op[1] < t[3])) {
          _.label = op[1];
          break;
        }
        if (op[0] === 6 && _.label < t[1]) {
          _.label = t[1];
          t = op;
          break;
        }
        if (t && _.label < t[2]) {
          _.label = t[2];
          _.ops.push(op);
          break;
        }
        if (t[2]) _.ops.pop();
        _.trys.pop();
        continue;
      }
      op = body.call(thisArg, _);
    } catch (e) {
      op = [ 6, e ];
      y = 0;
    } finally {
      f = t = 0;
    }
    if (op[0] & 5) throw op[1];
    return {
      value: op[0] ? op[1] : void 0,
      done: true
    };
  }
};

function finallyConstructor(callback) {
  var constructor = this.constructor;
  return this.then(function(value) {
    return constructor.resolve(callback()).then(function() {
      return value;
    });
  }, function(reason) {
    return constructor.resolve(callback()).then(function() {
      return constructor.reject(reason);
    });
  });
}

function allSettled(arr) {
  var P = this;
  return new P(function(resolve, reject) {
    if (!(arr && typeof arr.length !== "undefined")) {
      return reject(new TypeError(typeof arr + " " + arr + " is not iterable(cannot read property Symbol(Symbol.iterator))"));
    }
    var args = Array.prototype.slice.call(arr);
    if (args.length === 0) return resolve([]);
    var remaining = args.length;
    function res(i, val) {
      if (val && (typeof val === "object" || typeof val === "function")) {
        var then = val.then;
        if (typeof then === "function") {
          then.call(val, function(val) {
            res(i, val);
          }, function(e) {
            args[i] = {
              status: "rejected",
              reason: e
            };
            if (--remaining === 0) {
              resolve(args);
            }
          });
          return;
        }
      }
      args[i] = {
        status: "fulfilled",
        value: val
      };
      if (--remaining === 0) {
        resolve(args);
      }
    }
    for (var i = 0; i < args.length; i++) {
      res(i, args[i]);
    }
  });
}

var setTimeoutFunc = setTimeout;

function isArray(x) {
  return Boolean(x && typeof x.length !== "undefined");
}

function noop() {}

function bind(fn, thisArg) {
  return function() {
    fn.apply(thisArg, arguments);
  };
}

function Promise(fn) {
  if (!(this instanceof Promise)) throw new TypeError("Promises must be constructed via new");
  if (typeof fn !== "function") throw new TypeError("not a function");
  this._state = 0;
  this._handled = false;
  this._value = undefined;
  this._deferreds = [];
  doResolve(fn, this);
}

function handle(self, deferred) {
  while (self._state === 3) {
    self = self._value;
  }
  if (self._state === 0) {
    self._deferreds.push(deferred);
    return;
  }
  self._handled = true;
  Promise._immediateFn(function() {
    var cb = self._state === 1 ? deferred.onFulfilled : deferred.onRejected;
    if (cb === null) {
      (self._state === 1 ? resolve : reject)(deferred.promise, self._value);
      return;
    }
    var ret;
    try {
      ret = cb(self._value);
    } catch (e) {
      reject(deferred.promise, e);
      return;
    }
    resolve(deferred.promise, ret);
  });
}

function resolve(self, newValue) {
  try {
    if (newValue === self) throw new TypeError("A promise cannot be resolved with itself.");
    if (newValue && (typeof newValue === "object" || typeof newValue === "function")) {
      var then = newValue.then;
      if (newValue instanceof Promise) {
        self._state = 3;
        self._value = newValue;
        finale(self);
        return;
      } else if (typeof then === "function") {
        doResolve(bind(then, newValue), self);
        return;
      }
    }
    self._state = 1;
    self._value = newValue;
    finale(self);
  } catch (e) {
    reject(self, e);
  }
}

function reject(self, newValue) {
  self._state = 2;
  self._value = newValue;
  finale(self);
}

function finale(self) {
  if (self._state === 2 && self._deferreds.length === 0) {
    Promise._immediateFn(function() {
      if (!self._handled) {
        Promise._unhandledRejectionFn(self._value);
      }
    });
  }
  for (var i = 0, len = self._deferreds.length; i < len; i++) {
    handle(self, self._deferreds[i]);
  }
  self._deferreds = null;
}

function Handler(onFulfilled, onRejected, promise) {
  this.onFulfilled = typeof onFulfilled === "function" ? onFulfilled : null;
  this.onRejected = typeof onRejected === "function" ? onRejected : null;
  this.promise = promise;
}

function doResolve(fn, self) {
  var done = false;
  try {
    fn(function(value) {
      if (done) return;
      done = true;
      resolve(self, value);
    }, function(reason) {
      if (done) return;
      done = true;
      reject(self, reason);
    });
  } catch (ex) {
    if (done) return;
    done = true;
    reject(self, ex);
  }
}

Promise.prototype["catch"] = function(onRejected) {
  return this.then(null, onRejected);
};

Promise.prototype.then = function(onFulfilled, onRejected) {
  var prom = new this.constructor(noop);
  handle(this, new Handler(onFulfilled, onRejected, prom));
  return prom;
};

Promise.prototype["finally"] = finallyConstructor;

Promise.all = function(arr) {
  return new Promise(function(resolve, reject) {
    if (!isArray(arr)) {
      return reject(new TypeError("Promise.all accepts an array"));
    }
    var args = Array.prototype.slice.call(arr);
    if (args.length === 0) return resolve([]);
    var remaining = args.length;
    function res(i, val) {
      try {
        if (val && (typeof val === "object" || typeof val === "function")) {
          var then = val.then;
          if (typeof then === "function") {
            then.call(val, function(val) {
              res(i, val);
            }, reject);
            return;
          }
        }
        args[i] = val;
        if (--remaining === 0) {
          resolve(args);
        }
      } catch (ex) {
        reject(ex);
      }
    }
    for (var i = 0; i < args.length; i++) {
      res(i, args[i]);
    }
  });
};

Promise.allSettled = allSettled;

Promise.resolve = function(value) {
  if (value && typeof value === "object" && value.constructor === Promise) {
    return value;
  }
  return new Promise(function(resolve) {
    resolve(value);
  });
};

Promise.reject = function(value) {
  return new Promise(function(resolve, reject) {
    reject(value);
  });
};

Promise.race = function(arr) {
  return new Promise(function(resolve, reject) {
    if (!isArray(arr)) {
      return reject(new TypeError("Promise.race accepts an array"));
    }
    for (var i = 0, len = arr.length; i < len; i++) {
      Promise.resolve(arr[i]).then(resolve, reject);
    }
  });
};

Promise._immediateFn = typeof setImmediate === "function" && function(fn) {
  setImmediate(fn);
} || function(fn) {
  setTimeoutFunc(fn, 0);
};

Promise._unhandledRejectionFn = function _unhandledRejectionFn(err) {
  if (typeof console !== "undefined" && console) {
    console.warn("Possible Unhandled Promise Rejection:", err);
  }
};

var Demandbase;

(function(Demandbase) {
  var Config;
  (function(Config) {
    Config.ads = window.Demandbase.Config.ads || {};
    Config.analytics = window.Demandbase.Config.analytics || {};
    Config.conditions = window.Demandbase.Config.conditions || {};
    Config.content = window.Demandbase.Config.content || {};
    Config.forms = window.Demandbase.Config.forms || {};
    Config.segments = window.Demandbase.Config.segments || {};
    Config.emptyWatchDefault = window.Demandbase.Config.emptyWatchDefault || null;
    Config.hooks = window.Demandbase.Config.hooks || {};
    Config.isInIFrame = window.Demandbase.Config.isInIFrame || null;
    Config.key = window.Demandbase.Config.key || null;
    Config.logging = window.Demandbase.Config.logging || null;
    Config.nonCompanyDefault = window.Demandbase.Config.nonCompanyDefault || null;
    Config.nonWatchDefault = window.Demandbase.Config.nonWatchDefault || null;
    Config.testDomain = window.Demandbase.Config.testDomain || undefined;
    Config.testIp = window.Demandbase.Config.testIp || undefined;
    Config.tokens = window.Demandbase.Config.tokens || {};
    Config.useTestDomain = window.Demandbase.Config.useTestDomain || false;
    Config.useTestIp = window.Demandbase.Config.useTestIp || false;
    Config.Advertising = window.Demandbase.Config.Advertising || {};
    Config.AssetReporter = window.Demandbase.Config.AssetReporter || {};
    Config.Content = window.Demandbase.Config.Content || {};
    Config.ErrorReporter = window.Demandbase.Config.ErrorReporter || {};
    Config.Forms = window.Demandbase.Config.Forms || {};
    Config.Google_Analytics = window.Demandbase.Config.Google_Analytics || {};
    Config.Google_TagManager = window.Demandbase.Config.Google_TagManager || {};
    Config.IpApiModule = Demandbase.Config.IpApiModule || {};
    Config.SiteOptimization = window.Demandbase.Config.SiteOptimization || {};
    Config.EmailDomainReporter = window.Demandbase.Config.EmailDomainReporter || {};
    Config.isVoltronEnabled = window.Demandbase.Config.isVoltronEnabled || true;
    Config.SiteCustomization = window.Demandbase.Config.SiteCustomization || {
      experiences: {}
    };
  })(Config = Demandbase.Config || (Demandbase.Config = {}));
  var Connectors;
  (function(Connectors) {})(Connectors = Demandbase.Connectors || (Demandbase.Connectors = {}));
})(Demandbase || (Demandbase = {}));

var Demandbase;

(function(Demandbase) {
  Demandbase.version = "9.0.7";
})(Demandbase || (Demandbase = {}));

var Demandbase;

(function(Demandbase) {
  var Utilities;
  (function(Utilities) {
    var ErrorStackParser;
    (function(ErrorStackParser) {
      var FIREFOX_SAFARI_STACK_REGEXP = /(^|@)\S+\:\d+/;
      var CHROME_IE_STACK_REGEXP = /^\s*at .*(\S+\:\d+|\(native\))/m;
      var SAFARI_NATIVE_CODE_REGEXP = /^(eval@)?(\[native code\])?$/;
      function parse(error) {
        if (typeof error.stacktrace !== "undefined" || typeof error["opera#sourceloc"] !== "undefined") {
          return this.parseOpera(error);
        }
        if (error.stack && error.stack.match(CHROME_IE_STACK_REGEXP)) {
          return this.parseV8OrIE(error);
        }
        if (error.stack) {
          return this.parseFFOrSafari(error);
        }
        return undefined;
      }
      ErrorStackParser.parse = parse;
      function extractLocation(urlLike) {
        if (Demandbase.Shims.indexOf(urlLike, ":") === -1) {
          return [ urlLike ];
        }
        var regExp = /(.+?)(?:\:(\d+))?(?:\:(\d+))?$/;
        var parts = regExp.exec(urlLike.replace(/[\(\)]/g, ""));
        return [ parts[1], parts[2] || undefined, parts[3] || undefined ];
      }
      ErrorStackParser.extractLocation = extractLocation;
      function _parseInt(string, radix) {
        if (radix === void 0) {
          radix = 10;
        }
        if (!string) {
          return undefined;
        }
        return parseInt(string, radix);
      }
      ErrorStackParser._parseInt = _parseInt;
      function parseV8OrIE(error) {
        var filtered = error.stack.split("\n").filter(function(line) {
          return !!line.match(CHROME_IE_STACK_REGEXP);
        }, this);
        return filtered.map(function(line) {
          if (Demandbase.Shims.indexOf(line, "(eval ") > -1) {
            line = line.replace(/eval code/g, "eval").replace(/(\(eval at [^\()]*)|(\)\,.*$)/g, "");
          }
          var tokens = line.replace(/^\s+/, "").replace(/\(eval code/g, "(").split(/\s+/).slice(1);
          var locationParts = this.extractLocation(tokens.pop());
          var functionName = tokens.join(" ") || undefined;
          var fileName = Demandbase.Shims.indexOf([ "eval", "<anonymous>" ], locationParts[0]) > -1 ? undefined : locationParts[0];
          return {
            function: functionName,
            file: fileName,
            line: this._parseInt(locationParts[1]),
            column: this._parseInt(locationParts[2])
          };
        }, this);
      }
      ErrorStackParser.parseV8OrIE = parseV8OrIE;
      function parseFFOrSafari(error) {
        var filtered = error.stack.split("\n").filter(function(line) {
          return !line.match(SAFARI_NATIVE_CODE_REGEXP);
        }, this);
        return filtered.map(function(line) {
          if (Demandbase.Shims.indexOf(line, " > eval") > -1) {
            line = line.replace(/ line (\d+)(?: > eval line \d+)* > eval\:\d+\:\d+/g, ":$1");
          }
          if (Demandbase.Shims.indexOf(line, "@") === -1 && Demandbase.Shims.indexOf(line, ":") === -1) {
            return {
              function: line
            };
          }
          var tokens = line.split("@");
          var locationParts = this.extractLocation(tokens.pop());
          var functionName = tokens.join("@") || undefined;
          return {
            function: functionName,
            file: locationParts[0],
            line: this._parseInt(locationParts[1]),
            column: this._parseInt(locationParts[2])
          };
        }, this);
      }
      ErrorStackParser.parseFFOrSafari = parseFFOrSafari;
      function parseOpera(e) {
        if (!e.stacktrace || Demandbase.Shims.indexOf(e.message, "\n") > -1 && e.message.split("\n").length > e.stacktrace.split("\n").length) {
          return this.parseOpera9(e);
        }
        if (!e.stack) {
          return this.parseOpera10(e);
        }
        return this.parseOpera11(e);
      }
      ErrorStackParser.parseOpera = parseOpera;
      function parseOpera9(e) {
        var lineRE = /Line (\d+).*script (?:in )?(\S+)/i;
        var lines = e.message.split("\n");
        var result = [];
        for (var i = 2, len = lines.length; i < len; i += 2) {
          var match = lineRE.exec(lines[i]);
          if (match) {
            result.push({
              file: match[2],
              line: this._parseInt(match[1])
            });
          }
        }
        return result;
      }
      ErrorStackParser.parseOpera9 = parseOpera9;
      function parseOpera10(e) {
        var lineRE = /Line (\d+).*script (?:in )?(\S+)(?:: In function (\S+))?$/i;
        var lines = e.stacktrace.split("\n");
        var result = [];
        for (var i = 0, len = lines.length; i < len; i += 2) {
          var match = lineRE.exec(lines[i]);
          if (match) {
            result.push({
              function: match[3] || undefined,
              file: match[2],
              line: this._parseInt(match[1])
            });
          }
        }
        return result;
      }
      ErrorStackParser.parseOpera10 = parseOpera10;
      function parseOpera11(error) {
        var filtered = error.stack.split("\n").filter(function(line) {
          return !!line.match(FIREFOX_SAFARI_STACK_REGEXP) && !line.match(/^Error created at/);
        }, this);
        return filtered.map(function(line) {
          var tokens = line.split("@");
          var locationParts = this.extractLocation(tokens.pop());
          var functionCall = tokens.shift() || "";
          var functionName = functionCall.replace(/<anonymous function(: (\w+))?>/, "$2").replace(/\([^\)]*\)/g, "") || undefined;
          var argsRaw;
          if (functionCall.match(/\(([^\)]*)\)/)) {
            argsRaw = functionCall.replace(/^[^\(]+\(([^\)]*)\)$/, "$1");
          }
          var args = argsRaw === undefined || argsRaw === "[arguments not available]" ? undefined : argsRaw.split(",");
          return {
            function: functionName,
            file: locationParts[0],
            line: this._parseInt(locationParts[1]),
            column: this._parseInt(locationParts[2])
          };
        }, this);
      }
      ErrorStackParser.parseOpera11 = parseOpera11;
    })(ErrorStackParser = Utilities.ErrorStackParser || (Utilities.ErrorStackParser = {}));
  })(Utilities = Demandbase.Utilities || (Demandbase.Utilities = {}));
})(Demandbase || (Demandbase = {}));

var Demandbase;

(function(Demandbase) {
  var Shims;
  (function(Shims) {
    Shims.console = window.console || {
      log: function() {},
      debug: function() {}
    };
    Shims.JSON = window.JSON || {
      stringify: function() {},
      parse: function() {}
    };
    function indexOf(array, searchElement, fromIndex) {
      if (array === null || array === undefined) {
        throw new TypeError("Array.indexOf called on null or undefined");
      }
      if (array.indexOf) {
        return array.indexOf(searchElement, fromIndex);
      }
      return _indexOfPolyfill(array, searchElement, fromIndex);
    }
    Shims.indexOf = indexOf;
    function assign() {
      var args = [];
      for (var _i = 0; _i < arguments.length; _i++) {
        args[_i] = arguments[_i];
      }
      if (Object.assign && typeof Object.assign === "function") {
        return Object.assign.apply(null, args);
      }
      if (args[0] === null || args[0] === undefined) {
        throw new TypeError("Cannot convert undefined or null to object");
      }
      return _assignPolyfill(args);
    }
    Shims.assign = assign;
    function includes(search, start) {
      if (search instanceof RegExp) {
        throw new TypeError("First argument must not be a RegExp");
      }
      if (start === undefined) {
        start = 0;
      }
      return this.indexOf(search, start) !== -1;
    }
    Shims.includes = includes;
    function keys(obj) {
      if (Object.keys) {
        return Object.keys(obj);
      }
      if (typeof obj !== "function" && (typeof obj !== "object" || obj === null)) {
        throw new TypeError("Object.keys called on non-object");
      }
      return _keysPolyfill(obj);
    }
    Shims.keys = keys;
    function _indexOfPolyfill(array, searchElement, fromIndex) {
      var len = array.length >>> 0;
      var i = Math.min(fromIndex | 0, len);
      if (i < 0) {
        i = Math.max(0, len + i);
      } else if (i >= len) {
        return -1;
      }
      if (searchElement === void 0) {
        for (;i !== len; ++i) {
          if (array[i] === void 0 && i in array) {
            return i;
          }
        }
      } else if (searchElement !== searchElement) {
        for (;i !== len; ++i) {
          if (array[i] !== array[i]) {
            return i;
          }
        }
      } else {
        for (;i !== len; ++i) {
          if (array[i] === searchElement) {
            return i;
          }
        }
      }
      return -1;
    }
    Shims._indexOfPolyfill = _indexOfPolyfill;
    function _assignPolyfill(args) {
      var to = Object(args[0]);
      for (var index = 1; index < args.length; index++) {
        var nextSource = args[index];
        if (nextSource != null) {
          for (var nextKey in nextSource) {
            if (Object.prototype.hasOwnProperty.call(nextSource, nextKey)) {
              to[nextKey] = nextSource[nextKey];
            }
          }
        }
      }
      return to;
    }
    Shims._assignPolyfill = _assignPolyfill;
    function _keysPolyfill(obj) {
      var hasOwnProperty = Object.prototype.hasOwnProperty;
      var hasDontEnumBug = !{
        toString: null
      }.propertyIsEnumerable("toString");
      var dontEnums = [ "toString", "toLocaleString", "valueOf", "hasOwnProperty", "isPrototypeOf", "propertyIsEnumerable", "constructor" ];
      var dontEnumsLength = dontEnums.length;
      var result = [];
      var prop;
      var i;
      for (prop in obj) {
        if (hasOwnProperty.call(obj, prop)) {
          result.push(prop);
        }
      }
      if (hasDontEnumBug) {
        for (i = 0; i < dontEnumsLength; i++) {
          if (hasOwnProperty.call(obj, dontEnums[i])) {
            result.push(dontEnums[i]);
          }
        }
      }
      return result;
    }
    Shims._keysPolyfill = _keysPolyfill;
  })(Shims = Demandbase.Shims || (Demandbase.Shims = {}));
})(Demandbase || (Demandbase = {}));

var Demandbase;

(function(Demandbase) {
  var Utilities;
  (function(Utilities) {
    var Api;
    (function(Api) {
      function buildApiParamString(params) {
        var allParams = {
          referrer: document.referrer,
          page: document.URL,
          page_title: document.title
        };
        if (Demandbase.Config.isInIFrame) {
          try {
            allParams.page = window.top.document.URL;
            allParams.referrer = window.top.document.referrer;
            allParams.page_title = window.top.document.title;
          } catch (error) {
            allParams.page = document.referrer;
            allParams.referrer = null;
            allParams.page_title = "3rd Party iFrame";
          }
        }
        allParams = Demandbase.Shims.assign(allParams, params);
        return buildQueryString(allParams);
      }
      Api.buildApiParamString = buildApiParamString;
      function buildApiUrl(base, params) {
        var url = base || Utilities.Constants.URL_IP_API;
        url += buildApiParamString(params);
        return url;
      }
      Api.buildApiUrl = buildApiUrl;
      function buildQueryString(params) {
        var qs = "?";
        for (var name_1 in params) {
          if (params.hasOwnProperty(name_1) && params[name_1] !== undefined) {
            qs += name_1 + "=" + encodeURIComponent(params[name_1]) + "&";
          }
        }
        qs = qs.substring(0, qs.length - 1);
        return qs;
      }
      Api.buildQueryString = buildQueryString;
    })(Api = Utilities.Api || (Utilities.Api = {}));
  })(Utilities = Demandbase.Utilities || (Demandbase.Utilities = {}));
})(Demandbase || (Demandbase = {}));

(function(window) {
  window.Demandbase.utils = window.Demandbase.utils || {};
  Demandbase.Shims.assign(window.Demandbase.utils, window.Demandbase.utils, {
    buildApiParamString: Demandbase.Utilities.Api.buildApiParamString,
    buildApiUrl: Demandbase.Utilities.Api.buildApiUrl,
    buildQueryString: Demandbase.Utilities.Api.buildQueryString
  });
})(window);

var Demandbase;

(function(Demandbase) {
  var Utilities;
  (function(Utilities) {
    var Callbacks;
    (function(Callbacks) {
      Callbacks.callbackStack = [];
      function callback(data) {
        var _loop_1 = function(i) {
          var callback_1 = Callbacks.callbackStack[i];
          Demandbase.ErrorReporter.wrap(function() {
            callback_1.call(Demandbase, data);
          })();
        };
        for (var i = 0; i < Callbacks.callbackStack.length; i++) {
          _loop_1(i);
        }
      }
      Callbacks.callback = callback;
      function domScriptCallback(data) {
        Demandbase.IpApi.CompanyProfile = Demandbase.Utilities.flatten(data);
        this.callback(data);
      }
      Callbacks.domScriptCallback = domScriptCallback;
      function registerCallback(callback) {
        if (Demandbase.Shims.indexOf(Callbacks.callbackStack, callback) !== -1) {
          return;
        }
        Callbacks.callbackStack.push(callback);
        if (Demandbase.IpApi && Demandbase.IpApi.CompanyProfile) {
          Demandbase.ErrorReporter.wrap(function() {
            callback.call(Demandbase, Demandbase.IpApi.CompanyProfile);
          })();
        }
      }
      Callbacks.registerCallback = registerCallback;
    })(Callbacks = Utilities.Callbacks || (Utilities.Callbacks = {}));
  })(Utilities = Demandbase.Utilities || (Demandbase.Utilities = {}));
})(Demandbase || (Demandbase = {}));

(function(window) {
  window.Demandbase.utils = window.Demandbase.utils || {};
  Demandbase.Shims.assign(window.Demandbase.utils, window.Demandbase.utils, {
    callback: Demandbase.Utilities.Callbacks.callback.bind(Demandbase.Utilities.Callbacks),
    registerCallback: Demandbase.Utilities.Callbacks.registerCallback.bind(Demandbase.Utilities.Callbacks)
  });
})(window);

var Demandbase;

(function(Demandbase) {
  var Utilities;
  (function(Utilities) {
    var Constants;
    (function(Constants) {
      Constants.QS_USE_TEST_DOMAIN = "db_useTestDomain";
      Constants.QS_QUERY_DOMAIN = "db_domain";
      Constants.QS_ENABLE_LOG = "db_logging";
      Constants.QS_PREVIEW_TOKEN = "db_preview_token";
      Constants.DFLT_NON_COMPANY = "(Non-Company Visitor)";
      Constants.DFLT_AW_EMPTY = "(AccountWatch Empty)";
      Constants.DFLT_NON_AW = "(Non-AccountWatch Visitor)";
      Constants.DFLT_EVENT_TYPE = "click";
      Constants.URL_IP_API = "api.company-target.com/api/v2/ip.json";
      Constants.URL_DOMAIN_API = "api.demandbase.com/api/v1/domain.json";
      Constants.URL_BW_AD_PIXEL = Demandbase.Config.tokens.URL_BW_AD_PIXEL || "match.prod.bidr.io/cookie-sync/demandbase";
      Constants.URL_LR_AD_PIXEL = Demandbase.Config.tokens.URL_LR_AD_PIXEL || "id.rlcdn.com/464526.gif";
      Constants.MODIFICATION_ERROR = "SCModificationError";
      Constants.PARDOT_VISITOR_COOKIE_REGEX = /^visitor_id[\d]+$/;
      Constants.NON_HUMAN_DEVICES = [ /adsbot-google/i, /googlebot/i ];
      Constants.URL_CURRENT = function() {
        var pg = document.URL;
        if (Demandbase.Config.isInIFrame) {
          pg = document.referrer;
        }
        pg = encodeURIComponent(pg);
        return pg;
      }();
      Constants.PROTOCOL = "https://";
    })(Constants = Utilities.Constants || (Utilities.Constants = {}));
  })(Utilities = Demandbase.Utilities || (Demandbase.Utilities = {}));
})(Demandbase || (Demandbase = {}));

(function(window) {
  window.Demandbase.utils = window.Demandbase.utils || {};
  Demandbase.Shims.assign(window.Demandbase.utils, window.Demandbase.utils, {
    tokens: Demandbase.Utilities.Constants
  });
})(window);

var Demandbase;

(function(Demandbase) {
  var DBContent = function() {
    function DBContent(values) {
      if (values === void 0) {
        values = {};
      }
      this.name = values.name || "";
      this.modify = values.modify || null;
      this.segments = values.segments || [];
      this.url = values.url || [];
      if (!this.modify) {
        this.modify = function() {
          Demandbase.Utilities.Logging.log("DBContent: modify function not defined");
        };
      }
      if (typeof this.segments === "string") this.segments = [ this.segments ];
      if (typeof this.url === "string") this.url = [ this.url ];
    }
    DBContent.prototype.run = function() {
      var urlMatch = false;
      for (var index in this.url) {
        if (this.url.hasOwnProperty(index)) {
          var url = this.url[index];
          if (Demandbase.Utilities.isCurrentPage(url)) {
            urlMatch = true;
          }
        }
      }
      if (urlMatch) {
        var segMatch = false;
        for (var index in this.segments) {
          if (this.segments.hasOwnProperty(index)) {
            var segmentName = this.segments[index];
            var segment = window.Demandbase.Segments[segmentName];
            if (typeof segment !== "undefined" && segment) {
              segMatch = true;
            }
          }
        }
        if (!segMatch) {
          Demandbase.Utilities.Logging.log("DBContent modify " + this.name + " not fired.  Segment " + segmentName);
          return false;
        }
        try {
          Demandbase.Utilities.Logging.log("DBContent: running modify function for: " + this.name);
          this.modify.call(document);
        } catch (error) {
          error.name = Demandbase.Utilities.Constants.MODIFICATION_ERROR;
          throw error;
        }
        return true;
      }
      Demandbase.Utilities.Logging.log("DBContent modify " + this.name + " not fired. no URL match with: " + this.url);
      return false;
    };
    return DBContent;
  }();
  Demandbase.DBContent = DBContent;
})(Demandbase || (Demandbase = {}));

var Demandbase;

(function(Demandbase) {
  var DBContentBuilder;
  (function(DBContentBuilder) {
    function isValid(config) {
      if (!config) return false;
      var reqdPropsList = [ "name", "segments", "pages", "modify" ];
      if (typeof config.modify !== "function") {
        //!config['pages'] instanceof Array ||
        //!config['segments'] instanceof Array
        Demandbase.Utilities.Logging.log("DBContentBuilder: invalid type in config.");
        return false;
      }
      for (var i = 0; i < reqdPropsList.length; i++) {
        if (typeof config[reqdPropsList[i]] === "undefined") {
          Demandbase.Utilities.Logging.log("DBContentBuilder: invalid config missing: " + reqdPropsList[i]);
          return false;
        }
      }
      return true;
    }
    DBContentBuilder.isValid = isValid;
    function build(config) {
      if (isValid(config)) {
        if (typeof config.pages === "string") {
          config.url = [ config.pages ];
        } else {
          config.url = config.pages;
        }
        if (typeof config.segments === "string") {
          config.segments = [ config.segments ];
        }
        return new Demandbase.DBContent(config);
      }
      return null;
    }
    DBContentBuilder.build = build;
  })(DBContentBuilder = Demandbase.DBContentBuilder || (Demandbase.DBContentBuilder = {}));
})(Demandbase || (Demandbase = {}));

var Demandbase;

(function(Demandbase) {
  var Utilities;
  (function(Utilities) {
    var Events;
    (function(Events) {
      function add(eventObj) {
        var result = true;
        if (!isValid(eventObj)) {
          Demandbase.Utilities.Logging.log("Event not added.");
          return false;
        }
        var eventType = eventObj.type || Demandbase.Utilities.Constants.DFLT_EVENT_TYPE;
        var elements = eventObj.elements;
        var elmConstructor = elements.constructor;
        if (elmConstructor === HTMLCollection || elmConstructor === NodeList) {
          for (var eaElm in elements) {
            var added = false;
            if (elements.hasOwnProperty(eaElm)) {
              added = _attachListener(elements[eaElm], eventType, eventObj.listener);
              if (!added) {
                result = false;
                Demandbase.Utilities.Logging.log("Event not added to" + elements[eaElm]);
              }
            }
          }
        } else {
          return _attachListener(eventObj.elements, eventType, eventObj.listener);
        }
        return result;
      }
      Events.add = add;
      function _attachListener(element, eventName, listener) {
        if (!element) {
          Demandbase.Utilities.Logging.log("Event not registered - invalid element/s.");
          return null;
        }
        if (element.jquery) {
          element = element[0];
        }
        Demandbase.Utilities.addEventListener(element, eventName, listener);
        Demandbase.Utilities.Logging.log("Event Listener bind to: " + element + " on event " + eventName);
        return true;
      }
      Events._attachListener = _attachListener;
      function isValid(eventObj) {
        var result = false;
        var reqdPropsList = [ "elements", "listener" ];
        var elms = eventObj.elements || null;
        var listener = eventObj.listener || null;
        for (var i = 0; i < reqdPropsList.length; i++) {
          if (typeof eventObj[reqdPropsList[i]] === "undefined" || !eventObj[reqdPropsList[i]]) {
            Demandbase.Utilities.Logging.log("Invalid Event object. Missing: " + reqdPropsList[i]);
            return false;
          }
        }
        if (typeof listener !== "function") {
          Demandbase.Utilities.Logging.log('Invalid Event: "listener" must be a function. Got (' + listener + ")");
          return false;
        }
        if (elms instanceof Node || elms instanceof NodeList || elms instanceof HTMLElement || elms instanceof HTMLCollection || elms instanceof Window || elms instanceof Document || typeof elms === "function" || typeof window.Demandbase.jQuery !== "undefined" && elms instanceof window.Demandbase.jQuery) {
          result = true;
        } else {
          Demandbase.Utilities.Logging.log("Invalid Event:  element: " + elms + ' has type: "' + elms.constructor + '" which is not proper instance type.');
        }
        return result;
      }
      Events.isValid = isValid;
    })(Events = Utilities.Events || (Utilities.Events = {}));
  })(Utilities = Demandbase.Utilities || (Demandbase.Utilities = {}));
})(Demandbase || (Demandbase = {}));

(function(window) {
  window.Demandbase.utils = window.Demandbase.utils || {};
  Demandbase.Shims.assign(window.Demandbase.utils, window.Demandbase.utils, {
    events: Demandbase.Utilities.Events
  });
})(window);

var Demandbase;

(function(Demandbase) {
  var Utilities;
  (function(Utilities) {
    var Logging;
    (function(Logging) {
      Logging.logging = false;
      Logging.debug = false;
      function alert(message) {
        log(message);
      }
      Logging.alert = alert;
      function log(message) {
        if (Demandbase.Config.logging || Demandbase.Utilities.getQueryParam(Demandbase.Utilities.Constants.QS_ENABLE_LOG) === "true") {
          Demandbase.Shims.console.log("DB: " + message);
        }
      }
      Logging.log = log;
    })(Logging = Utilities.Logging || (Utilities.Logging = {}));
  })(Utilities = Demandbase.Utilities || (Demandbase.Utilities = {}));
})(Demandbase || (Demandbase = {}));

(function(window) {
  window.Demandbase.utils = window.Demandbase.utils || {};
  Demandbase.Shims.assign(window.Demandbase.utils, window.Demandbase.utils, {
    logging: Demandbase.Utilities.Logging.logging,
    debug: Demandbase.Utilities.Logging.debug,
    alert: Demandbase.Utilities.Logging.alert.bind(Demandbase.Utilities.Logging),
    log: Demandbase.Utilities.Logging.log.bind(Demandbase.Utilities.Logging)
  });
})(window);

var Demandbase;

(function(Demandbase) {
  var Utilities;
  (function(Utilities) {
    function getCookiesByRegex(regex, _document) {
      var extractedCookies = {};
      _document.cookie.split(";").forEach(function(cookieString) {
        var cookie = cookieString.split("=");
        var cookieKey = cookie[0].trim();
        if (regex.test(cookieKey) && cookie.length > 1) {
          extractedCookies[cookieKey] = cookie[1].trim();
        }
      });
      return extractedCookies;
    }
    Utilities.getCookiesByRegex = getCookiesByRegex;
    function getElementByIdOrName(elementIdentifier) {
      return document.getElementById(elementIdentifier) || document.getElementsByName(elementIdentifier)[0] || null;
    }
    Utilities.getElementByIdOrName = getElementByIdOrName;
    function addEventListener(target, type, listener) {
      if (target.addEventListener) {
        target.addEventListener(type, listener);
      } else if (target.attachEvent) {
        target.attachEvent(type, listener);
      }
    }
    Utilities.addEventListener = addEventListener;
    function dig(target) {
      var keys = [];
      for (var _i = 1; _i < arguments.length; _i++) {
        keys[_i - 1] = arguments[_i];
      }
      var digged = target;
      for (var _a = 0, keys_1 = keys; _a < keys_1.length; _a++) {
        var key = keys_1[_a];
        if (typeof digged === "undefined") {
          return undefined;
        }
        if (typeof key === "function") {
          digged = key(digged);
        } else {
          digged = digged[key];
        }
      }
      return digged;
    }
    Utilities.dig = dig;
    function flatten(object) {
      for (var key in object) {
        var value = object[key];
        if (typeof value !== "object" || value === null || !object.hasOwnProperty(key)) {
          continue;
        }
        for (var nestedKey in value) {
          object[key + "_" + nestedKey] = value[nestedKey];
        }
        delete object[key];
      }
      return object;
    }
    Utilities.flatten = flatten;
    function getAttributeValue(data, attrName) {
      if (data[attrName] === false) {
        return "false";
      }
      var registryMap = {
        city: "registry_city",
        state: "registry_state",
        zip: "registry_zip_code",
        country: "registry_country_code",
        country_name: "registry_country",
        latitude: "registry_latitude",
        longitude: "registry_longitude"
      };
      var dflt = Demandbase.Config.nonCompanyDefault || Demandbase.Utilities.Constants.DFLT_NON_COMPANY;
      var awDflt = Demandbase.Config.emptyWatchDefault || Demandbase.Utilities.Constants.DFLT_AW_EMPTY;
      var regName = registryMap[attrName] || "";
      var attrValue = data[attrName] || data[regName] || dflt;
      var isCompany = (data.company_name || dflt) !== dflt;
      var dataKeys = Demandbase.Shims.keys(data);
      var isAcctWatch = false;
      for (var i = 0; i < dataKeys.length; i++) {
        if (Demandbase.Shims.indexOf(dataKeys[i], "watch_list_") === 0) {
          isAcctWatch = true;
          break;
        }
      }
      if (Demandbase.Shims.indexOf(attrName, "watch_list_") !== -1 && isCompany) {
        if (!isAcctWatch) {
          awDflt = Demandbase.Config.nonWatchDefault || Demandbase.Utilities.Constants.DFLT_NON_AW;
        }
        attrValue = data[attrName] || awDflt;
      }
      return attrValue;
    }
    Utilities.getAttributeValue = getAttributeValue;
    function getQueryParam(param, _window) {
      var _window = _window || window || {
        location: {
          search: "",
          hash: ""
        }
      };
      var params = {};
      var qs = _window.location.search.substring(1) || _window.location.hash && _window.location.hash.split("?")[1];
      if (!qs) return "";
      var pairs = qs.split("&");
      for (var i = 0; i < pairs.length; i++) {
        var nvArray = pairs[i].split("=");
        var name_1 = nvArray[0];
        var value = nvArray[1];
        params[name_1] = value;
      }
      return params[param] || "";
    }
    Utilities.getQueryParam = getQueryParam;
    function insertScript(url, id, srcPrefix) {
      if (srcPrefix === void 0) {
        srcPrefix = "https://";
      }
      if (!url) {
        return;
      }
      Demandbase._loadedScripts = Demandbase._loadedScripts || {};
      if (Demandbase._loadedScripts[url]) {
        return;
      }
      Demandbase._loadedScripts[url] = true;
      var element = document.createElement("script");
      var firstScript = document.getElementsByTagName("script")[0];
      element.async = true;
      element.id = id || "";
      element.src = "" + srcPrefix + url.replace(/(^\/\/)|(^http:\/\/)|(^https:\/\/)/, "");
      firstScript.parentNode.insertBefore(element, firstScript);
    }
    Utilities.insertScript = insertScript;
    function isOldBrowserOrUserAgentUnavailable() {
      try {
        return Demandbase.Shims.indexOf(window.navigator.userAgent, "MSIE ") > 0;
      } catch (error) {
        return true;
      }
    }
    Utilities.isOldBrowserOrUserAgentUnavailable = isOldBrowserOrUserAgentUnavailable;
    function b64EncodeUnicode(str) {
      return btoa(encodeURIComponent(str).replace(/%([0-9A-F]{2})/g, function toSolidBytes(match, p1) {
        return String.fromCharCode(parseInt("0x" + p1, 16));
      }));
    }
    Utilities.b64EncodeUnicode = b64EncodeUnicode;
    function generateDeprecationMessage(name, version) {
      return name + " has been deprecated since version " + version;
    }
    Utilities.generateDeprecationMessage = generateDeprecationMessage;
  })(Utilities = Demandbase.Utilities || (Demandbase.Utilities = {}));
})(Demandbase || (Demandbase = {}));

(function(window) {
  window.Demandbase.utils = window.Demandbase.utils || {};
  Demandbase.Shims.assign(window.Demandbase.utils, window.Demandbase.utils, Demandbase.Utilities);
  Demandbase.Shims.assign(window.Demandbase.utils, Demandbase.utils, {
    loadScript: Demandbase.Utilities.insertScript,
    flattenData: Demandbase.Utilities.flatten,
    getAttrValue: Demandbase.Utilities.getAttributeValue
  });
})(window);

var Demandbase;

(function(Demandbase) {
  var Utilities;
  (function(Utilities) {
    function detectIFrame() {
      return window.top !== window.self;
    }
    Utilities.detectIFrame = detectIFrame;
    function getDocumentReadyState() {
      return document.readyState;
    }
    Utilities.getDocumentReadyState = getDocumentReadyState;
    function isCookieEnabled() {
      try {
        if (window.navigator.cookieEnabled) {
          document.cookie = "COOKIE_TEST=TEST";
          if (Demandbase.Shims.indexOf(document.cookie, "COOKIE_TEST=TEST") !== -1) {
            document.cookie = "COOKIE_TEST=PASSED_TEST";
            return true;
          }
        }
        return false;
      } catch (error) {
        return false;
      }
    }
    Utilities.isCookieEnabled = isCookieEnabled;
    function getCurrentUrl(currUrl) {
      var currentUrl = document.location.href;
      if (Demandbase.Config.isInIFrame) {
        currentUrl = document.referrer;
      }
      if (currUrl) {
        currentUrl = currUrl;
      }
      return currentUrl;
    }
    function isCurrentPage(testUrl, currUrl) {
      var qm = "?";
      var pound = "#";
      var hash = document.location.hash;
      var search = document.location.search;
      var currentUrl = getCurrentUrl(currUrl);
      if (currUrl) {
        var searchEnd = Demandbase.Shims.indexOf(currUrl, pound);
        if (searchEnd === -1) {
          searchEnd = currUrl.length;
        }
        hash = currUrl.substring(Demandbase.Shims.indexOf(currUrl, pound), currUrl.length);
        search = currUrl.substring(Demandbase.Shims.indexOf(currUrl, qm), searchEnd);
        currentUrl = currUrl;
      }
      function stripProtocol(str) {
        var doubleSlash = "//";
        if (Demandbase.Shims.indexOf(str, doubleSlash) === 0) {
          return str.substring(doubleSlash.length, str.length);
        }
        return str.replace(/^.*?:\/\//g, "");
      }
      function stripWww(str) {
        return str.replace(/^(www\.)/g, "");
      }
      function stripTail(str) {
        var slash = "/";
        if (Demandbase.Shims.indexOf(str, pound, str.length - pound.length) !== -1) {
          str = str.substring(0, str.length - 1);
        }
        if (Demandbase.Shims.indexOf(str, slash, str.length - slash.length) !== -1) {
          str = str.substring(0, str.length - 1);
        }
        return str;
      }
      testUrl = stripProtocol(testUrl);
      testUrl = stripWww(testUrl);
      testUrl = stripTail(testUrl);
      currentUrl = stripProtocol(currentUrl);
      currentUrl = stripWww(currentUrl);
      currentUrl = stripTail(currentUrl);
      if (Demandbase.Shims.indexOf(testUrl, pound) === -1 && Demandbase.Shims.indexOf(currentUrl, pound) !== -1) {
        currentUrl = currentUrl.substring(0, currentUrl.length - hash.length);
      }
      if (Demandbase.Shims.indexOf(testUrl, qm) === -1 && Demandbase.Shims.indexOf(currentUrl, qm) !== -1) {
        currentUrl = currentUrl.substring(0, currentUrl.length - search.length);
      }
      currentUrl = stripTail(currentUrl);
      var result = currentUrl === testUrl;
      Demandbase.Utilities.Logging.log("utilities.isCurrentPage(): Page check resulted in: " + result);
      return result;
    }
    Utilities.isCurrentPage = isCurrentPage;
    function isCurrentPageRegex(testRegex, currUrl) {
      if (!testRegex) return false;
      if (testRegex.length <= 0) return false;
      if (testRegex[0] !== "^") {
        testRegex = "^" + testRegex;
      }
      var end = testRegex.length - 1;
      if (testRegex[end] !== "$") {
        testRegex += "$";
      }
      var currentUrl = getCurrentUrl(currUrl);
      return new RegExp(testRegex).test(currentUrl);
    }
    Utilities.isCurrentPageRegex = isCurrentPageRegex;
    function isStorageEnabled(type) {
      try {
        var storage = window[type.toString()];
        storage.setItem("STORAGE_CHECK", "STORAGE_CHECK");
        var test = storage.getItem("STORAGE_CHECK");
        storage.removeItem("STORAGE_CHECK");
        return true;
      } catch (error) {
        return false;
      }
    }
    Utilities.isStorageEnabled = isStorageEnabled;
    function jqid(id) {
      return !id ? null : "#" + id.replace(/(:|\.|\[|\]|,)/g, "\\$1");
    }
    Utilities.jqid = jqid;
    function includesAny(haystack, needles) {
      for (var i = 0; i < needles.length; i++) {
        if (includes(haystack, needles[i])) return true;
      }
      return false;
    }
    Utilities.includesAny = includesAny;
    function isValidEmail(str) {
      var regexp = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return regexp.test(str);
    }
    Utilities.isValidEmail = isValidEmail;
    function escapeRegExp(str) {
      return str.replace(/[.*+?^${}()|[\]\\\/]/g, "\\$&");
    }
    Utilities.escapeRegExp = escapeRegExp;
    function nodeListToArray(nodeList) {
      var output = [];
      for (var i = 0; i < nodeList.length; i++) output.push(nodeList[i]);
      return output;
    }
    Utilities.nodeListToArray = nodeListToArray;
    function includes(str, search) {
      if (!search) {
        return false;
      }
      if (search.length > str.length) {
        return false;
      }
      return Demandbase.Shims.indexOf(str, search) !== -1;
    }
  })(Utilities = Demandbase.Utilities || (Demandbase.Utilities = {}));
})(Demandbase || (Demandbase = {}));

var Demandbase;

(function(Demandbase) {
  var ModuleFactory = function() {
    function ModuleFactory(config, moduleNameToConstructorMap, nameSpace) {
      this.config = config;
      this.moduleNameToConstructorMap = moduleNameToConstructorMap;
      this.nameSpace = nameSpace;
    }
    ModuleFactory.prototype.build = function() {
      this._parseConfig();
    };
    ModuleFactory.prototype._parseConfig = function() {
      var _this = this;
      Demandbase.Shims.keys(this.config).forEach(function(configKey) {
        var configGroups = _this._testConfigForKey(configKey);
        if (configGroups && configGroups.length === 3) {
          var moduleName = configGroups[1];
          var moduleConstructor = _this.moduleNameToConstructorMap[moduleName];
          if (_this.nameSpace[configKey]) {
            Demandbase.ErrorReporter.send(new Error("Failed to dynamically create configuration for " + configKey + " due to previously existing configuration with the same name."));
            return;
          }
          if (!moduleConstructor) {
            Demandbase.ErrorReporter.send(new Error("No constructor available in moduleNameToConstructor map for module: " + moduleName));
            return;
          }
          _this.nameSpace[configKey] = new moduleConstructor(_this.config[configKey]);
          if (_this.nameSpace[configKey].isEnabled()) {
            _this.nameSpace[configKey].initialize();
          }
        }
      });
    };
    ModuleFactory.prototype._testConfigForKey = function(configKey) {
      return ModuleFactory.REGEX_CUSTOM_MODULE_NAME.exec(configKey);
    };
    ModuleFactory.REGEX_CUSTOM_MODULE_NAME = /(.*)__(.*)/;
    return ModuleFactory;
  }();
  Demandbase.ModuleFactory = ModuleFactory;
})(Demandbase || (Demandbase = {}));

var Demandbase;

(function(Demandbase) {
  var BaseModule = function() {
    function BaseModule() {
      this.configuration = {};
    }
    BaseModule.prototype.isEnabled = function() {
      return this.configuration.enabled;
    };
    BaseModule.prototype.mergeConfigs = function() {
      var configs = [];
      for (var _i = 0; _i < arguments.length; _i++) {
        configs[_i] = arguments[_i];
      }
      var _a;
      (_a = Demandbase.Shims).assign.apply(_a, [ this.configuration ].concat(configs));
    };
    return BaseModule;
  }();
  Demandbase.BaseModule = BaseModule;
})(Demandbase || (Demandbase = {}));

var Demandbase;

(function(Demandbase) {
  var AdvertisingModule = function(_super) {
    __extends(AdvertisingModule, _super);
    function AdvertisingModule(config) {
      var _this = _super.call(this) || this;
      _this.ADVERTISING_PIXEL_ID = "ad";
      _this.CONVERSION_PIXEL_ID = "cn";
      _this.RETARGETING_PIXEL_ID = "rt";
      _this.DEFAULT_CONFIGURATION = {
        enabled: true,
        key: null,
        reportingOnly: false,
        enableBW: true,
        enableLR: true
      };
      _this.configuration = {};
      _this.trackConversion = _this.trackConversionListener;
      _this.load = _this.initialize;
      _this.loadPixels = _this.insertPixels;
      _this._loadPixel = _this.insertPixel;
      _this._setCampaign = _this.loadCampaign;
      _this._setEvents = _this.registerEvents;
      _super.prototype.mergeConfigs.call(_this, _this.DEFAULT_CONFIGURATION, config || Demandbase.Config.Advertising);
      _super.prototype.mergeConfigs.call(_this, config || Demandbase.Config.ads);
      return _this;
    }
    AdvertisingModule.prototype.initialize = function() {
      this.insertPixels();
      if (this.configuration.reportingOnly === true && this.configuration.key && this.configuration.key !== Demandbase.Config.key) {
        Demandbase.IpApiReportingOnly.get(this.configuration.key, false);
      }
    };
    AdvertisingModule.prototype.isConversionPage = function() {
      throw new Error(Demandbase.Utilities.generateDeprecationMessage("AdvertisingModule.isConversionPage", "8.0.0"));
    };
    AdvertisingModule.prototype.insertPixels = function() {
      if (this.configuration.enableBW) {
        Demandbase.Utilities.Logging.log("BW pixel enabled");
        this.insertBWPixel(this.ADVERTISING_PIXEL_ID);
      }
      if (this.configuration.enableLR) {
        Demandbase.Utilities.Logging.log("LR pixel enabled");
        this.insertLRPixel(this.ADVERTISING_PIXEL_ID);
      }
    };
    AdvertisingModule.prototype.createAndAppendPixel = function(id, src) {
      var element = document.getElementsByTagName("body")[0] || document.getElementsByTagName("head")[0];
      var pixelElm = document.createElement("img");
      pixelElm.setAttribute("style", "display:none");
      pixelElm.setAttribute("alt", "");
      pixelElm.setAttribute("aria-hidden", "true");
      pixelElm.setAttribute("width", "0");
      pixelElm.setAttribute("height", "0");
      pixelElm.id = id;
      pixelElm.src = src;
      element.appendChild(pixelElm);
    };
    AdvertisingModule.prototype.insertBWPixel = function(name) {
      var id = "db_bw_pixel_" + name;
      var src = Demandbase.Utilities.Constants.PROTOCOL + Demandbase.Utilities.Constants.URL_BW_AD_PIXEL;
      this.createAndAppendPixel(id, src);
    };
    AdvertisingModule.prototype.insertLRPixel = function(name) {
      var id = "db_lr_pixel_" + name;
      var src = Demandbase.Utilities.Constants.PROTOCOL + Demandbase.Utilities.Constants.URL_LR_AD_PIXEL;
      this.createAndAppendPixel(id, src);
    };
    AdvertisingModule.prototype.insertPixel = function(name) {
      throw new Error(Demandbase.Utilities.generateDeprecationMessage("AdvertisingModule.insertPixel", "8.0.0"));
    };
    AdvertisingModule.prototype.loadCampaign = function() {
      throw new Error(Demandbase.Utilities.generateDeprecationMessage("AdvertisingModule.loadCampaign", "8.0.0"));
    };
    AdvertisingModule.prototype.registerEvents = function() {
      throw new Error(Demandbase.Utilities.generateDeprecationMessage("AdvertisingModule.registerEvents", "8.0.0"));
    };
    AdvertisingModule.prototype.trackConversionListener = function() {
      throw new Error(Demandbase.Utilities.generateDeprecationMessage("AdvertisingModule.trackConversionListener", "8.0.0"));
    };
    AdvertisingModule.prototype.virtualPageViewListener = function() {
      throw new Error(Demandbase.Utilities.generateDeprecationMessage("AdvertisingModule.virtualPageViewListener", "8.0.0"));
    };
    return AdvertisingModule;
  }(Demandbase.BaseModule);
  Demandbase.AdvertisingModule = AdvertisingModule;
})(Demandbase || (Demandbase = {}));

var Demandbase;

(function(Demandbase) {
  var AssetReporterModule = function(_super) {
    __extends(AssetReporterModule, _super);
    function AssetReporterModule(config) {
      var _this = _super.call(this) || this;
      _this.DEFAULT_CONFIGURATION = {
        enabled: true,
        assetList: [ "api.demandbase.com/autocomplete/widget.js", "api.demandbase.com/autocomplete/widget.min.js", "autocomplete.demandbase.com/autocomplete/widget.js", "autocomplete.demandbase.com/autocomplete/widget.min.js", "scripts.demandbase.com/formWidget.js", "scripts.demandbase.com/formWidgetDebug.js", "scripts.demandbase.com/demandbase-sdk.js", "scripts.demandbase.com/demandbase-sdk-debug.js", "scripts.demandbase.com/forms.js", "scripts.demandbase.com/forms.min.js" ]
      };
      _this.ERROR_MESSAGE_PREFIX = "Legacy Asset Detected: ";
      _this.configuration = {};
      _this.values = {};
      _super.prototype.mergeConfigs.call(_this, _this.DEFAULT_CONFIGURATION, config || Demandbase.Config.AssetReporter);
      return _this;
    }
    AssetReporterModule.prototype.initialize = function() {
      if (Demandbase.Utilities.getDocumentReadyState() === "complete") {
        this.read();
      } else {
        Demandbase.Utilities.addEventListener(window, "load", Demandbase.ErrorReporter.wrap(this.read.bind(this)));
      }
    };
    AssetReporterModule.prototype.read = function() {
      var assetQty = this.configuration.assetList.length;
      for (var i = 0; i < assetQty; i++) {
        var assetUrl = this.configuration.assetList[i];
        var asset = document.querySelector("script[src='" + Demandbase.Utilities.Constants.PROTOCOL + assetUrl + "']");
        if (asset) {
          this.values[assetUrl] = true;
          this.send(assetUrl);
        } else {
          this.values[assetUrl] = false;
        }
      }
    };
    AssetReporterModule.prototype.send = function(message) {
      var error = new Error(this.ERROR_MESSAGE_PREFIX + message);
      Demandbase.ErrorReporter.send(error);
    };
    return AssetReporterModule;
  }(Demandbase.BaseModule);
  Demandbase.AssetReporterModule = AssetReporterModule;
})(Demandbase || (Demandbase = {}));

var Demandbase;

(function(Demandbase) {
  var ContentModule = function(_super) {
    __extends(ContentModule, _super);
    function ContentModule(config) {
      var _this = _super.call(this) || this;
      _this.DEFAULT_CONFIGURATION = {
        enabled: true
      };
      _this.configuration = {};
      _this.mods = {};
      _super.prototype.mergeConfigs.call(_this, _this.DEFAULT_CONFIGURATION, config || Demandbase.Config.Content);
      Demandbase.Shims.assign(_this.configuration, config || Demandbase.Config.content);
      return _this;
    }
    ContentModule.prototype.initialize = function() {
      Demandbase.Utilities.Callbacks.registerCallback(this.callback.bind(this));
      this.setup();
    };
    ContentModule.prototype.callback = function() {
      this.setup();
      this.modify();
    };
    ContentModule.prototype.setup = function() {
      if (typeof Demandbase.Config.content !== "undefined") {
        for (var index in Demandbase.Config.content) {
          var modObj = Demandbase.Config.content[index];
          var dbContent = window.Demandbase.DBContentBuilder.build(modObj);
          if (dbContent) {
            this.mods[dbContent.name] = dbContent;
          }
        }
      }
    };
    ContentModule.prototype.modify = function() {
      var _this = this;
      return Demandbase.ErrorReporter.wrap(function() {
        var isMod = false;
        for (var eachMod in _this.mods) {
          if (_this.mods.hasOwnProperty(eachMod)) {
            var modObj = _this.mods[eachMod];
            var isRunMod = modObj.run();
            if (isRunMod) isMod = true;
          }
        }
      })();
    };
    return ContentModule;
  }(Demandbase.BaseModule);
  Demandbase.ContentModule = ContentModule;
})(Demandbase || (Demandbase = {}));

var Demandbase;

(function(Demandbase) {
  var EmailDomainReporterModule = function(_super) {
    __extends(EmailDomainReporterModule, _super);
    function EmailDomainReporterModule(config) {
      var _this = _super.call(this) || this;
      _this.DEFAULT_CONFIGURATION = {
        enabled: true,
        fireOnLoad: false,
        formInputSelectors: [ 'input[type="text"]', 'input[type="email"]' ],
        inputSearchTerms: [ "email", "user", "login" ]
      };
      _this.configuration = {};
      _this.baseUrl = "https://segments.company-target.com";
      _this.activeSetTimeout = 0;
      _super.prototype.mergeConfigs.call(_this, _this.DEFAULT_CONFIGURATION, config || Demandbase.Config.EmailDomainReporter);
      return _this;
    }
    EmailDomainReporterModule.prototype.initialize = function() {
      if (this.configuration.fireOnLoad) {
        this.sendDataIfAlreadyPresent();
      }
      this.attachListenersIfDocumentReady();
    };
    EmailDomainReporterModule.prototype.sendDataIfAlreadyPresent = function() {
      var _this = this;
      var emailInputs = this.suspectedEmailInputs();
      if (emailInputs.length < 1) return;
      emailInputs.forEach(function(input) {
        var value = input.value;
        if (!Demandbase.Utilities.isValidEmail(value)) return;
        var domain = value.split("@")[1].toLowerCase();
        _this.send(domain);
      });
    };
    EmailDomainReporterModule.prototype.attachListenersIfDocumentReady = function() {
      var _this = this;
      if (Demandbase.Utilities.getDocumentReadyState() === "loading") {
        document.addEventListener("DOMContentLoaded", this.attachListenersIfDocumentReady.bind(this));
        return;
      }
      this.suspectedEmailInputs().forEach(function(input) {
        input.addEventListener("input", function() {
          var value = input.value;
          if (!Demandbase.Utilities.isValidEmail(value)) return;
          var domain = value.split("@")[1].toLowerCase();
          window.clearTimeout(_this.activeSetTimeout);
          _this.activeSetTimeout = window.setTimeout(function() {
            _this.send(domain);
          }, 400);
        });
      });
    };
    EmailDomainReporterModule.prototype.suspectedEmailInputs = function() {
      var _this = this;
      var allInputsOnPage = Demandbase.Utilities.nodeListToArray(document.querySelectorAll(this.configuration.formInputSelectors.join(","))).map(function(element) {
        return element;
      });
      var suspectedEmailInputs = allInputsOnPage.filter(function(inputElement) {
        var name = inputElement.name.toLowerCase();
        var id = inputElement.id.toLowerCase();
        var searchTerms = _this.configuration.inputSearchTerms;
        if (Demandbase.Utilities.includesAny(name, searchTerms)) return true;
        if (Demandbase.Utilities.includesAny(id, searchTerms)) return true;
        return false;
      });
      return suspectedEmailInputs;
    };
    EmailDomainReporterModule.prototype.send = function(domain) {
      var xhttp;
      if (window.XMLHttpRequest) {
        xhttp = new XMLHttpRequest();
      } else if (window.ActiveXObject) {
        xhttp = new ActiveXObject("Microsoft.XMLHTTP");
      }
      var token = Demandbase.Config.key || Demandbase.Utilities.dig(Demandbase.Config, "analytics", "key") || Demandbase.Utilities.dig(Demandbase.Config, "ads", "key") || Demandbase.Utilities.dig(Demandbase.Config, "forms", "key") || "";
      var qsB64 = Demandbase.Utilities.b64EncodeUnicode("vendor=mariposa&p1=" + domain + "&token=" + token);
      var url = this.baseUrl + "/l/" + qsB64;
      try {
        xhttp.open("GET", url);
        xhttp.withCredentials = true;
        xhttp.setRequestHeader("Content-type", "application/json");
        xhttp.send();
      } catch (requestError) {
        throw requestError;
      }
    };
    EmailDomainReporterModule.prototype.responseHandler = function(request) {};
    return EmailDomainReporterModule;
  }(Demandbase.BaseModule);
  Demandbase.EmailDomainReporterModule = EmailDomainReporterModule;
})(Demandbase || (Demandbase = {}));

var Demandbase;

(function(Demandbase) {
  var ErrorReporterModule = function(_super) {
    __extends(ErrorReporterModule, _super);
    function ErrorReporterModule(config) {
      var _this = _super.call(this) || this;
      _this.VERSION = "0.0.0";
      _this.PROJECT_ID = "141580";
      _this.PROJECT_KEY = "9a0a3519e930259f5886a7af53b0ccaa";
      _this.SENTRY_PROJECT_ID = "1190150";
      _this.SENTRY_PUBLIC_KEY = "3c9d467f8a9d4295b0f8320ae852091d";
      _this.DEFAULT_CONFIGURATION = {
        environment: "production",
        ignorableErrors: []
      };
      _this.configuration = {};
      _this.additionalErrorDetails = {};
      _super.prototype.mergeConfigs.call(_this, _this.DEFAULT_CONFIGURATION, config || Demandbase.Config.ErrorReporter);
      return _this;
    }
    ErrorReporterModule.prototype.initialize = function() {};
    ErrorReporterModule.prototype.send = function(error) {
      if (Demandbase.Shims.indexOf(this.configuration.ignorableErrors, error.name) > -1 || Demandbase.Shims.indexOf(this.configuration.ignorableErrors, error.message) > -1) {
        return;
      }
      var sentryXhttp;
      if (window.XMLHttpRequest) {
        sentryXhttp = new XMLHttpRequest();
      } else if (window.ActiveXObject) {
        sentryXhttp = new ActiveXObject("Microsoft.XMLHTTP");
      }
      var sentryUrl = "https://sentry.io/api/" + this.SENTRY_PROJECT_ID + "/store/?sentry_version=7&sentry_key=" + this.SENTRY_PUBLIC_KEY;
      try {
        sentryXhttp.open("POST", sentryUrl, true);
        sentryXhttp.setRequestHeader("Content-type", "text/plain;charset=UTF-8");
        sentryXhttp.send(this.formatMessage(error, true));
      } catch (requestError) {}
    };
    ErrorReporterModule.prototype.wrap = function(method) {
      var _this = this;
      if (typeof method !== "function") {
        throw new Error("Invalid Function: " + method);
      }
      return function() {
        var parameters = [];
        for (var _i = 0; _i < arguments.length; _i++) {
          parameters[_i] = arguments[_i];
        }
        try {
          if (typeof method !== "undefined" && typeof method.apply === "function") {
            return method.apply(_this, parameters);
          }
        } catch (error) {
          _this.send(error);
          Demandbase.Utilities.Logging.alert("Error: " + error + "\n" + error.stack);
        }
      };
    };
    ErrorReporterModule.prototype.formatMessage = function(error, forSentry) {
      if (forSentry === void 0) {
        forSentry = false;
      }
      var errorDetails = this.parseError(error);
      var context = this.parseContext();
      var environment = this.parseEnviroment();
      var session = this.parseSession();
      var params = this.parseParams();
      var additionalErrorDetails = this.additionalErrorDetails;
      if (forSentry) {
        var sentryFormattedError = this.formatErrorForSentry(errorDetails);
        return Demandbase.Shims.JSON.stringify({
          logger: context.notifier.name,
          platform: "javascript",
          release: context.version,
          environment: context.environment,
          request: {
            url: context.url
          },
          contexts: {
            browser: {
              userAgent: context.userAgent
            }
          },
          tags: {
            clientId: environment.config.clientId
          },
          extra: {
            readyState: context.readyState,
            config: environment.config,
            companyProfile: session,
            additionalErrorDetails: additionalErrorDetails
          },
          exception: {
            values: [ sentryFormattedError ]
          }
        });
      }
      return Demandbase.Shims.JSON.stringify({
        errors: [ errorDetails ],
        context: context,
        environment: environment,
        session: session,
        params: params
      });
    };
    ErrorReporterModule.prototype.formatErrorForSentry = function(errorDetails) {
      var stacktrace = [];
      for (var _i = 0, _a = errorDetails.backtrace; _i < _a.length; _i++) {
        var frame = _a[_i];
        stacktrace.push({
          function: frame.function,
          filename: frame.file,
          lineno: frame.line,
          colno: frame.column
        });
      }
      return {
        type: errorDetails.type,
        value: errorDetails.message,
        stacktrace: {
          frames: stacktrace
        }
      };
    };
    ErrorReporterModule.prototype.parseError = function(error) {
      return {
        type: error.name,
        message: error.message,
        backtrace: Demandbase.Utilities.ErrorStackParser.parse(error)
      };
    };
    ErrorReporterModule.prototype.parseContext = function() {
      return {
        notifier: {
          name: "ErrorReporterModule",
          version: this.VERSION
        },
        environment: this.configuration.environment,
        version: Demandbase.version,
        url: window.location.href,
        userAgent: navigator.userAgent,
        rootDirectory: window.location.origin,
        readyState: document.readyState
      };
    };
    ErrorReporterModule.prototype.parseEnviroment = function() {
      return {
        config: Demandbase.Utilities.dig(Demandbase, "Config")
      };
    };
    ErrorReporterModule.prototype.parseSession = function() {
      return {
        companyProfile: Demandbase.Utilities.dig(Demandbase, "IP", "CompanyProfile")
      };
    };
    ErrorReporterModule.prototype.parseParams = function() {
      return {};
    };
    return ErrorReporterModule;
  }(Demandbase.BaseModule);
  Demandbase.ErrorReporterModule = ErrorReporterModule;
})(Demandbase || (Demandbase = {}));

var Demandbase;

(function(Demandbase) {
  var FormsLoaderModule = function(_super) {
    __extends(FormsLoaderModule, _super);
    function FormsLoaderModule(config) {
      var _this = _super.call(this) || this;
      _this.FORMS_REMOTE_MODULE_URL = "tag.demandbase.com/shared/forms_2343aad66e.min.js";
      _this.DEFAULT_CONFIGURATION = {
        enabled: undefined,
        emailID: null,
        emailFields: []
      };
      _this.configuration = {};
      _this.inserted = false;
      _this.setConfiguration(config);
      return _this;
    }
    FormsLoaderModule.prototype.initialize = function() {
      Demandbase.Utilities.Callbacks.registerCallback(this.whenReady.bind(this));
    };
    FormsLoaderModule.prototype.whenReady = function() {
      if (this.isMktoForms2Installed()) {
        window.MktoForms2.whenReady(Demandbase.ErrorReporter.wrap(this.load.bind(this)));
      } else {
        this.load();
      }
    };
    FormsLoaderModule.prototype.load = function() {
      var isFormPage = false;
      if (typeof Demandbase.Config.isFormPage === "function") {
        isFormPage = Demandbase.Config.isFormPage();
        this.setConfiguration();
        isFormPage = Demandbase.Config.isFormPage();
      } else {
        isFormPage = this.isFormPage();
      }
      if (!isFormPage || this.inserted) {
        return;
      }
      this.insertForms();
    };
    FormsLoaderModule.prototype.isFormPage = function() {
      var emailFieldList = this.configuration.emailFields;
      if (this.configuration.emailID) {
        emailFieldList.push(this.configuration.emailID);
      }
      for (var i = 0; i < emailFieldList.length; i++) {
        if (Demandbase.Utilities.getElementByIdOrName(emailFieldList[i])) {
          return true;
        }
      }
      return false;
    };
    FormsLoaderModule.prototype.isMktoForms2Installed = function() {
      return window.MktoForms2 !== undefined && window.MktoForms2.whenReady !== undefined;
    };
    FormsLoaderModule.prototype.insertForms = function() {
      this.inserted = true;
      Demandbase.Connectors.initWebForm = this.initializeWebForm;
      Demandbase.Utilities.insertScript(Demandbase.FormsLoader.FORMS_REMOTE_MODULE_URL, "db_form_module");
    };
    FormsLoaderModule.prototype.initializeWebForm = function(config) {
      config = config || Demandbase.Config.forms || Demandbase.Config.Forms || {};
      window.Demandbase.Connectors.WebForm.connect(config);
    };
    FormsLoaderModule.prototype.setConfiguration = function(config) {
      _super.prototype.mergeConfigs.call(this, this.DEFAULT_CONFIGURATION, config || Demandbase.Config.Forms);
      if (this.configuration.enabled === undefined && Demandbase.Config.Forms !== undefined) {
        this.configuration.enabled = true;
      }
      _super.prototype.mergeConfigs.call(this, this.DEFAULT_CONFIGURATION, config || Demandbase.Config.forms);
      if (this.configuration.enabled === undefined && Demandbase.Config.forms !== undefined) {
        this.configuration.enabled = true;
      }
    };
    return FormsLoaderModule;
  }(Demandbase.BaseModule);
  Demandbase.FormsLoaderModule = FormsLoaderModule;
})(Demandbase || (Demandbase = {}));

var Demandbase;

(function(Demandbase) {
  var SiteOptimizationLoaderModule = function(_super) {
    __extends(SiteOptimizationLoaderModule, _super);
    function SiteOptimizationLoaderModule(config) {
      var _this = _super.call(this) || this;
      _this.SO_REMOTE_MODULE_URL = "https://tag.demandbase.com/shared/siteOptimization_2343aad66e.min.js";
      _this.REMOTE_STYLESHEET_URL = "https://tag.demandbase.com/shared/siteOptimization_2343aad66e.css";
      _this.DEFAULT_CONFIGURATION = {
        additionalClass: null,
        backgroundColorClass: null,
        closedTitle: "Recommended Content",
        companyProfile: null,
        cssFileURL: _this.REMOTE_STYLESHEET_URL,
        delay: 0,
        enabled: undefined,
        fadeIn: 0,
        fontColor: null,
        fontName: null,
        googleAnalyticsTrackerName: null,
        isGoogleAnalyticsEnabled: false,
        isRippleAnimation: true,
        isSwitchersDots: true,
        isSwitchersArrows: false,
        itemBackgroundColor: null,
        mainClass: "defaultBlock",
        openByDefault: false,
        openTitle: null,
        recommendationApiURL: "https://site-optimization-api.company-target.com/recommend/",
        recommendationCompanyName: null,
        recommendationCompanyId: null,
        recommendationKey: null,
        recommendationsProtocol: "forceHTTPS",
        recommendationUrl: window.location.href,
        showCloseButton: true,
        showCompanyName: true,
        showFeedbackLink: false,
        showIndicatorArrows: true,
        showLogo: true,
        showLogoWhenClosed: true,
        showLogoWhenOpen: false,
        showOnlyOnScroll: false,
        showTitleWhenClosed: true,
        showTitleWhenOpen: true,
        switcherArrowsColor: "#444",
        state: {
          openedRecommendationBlock: null
        },
        widgetBackgroundColor: null,
        widgetContainerId: null
      };
      _this.configuration = {};
      _this.inserted = false;
      _super.prototype.mergeConfigs.call(_this, _this.DEFAULT_CONFIGURATION, config || Demandbase.Config.SiteOptimization);
      _this.configuration.recommendationKey = Demandbase.Config.key;
      return _this;
    }
    SiteOptimizationLoaderModule.prototype.initialize = function() {
      Demandbase.Utilities.Callbacks.registerCallback(this.callback.bind(this));
    };
    SiteOptimizationLoaderModule.prototype.callback = function(data) {
      this.configuration.companyProfile = data;
      this.insertSiteOptimization();
    };
    SiteOptimizationLoaderModule.prototype.insertSiteOptimization = function() {
      this.inserted = true;
      Demandbase.Utilities.insertScript(Demandbase.SiteOptimizationLoader.SO_REMOTE_MODULE_URL, "db_site_optimization_module");
    };
    return SiteOptimizationLoaderModule;
  }(Demandbase.BaseModule);
  Demandbase.SiteOptimizationLoaderModule = SiteOptimizationLoaderModule;
})(Demandbase || (Demandbase = {}));

var Demandbase;

(function(Demandbase) {
  var BaseGoogle_AnalyticsModule = function(_super) {
    __extends(BaseGoogle_AnalyticsModule, _super);
    function BaseGoogle_AnalyticsModule(config) {
      var _this = _super.call(this) || this;
      _this.DEFAULT_CONFIGURATION = {
        enabled: true,
        events: null,
        fieldMap: null,
        googleAnalyticsClassicScope: 2,
        trackerName: null,
        trackerId: null
      };
      _this.configuration = {};
      _this.gType = "";
      _this._cEvent = _this.sendEvent;
      _super.prototype.mergeConfigs.call(_this, _this.DEFAULT_CONFIGURATION, config || Demandbase.Config.Google_Analytics);
      _super.prototype.mergeConfigs.call(_this, config || Demandbase.Config.analytics);
      return _this;
    }
    BaseGoogle_AnalyticsModule.prototype.initialize = function() {
      this._detectG();
      this._setTrackerName();
      if (this.configuration.fieldMap && Demandbase.Shims.JSON.stringify(this.configuration.fieldMap) !== "{}") {
        Demandbase.Utilities.Callbacks.registerCallback(this.callback.bind(this));
      }
      this._setEvents();
    };
    BaseGoogle_AnalyticsModule.prototype.sendEvent = function(category, action, label) {
      if (this.gType === "ga") {
        this._trackEvent(category, action, label);
      } else {
        window.ga(function() {
          Demandbase.Connectors.Google_Analytics._sendEvent(category, action, label);
        });
      }
      Demandbase.Utilities.Logging.log("Sent Custom Event:" + category + "/" + action + "/" + label);
    };
    BaseGoogle_AnalyticsModule.prototype._setTrackerName = function() {
      var _this = this;
      if (this.configuration.trackerName) return;
      var foundUaMethod = typeof window.ga !== "undefined";
      var foundClassicMethod = typeof window._gat !== "undefined" && typeof window._gat._getTrackers === "function";
      if (foundClassicMethod) {
        var trackers = _gat._getTrackers();
        if (typeof trackers.length !== "undefined" && trackers.length > 0) {
          if (this.configuration.trackerId) {
            for (var i = 0; i < trackers.length; i++) {
              if (trackers[i]._getName().length > 0) {
                var name_1 = trackers[i]._getName();
                if (trackers[i]._getAccount() === this.configuration.trackerId) {
                  if (!this.configuration.trackerName) {
                    this.configuration.trackerName = name_1;
                    return;
                  }
                }
              }
            }
          }
          var tracker = trackers[0] || null;
          if (tracker && typeof tracker._getName === "function") {
            var name_2 = tracker._getName() || null;
            if (!this.configuration.trackerName) {
              this.configuration.trackerName = name_2;
            }
          }
        }
      }
      if (foundUaMethod) {
        window.ga(function() {
          var trackers = window.ga.getAll() || [];
          if (_this.configuration.trackerId) {
            for (var i = 0; i < trackers.length; i++) {
              var tracker = trackers[i];
              var name_3 = tracker.get("name");
              if (tracker.get("trackingId") === _this.configuration.trackerId) {
                _this.configuration.trackerName = name_3;
                return;
              }
            }
          }
          if (typeof trackers.length !== "undefined" && trackers.length > 0) {
            var tracker = trackers[0] || null;
            if (tracker && typeof tracker.get === "function") {
              var name_4 = tracker.get("name") || null;
              _this.configuration.trackerName = name_4;
            }
          }
        });
      }
    };
    BaseGoogle_AnalyticsModule.prototype.callback = function(data) {
      try {
        if (!data) {
          throw new Error("Error - no data passed to callback");
        }
        var self_1 = Demandbase.Connectors.Google_Analytics;
        self_1._detectG();
        self_1._setTrackerName();
        for (var field in self_1.configuration.fieldMap) {
          if (self_1.configuration.fieldMap.hasOwnProperty(field)) {
            var num = +field;
            var lbl = self_1.configuration.fieldMap[field];
            var val = Demandbase.Utilities.getAttributeValue(data, lbl);
            self_1._var(num, lbl, val.toString());
          }
        }
        self_1.sendEvent("Demandbase", "API Resolution", "IP API");
      } catch (e) {
        Demandbase.Utilities.Logging.log("GA Error: " + e + "\n" + e.stack);
        Demandbase.Connectors.Google_Analytics.sendEvent("Demandbase", "API Resolution", "Callback Error");
      }
    };
    BaseGoogle_AnalyticsModule.prototype._detectG = function() {
      if (window._gaq) {
        this.gType = "ga";
        _gaq.push([ "_addDevId", "NE7T9" ]);
      } else {
        this.gType = null;
      }
      this._setGaObject();
      try {
        window.ga(function() {
          Demandbase.Connectors.Google_Analytics.gType = "ua";
        });
      } catch (error) {
        Demandbase.Connectors.Google_Analytics.gType = "ua";
      }
      Demandbase.Utilities.Logging.log("Detected Google version: " + this.gType);
    };
    BaseGoogle_AnalyticsModule.prototype._sendEvent = function(category, action, label) {
      var command = this.configuration.trackerName ? this.configuration.trackerName + ".send" : "send";
      window.ga(command, "event", {
        eventCategory: category,
        eventAction: action,
        eventLabel: label,
        nonInteraction: true
      });
    };
    BaseGoogle_AnalyticsModule.prototype._setCustomDimension = function(index, value) {
      var command = this.configuration.trackerName ? this.configuration.trackerName + ".set" : "set";
      window.ga(command, "dimension" + index, value);
    };
    BaseGoogle_AnalyticsModule.prototype._setCustomVariable = function(index, name, value) {
      var command = this.configuration.trackerName ? this.configuration.trackerName + "._setCustomVar" : "_setCustomVar";
      var scope = this.configuration.googleAnalyticsClassicScope || 2;
      window._gaq.push([ command, index >> 0, name, value, scope ]);
    };
    BaseGoogle_AnalyticsModule.prototype._setEvents = function() {
      var eventList = this.configuration.events || [];
      if (eventList) {
        for (var i in eventList) {
          if (eventList.hasOwnProperty(i)) {
            var eventObj = eventList[i];
            if (eventObj.data) {
              var cat = eventObj.data.category || "";
              var act = eventObj.data.action || "";
              var lbl = eventObj.data.label || "";
              if (typeof eventObj.listener === "undefined" && cat && act && lbl) {
                eventObj.listener = function() {
                  Demandbase.Connectors.Google_Analytics.sendEvent(cat, act, lbl);
                  Demandbase.Utilities.Logging.log("Event listener ran");
                };
              } else if (!cat || !act || !lbl) {
                Demandbase.Utilities.Logging.log("Need to define a custom listener function or set data with category/action/label");
              }
            }
            Demandbase.Utilities.Events.add(eventObj);
          }
        }
      }
    };
    BaseGoogle_AnalyticsModule.prototype._setGaObject = function() {
      if (typeof window.ga === "undefined") {
        window.ga = window.ga || function() {
          (window.ga.q = window.ga.q || []).push(arguments);
        };
        window.ga.l = +new Date();
      }
    };
    BaseGoogle_AnalyticsModule.prototype._trackEvent = function(category, action, label) {
      var command = this.configuration.trackerName ? this.configuration.trackerName + "._trackEvent" : "_trackEvent";
      window._gaq.push([ command, category, action, label, 0, 1 ]);
    };
    BaseGoogle_AnalyticsModule.prototype._var = function(index, name, value) {
      if (this.gType === "ga") {
        this._setCustomVariable(index, name, value);
      } else {
        window.ga(function() {
          Demandbase.Connectors.Google_Analytics._setCustomDimension(index, value);
        });
      }
      Demandbase.Utilities.Logging.log(index + " " + name + " : " + value);
    };
    return BaseGoogle_AnalyticsModule;
  }(Demandbase.BaseModule);
  Demandbase.BaseGoogle_AnalyticsModule = BaseGoogle_AnalyticsModule;
})(Demandbase || (Demandbase = {}));

var Demandbase;

(function(Demandbase) {
  var Google_AnalyticsModule = function(_super) {
    __extends(Google_AnalyticsModule, _super);
    function Google_AnalyticsModule() {
      return _super !== null && _super.apply(this, arguments) || this;
    }
    Google_AnalyticsModule.prototype.getTrackerInfo = function() {
      var classicInfo = [];
      var universalInfo = [];
      if (typeof window._gaq !== "undefined" && typeof window._gat !== "undefined" && typeof window._gat._getTrackers === "function") {
        var classicTrackers = window._gat._getTrackers();
        classicTrackers.forEach(function(classicTracker) {
          if (classicTracker._getName().length > 0) {
            classicInfo.push({
              type: "classic",
              trackerId: classicTracker._getAccount(),
              name: classicTracker._getName()
            });
          }
        });
      }
      if (typeof window.ga !== "undefined" && typeof window.ga.getAll !== "undefined") {
        var universalTrackers = window.ga.getAll();
        universalTrackers.forEach(function(universalTracker) {
          universalInfo.push({
            type: "universal",
            trackerId: universalTracker.get("trackingId"),
            name: universalTracker.get("name")
          });
        });
      }
      return universalInfo.concat(classicInfo);
    };
    return Google_AnalyticsModule;
  }(Demandbase.BaseGoogle_AnalyticsModule);
  Demandbase.Google_AnalyticsModule = Google_AnalyticsModule;
})(Demandbase || (Demandbase = {}));

var Demandbase;

(function(Demandbase) {
  var Google_TagManagerModule = function(_super) {
    __extends(Google_TagManagerModule, _super);
    function Google_TagManagerModule(config) {
      var _this = _super.call(this) || this;
      _this.DEFAULT_CONFIGURATION = {
        enabled: true
      };
      _this.configuration = {};
      _super.prototype.mergeConfigs.call(_this, _this.DEFAULT_CONFIGURATION, config || Demandbase.Config.Google_TagManager);
      return _this;
    }
    Google_TagManagerModule.prototype.initialize = function() {
      Demandbase.Utilities.Callbacks.registerCallback(this.callback.bind(this));
    };
    Google_TagManagerModule.prototype.callback = function(data) {
      Demandbase.Connectors.Google_TagManager.pushToDataLayer(data);
    };
    Google_TagManagerModule.prototype.pushToDataLayer = function(data, id) {
      if (!window.google_tag_manager || !window.dataLayer || typeof dataLayer.push !== "function") {
        return false;
      }
      var eventLabel = id ? "_" + id : "";
      dataLayer.push(data);
      dataLayer.push({
        event: "Demandbase_Loaded" + eventLabel
      });
      Demandbase.Utilities.Logging.log("Pushed to GTM dataLayer");
      return true;
    };
    return Google_TagManagerModule;
  }(Demandbase.BaseModule);
  Demandbase.Google_TagManagerModule = Google_TagManagerModule;
})(Demandbase || (Demandbase = {}));

var Demandbase;

(function(Demandbase) {
  var IpApiModule = function(_super) {
    __extends(IpApiModule, _super);
    function IpApiModule(config) {
      var _this = _super.call(this) || this;
      _this.TEST_MODE_ENABLED = "db_useTestIp";
      _this.TEST_MODE_VALUE = "db_ip";
      _this.API_ENDPOINT = "api.company-target.com/api/v2/ip.json";
      _this.DEFAULT_CONFIGURATION = {
        apiKey: null,
        baseUrl: _this.API_ENDPOINT,
        testModeEnabled: false,
        testModeValue: null,
        masIntegrations: {
          pardot: false
        },
        enablePardotPolling: true
      };
      _this.configuration = {};
      _this.initialized = false;
      _this.pollForPardotStart = 0;
      _this.pardotMaxPollWindow = 5e3;
      _this.key = _this.configuration.apiKey;
      _this.useTestValue = _this.configuration.testModeEnabled;
      _this.testValue = _this.configuration.testModeValue;
      _this.load = _this.get;
      _this._loadOnce = _this.getOnce;
      _this.CompanyProfile = undefined;
      _this.isCalled = false;
      _this.experiences = {};
      try {
        _super.prototype.mergeConfigs.call(_this, _this.DEFAULT_CONFIGURATION, {
          apiKey: Demandbase.Config.key || Demandbase.Utilities.dig(Demandbase.Config, "analytics", "key") || Demandbase.Utilities.dig(Demandbase.Config, "ads", "key") || Demandbase.Utilities.dig(Demandbase.Config, "forms", "key"),
          testModeEnabled: Demandbase.Utilities.getQueryParam(_this.TEST_MODE_ENABLED) || Demandbase.Config.useTestIp,
          testModeValue: Demandbase.Utilities.getQueryParam(_this.TEST_MODE_VALUE) || Demandbase.Config.testIp
        }, config || Demandbase.Config.IpApiModule);
        _this.initialized = true;
      } catch (e) {
        _this.initialized = false;
      }
      return _this;
    }
    IpApiModule.prototype.initialize = function() {
      try {
        Demandbase.Shims.assign(this.configuration, this.configuration, {
          apiKey: Demandbase.Config.key || Demandbase.Utilities.dig(Demandbase.Config, "analytics", "key") || Demandbase.Utilities.dig(Demandbase.Config, "ads", "key") || Demandbase.Utilities.dig(Demandbase.Config, "forms", "key"),
          testModeEnabled: Demandbase.Utilities.getQueryParam(this.TEST_MODE_ENABLED) || Demandbase.Config.useTestIp,
          testModeValue: Demandbase.Utilities.getQueryParam(this.TEST_MODE_VALUE) || Demandbase.Config.testIp
        });
        this.initialized = true;
      } catch (e) {
        this.initialized = false;
        Demandbase.ErrorReporter.send(e);
      }
    };
    IpApiModule.prototype.buildIPAPIParameters = function(apiKey) {
      return __awaiter(this, void 0, void 0, function() {
        var commonQueryParams, cohort;
        return __generator(this, function(_a) {
          switch (_a.label) {
           case 0:
            commonQueryParams = {
              query: this.fetchIpAddress(),
              mas_integrations: undefined,
              src: "tag"
            };
            if (!document.interestCohort) return [ 3, 2 ];
            return [ 4, document.interestCohort() ];

           case 1:
            cohort = _a.sent();
            commonQueryParams.cohort_id = cohort.id;
            commonQueryParams.cohort_version = cohort.version;
            _a.label = 2;

           case 2:
            if (Demandbase.Config.isVoltronEnabled) {
              return [ 2, Demandbase.Shims.assign(commonQueryParams, {
                auth: apiKey || this.configuration.apiKey
              }) ];
            }
            return [ 2, Demandbase.Shims.assign(commonQueryParams, {
              key: apiKey || this.configuration.apiKey
            }) ];
          }
        });
      });
    };
    IpApiModule.prototype.get = function(apiKey, triggerCallback) {
      if (apiKey === void 0) {
        apiKey = undefined;
      }
      if (triggerCallback === void 0) {
        triggerCallback = true;
      }
      return __awaiter(this, void 0, void 0, function() {
        var request, params, previewToken, thereIsAValidPardotIntegration;
        var _this = this;
        return __generator(this, function(_a) {
          switch (_a.label) {
           case 0:
            if (!this.initialized) {
              this.initialize();
            }
            if (window.XMLHttpRequest) {
              request = new XMLHttpRequest();
            } else if (window.ActiveXObject) {
              request = new ActiveXObject("Microsoft.XMLHTTP");
            }
            if (!(!request || Demandbase.Utilities.isOldBrowserOrUserAgentUnavailable())) return [ 3, 2 ];
            return [ 4, this.getByDomScript(apiKey, triggerCallback) ];

           case 1:
            _a.sent();
            return [ 2, Demandbase.Utilities.Logging.log("IP API query via DOM tag") ];

           case 2:
            return [ 4, this.buildIPAPIParameters(apiKey) ];

           case 3:
            params = _a.sent();
            previewToken = Demandbase.Utilities.getQueryParam(Demandbase.Utilities.Constants.QS_PREVIEW_TOKEN);
            if (previewToken) params.preview_token = previewToken;
            if (!params.key && !params.auth) {
              return [ 2, Demandbase.Utilities.Logging.log("IP API query cancelled - check auth key.") ];
            }
            thereIsAValidPardotIntegration = this.configuration.masIntegrations && this.configuration.masIntegrations.pardot;
            if (!thereIsAValidPardotIntegration) {
              Demandbase.Utilities.Logging.log("No Pardot integration in config, skipping cookie sync");
            } else {
              params.mas_integrations = Demandbase.Utilities.b64EncodeUnicode(Demandbase.Shims.JSON.stringify({
                pardot: this.fetchOrPollForPardotCookie() || {}
              }));
            }
            if (triggerCallback) {
              request.onreadystatechange = Demandbase.ErrorReporter.wrap(function() {
                _this.responseHandler(request);
              });
            }
            try {
              request.open("GET", "https://" + Demandbase.Utilities.Api.buildApiUrl(this.configuration.baseUrl, params));
              if (typeof request.withCredentials !== "undefined") {
                request.withCredentials = true;
              }
              request.send();
            } catch (error) {
              if (request.status === 0) {
                if (!this.isIgnorableDevice()) {
                  throw new Error("IP API Request Blocked");
                }
              } else {
                throw error;
              }
            }
            return [ 2 ];
          }
        });
      });
    };
    IpApiModule.prototype.isIgnorableDevice = function() {
      for (var i = 0; i < Demandbase.Utilities.Constants.NON_HUMAN_DEVICES.length; i++) {
        if (Demandbase.Utilities.Constants.NON_HUMAN_DEVICES[i].test(window.navigator.userAgent)) {
          return true;
        }
      }
      return false;
    };
    IpApiModule.prototype.getByDomScript = function(apiKey, triggerCallback) {
      if (apiKey === void 0) {
        apiKey = undefined;
      }
      if (triggerCallback === void 0) {
        triggerCallback = true;
      }
      return __awaiter(this, void 0, void 0, function() {
        var params, _a, _b, _c;
        return __generator(this, function(_d) {
          switch (_d.label) {
           case 0:
            _b = (_a = Demandbase.Shims).assign;
            _c = [ {} ];
            return [ 4, this.buildIPAPIParameters(apiKey) ];

           case 1:
            params = _b.apply(_a, _c.concat([ _d.sent(), {
              callback: triggerCallback ? "Demandbase.Utilities.Callbacks.domScriptCallback" : ""
            } ]));
            if (!params && !params.auth) {
              return [ 2, Demandbase.Utilities.Logging.log("IP API query cancelled - check auth key.") ];
            }
            Demandbase.Utilities.insertScript(Demandbase.Utilities.Api.buildApiUrl(this.configuration.baseUrl, params), "db_ip_api");
            return [ 2 ];
          }
        });
      });
    };
    IpApiModule.prototype.getOnce = function() {
      if (this.isCalled) {
        Demandbase.Utilities.Logging.log("IP API call halted. Already called.");
        return;
      }
      this.isCalled = true;
      this.get();
    };
    IpApiModule.prototype.fetchIpAddress = function() {
      if (this.configuration.testModeEnabled) {
        return this.configuration.testModeValue;
      }
      return undefined;
    };
    IpApiModule.prototype.responseHandler = function(request) {
      if (request.readyState !== 4 || request.status !== 200) {
        return;
      }
      var responseText = request.responseText;
      try {
        var responseData = Demandbase.Shims.JSON.parse(responseText);
        this.parseResponseForExperiences(responseData);
        this.CompanyProfile = Demandbase.Utilities.flatten(responseData);
        Demandbase.Utilities.Callbacks.callback(this.CompanyProfile);
      } catch (error) {
        Demandbase.ErrorReporter.additionalErrorDetails = {
          status: request.status,
          readyState: request.readyState,
          url: request.responseURL,
          body: responseText
        };
        if (typeof responseText !== "string" || !responseText) {
          throw new Error("responseText should be text and not empty");
        } else {
          throw error;
        }
      }
    };
    IpApiModule.prototype.parseResponseForExperiences = function(responseData) {
      if (responseData && responseData.hasOwnProperty("experiences")) {
        Demandbase.Utilities.Logging.log("IpAPI.parseResponseForExperiences(): Experiences present in IP API response.");
        this.experiences = responseData["experiences"];
      }
      return this.experiences;
    };
    IpApiModule.prototype.fetchOrPollForPardotCookie = function() {
      var thereIsAValidPardotIntegration = this.configuration.masIntegrations && this.configuration.masIntegrations.pardot;
      if (!thereIsAValidPardotIntegration) {
        Demandbase.Utilities.Logging.log("No Pardot integration in config, skipping cookie sync");
        return;
      }
      var pardotCookie = Demandbase.Utilities.getCookiesByRegex(Demandbase.Utilities.Constants.PARDOT_VISITOR_COOKIE_REGEX, document);
      if (typeof pardotCookie === "object" && Demandbase.Shims.keys(pardotCookie).length > 0) {
        Demandbase.Utilities.Logging.log("Found Pardot cookie, including in API request");
        return pardotCookie;
      }
      var pollingShouldBeInitiated = this.configuration.enablePardotPolling && this.pollForPardotStart === 0;
      if (pollingShouldBeInitiated === false) return;
      Demandbase.Utilities.Logging.log("Pardot cookie not found, initiating polling");
      this.pollForPardotCookie();
    };
    IpApiModule.prototype.pollForPardotCookie = function() {
      var _this = this;
      if (this.pollForPardotStart === 0) {
        this.pollForPardotStart = Date.now();
        Demandbase.Utilities.Logging.log("Pardot cookie polling started at " + this.pollForPardotStart);
      }
      var millisSincePollingStarted = Date.now() - this.pollForPardotStart;
      var pollingWindowExceeded = millisSincePollingStarted > this.pardotMaxPollWindow;
      if (pollingWindowExceeded) {
        Demandbase.Utilities.Logging.log("Pardot cookie not found within " + this.pardotMaxPollWindow + " ms");
        return;
      }
      var pardotCookieIsReady = this.fetchOrPollForPardotCookie();
      if (pardotCookieIsReady) {
        Demandbase.Utilities.Logging.log("Pardot cookie found, making second API call");
        this.get(undefined, false);
        return;
      }
      window.setTimeout(function() {
        _this.pollForPardotCookie();
      }, 100);
    };
    return IpApiModule;
  }(Demandbase.BaseModule);
  Demandbase.IpApiModule = IpApiModule;
})(Demandbase || (Demandbase = {}));

var Demandbase;

(function(Demandbase) {
  var SiteCustomizationModule = function(_super) {
    __extends(SiteCustomizationModule, _super);
    function SiteCustomizationModule(config) {
      var _this = _super.call(this) || this;
      _this.DEFAULT_CONFIGURATION = {
        isEnabled: false,
        experiences: {}
      };
      _this.SC_QUERY_PARAMETER_FORCE_FIRE = "db_sc_experience_by_id";
      _this.configuration = Demandbase.Shims.assign({}, _this.DEFAULT_CONFIGURATION);
      _this.wrappedExperiences = {};
      _this.initialized = false;
      _super.prototype.mergeConfigs.call(_this, _this.configuration, _this.DEFAULT_CONFIGURATION, Demandbase.Config.SiteCustomization, config);
      return _this;
    }
    SiteCustomizationModule.prototype.isEnabled = function() {
      return this.configuration.isEnabled === true || this.configuration.enabled === true;
    };
    SiteCustomizationModule.prototype.initialize = function() {
      if (!this.isEnabled()) {
        Demandbase.Utilities.Logging.log("Site Customization is currently disabled, will not fire.");
        return;
      }
      Demandbase.Utilities.Logging.log("SiteCustomization.initialize(): Initializing...");
      this.setup();
      Demandbase.Utilities.Callbacks.registerCallback(this.fireExperienceByQueryParameter.bind(this));
      Demandbase.Utilities.Callbacks.registerCallback(this.callback.bind(this));
    };
    SiteCustomizationModule.prototype.callback = function() {
      Demandbase.Utilities.Logging.log("SiteCustomization.callback(): Invoked! Setting up SC and firing.");
      this.setup();
      this.fireSiteCustomization();
    };
    SiteCustomizationModule.prototype.setup = function(forceRun) {
      if (!forceRun && this.initialized) {
        Demandbase.Utilities.Logging.log("SiteCustomization.setup(): already initilaized! not running setup again.");
        return;
      }
      if (typeof this.configuration.experiences !== "undefined") {
        var rawExperienceObj = this.configuration.experiences || {};
        var allExperienceIds = Demandbase.Shims.keys(rawExperienceObj) || [];
        Demandbase.Utilities.Logging.log("SiteCustomization.setup(): Wrapping " + allExperienceIds.length + " experiences for setup");
        for (var key in rawExperienceObj) {
          var modObj = rawExperienceObj[key];
          var dbExperience = new Experience(modObj);
          if (dbExperience) {
            this.wrappedExperiences[dbExperience.id] = dbExperience;
          }
        }
        this.initialized = true;
      }
    };
    SiteCustomizationModule.prototype.fireSiteCustomization = function() {
      var _this = this;
      return Demandbase.ErrorReporter.wrap(function() {
        var experiencesFromIPAPI = Demandbase.IpApi.experiences;
        Demandbase.Utilities.Logging.log("fireSiteCustomization(): Running for IP API experiences: " + JSON.stringify(experiencesFromIPAPI));
        if (!experiencesFromIPAPI) {
          Demandbase.Utilities.Logging.log("fireSiteCustomization(): Error firing SC experience. IP API response does not contain valid experiences.");
          return false;
        }
        var arrayOfIPAPIExperiences = Object.keys(experiencesFromIPAPI).map(function(key) {
          return experiencesFromIPAPI[key];
        });
        var experiencesToFire = _this.sortExperiencesToFire(arrayOfIPAPIExperiences);
        for (var i = 0; i < experiencesToFire.length; i++) {
          if (_this.applyExperience(experiencesToFire[i].id)) {
            return true;
          }
        }
        return false;
      })();
    };
    SiteCustomizationModule.prototype.sortExperiencesToFire = function(experiencesFromIpAPI) {
      var _this = this;
      if (!experiencesFromIpAPI || !Array.isArray(experiencesFromIpAPI) || experiencesFromIpAPI.length === 0) {
        Demandbase.Utilities.Logging.log("sortExperiencesToFire(): No expereinces returned by IP API: " + JSON.stringify(experiencesFromIpAPI));
        return [];
      }
      experiencesFromIpAPI.sort(function(a, b) {
        var priorityA = _this.wrappedExperiences[a.id] ? _this.wrappedExperiences[a.id].priority : null;
        var priorityB = _this.wrappedExperiences[b.id] ? _this.wrappedExperiences[b.id].priority : null;
        if (!priorityA || !priorityB) {
          Demandbase.Utilities.Logging.log("sortExperiencesToFire(): Warning: priority is not defined " + priorityA + " or " + priorityB);
        }
        if (priorityA === priorityB || (!priorityA || !priorityB)) {
          if (!a.updated_at || !b.updated_at) {
            Demandbase.Utilities.Logging.log("sortExperiencesToFire(): Warning: updated_at is not defined " + a.updated_at + " or " + b.updated_at);
            return 0;
          }
          return new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime();
        }
        return priorityB - priorityA;
      });
      return experiencesFromIpAPI;
    };
    SiteCustomizationModule.prototype.fireExperienceById = function(experienceId) {
      this.setup();
      Demandbase.Utilities.Logging.log("fireExperienceById(): Firing by experience id: " + experienceId);
      return this.applyExperience(experienceId, true);
    };
    SiteCustomizationModule.prototype.fireExperienceByQueryParameter = function() {
      var experienceIdToFire = Demandbase.Utilities.getQueryParam(this.SC_QUERY_PARAMETER_FORCE_FIRE);
      if (experienceIdToFire) {
        Demandbase.Utilities.Logging.log("fireExperienceByQueryParameter(): Firing experience id: " + experienceIdToFire + " now");
        this.setup();
        return this.applyExperience(experienceIdToFire, true);
      }
      Demandbase.Utilities.Logging.log('fireExperienceByQueryParameter(): Not firing experience id: "' + experienceIdToFire + '" as it is not valid');
      return false;
    };
    SiteCustomizationModule.prototype.applyExperience = function(experienceId, forceRun) {
      if (forceRun === void 0) {
        forceRun = false;
      }
      Demandbase.Utilities.Logging.log("applyExperience(): Requested to apply Experience ID: " + experienceId + " with forceRun of " + forceRun);
      if (experienceId && this.wrappedExperiences.hasOwnProperty(experienceId)) {
        var modObj = this.wrappedExperiences[experienceId];
        if (modObj) {
          return forceRun ? modObj.forceRun() : modObj.run();
        }
        Demandbase.Utilities.Logging.log("applyExperience(): Experience ID: " + experienceId + " modobj not truthy: " + JSON.stringify(modObj));
        return false;
      }
      Demandbase.Utilities.Logging.log("applyExperience(): Experience ID: " + experienceId + " not found in " + JSON.stringify(this.wrappedExperiences, null, 4));
      return false;
    };
    return SiteCustomizationModule;
  }(Demandbase.BaseModule);
  Demandbase.SiteCustomizationModule = SiteCustomizationModule;
  var Experience = function() {
    function Experience(exp) {
      this.exp = exp;
      this.isEnabled = false;
      this.priority = null;
      this.id = "";
      this.name = "";
      this.pages = exp.pages || [];
      if (!(this.pages instanceof Array)) {
        this.pages = [ this.pages ];
      }
      this.isEnabled = exp.isEnabled || false;
      this.name = exp.name || "";
      this.id = exp.id || "";
      this.priority = exp.priority || 5e3;
      this.modify = exp.modify || function() {};
    }
    Experience.prototype.forceRun = function() {
      try {
        Demandbase.Utilities.Logging.log("Experience.forceRun: running modify function for: " + this.name);
        this.modify.call(document);
        return true;
      } catch (error) {
        error.name = Demandbase.Utilities.Constants.MODIFICATION_ERROR;
        throw error;
      }
    };
    Experience.prototype.run = function() {
      if (!this.isEnabled) {
        Demandbase.Utilities.Logging.log("Experience.run(): Experience named: " + this.name + " is currently disabled, will not fire.");
        return false;
      }
      var urlMatch = this.doesPageMatch();
      if (!urlMatch) {
        Demandbase.Utilities.Logging.log("Experience.run(): SiteCustomization modify " + this.name + " not fired. no URL match with: " + JSON.stringify(this.pages));
        return false;
      }
      Demandbase.Utilities.Logging.log("Experience.run(): Experience named: " + this.name + " url matched and will run.");
      return this.forceRun();
    };
    Experience.prototype.doesPageMatch = function() {
      Demandbase.Utilities.Logging.log("Experience.doesPageMatch(): Experience named: " + this.name + " checking these URLs: " + JSON.stringify(this.pages));
      for (var index = 0; index < this.pages.length; index++) {
        if (Demandbase.Utilities.isCurrentPage(this.pages[index] || "")) {
          return true;
        }
      }
      return false;
    };
    return Experience;
  }();
  Demandbase.Experience = Experience;
})(Demandbase || (Demandbase = {}));

var Demandbase;

(function(Demandbase) {
  var Domain = function() {
    function Domain() {}
    Domain._callback = function(data) {
      if (!data.domain && !data.person) {
        Demandbase.Utilities.Logging.log("Demandbase.Domain: No company profile available for domain: " + this.getDomain());
        return;
      }
      data = data.domain || data.person;
      var flatData = Demandbase.Utilities.flatten(data);
      this.CompanyProfile = data;
    };
    Domain.load = function() {
      if (typeof Demandbase.Config.getDomain === "function" && this.key !== undefined) {
        var queryDomain = "";
        var params = {};
        if (this.useTestValue) {
          queryDomain = this.testValue;
        } else {
          queryDomain = this.getDomain();
        }
        params = {
          key: this.key,
          callback: "Demandbase.Domain._callback",
          query: queryDomain,
          src: "tag"
        };
        Demandbase.Utilities.Logging.log("Calling Domain API...");
        Demandbase.Utilities.insertScript(Demandbase.Utilities.Api.buildApiUrl(Demandbase.Utilities.Constants.URL_DOMAIN_API, params), "db_domain_api");
      } else {
        Demandbase.Utilities.Logging.log("Domain API query cancelled - check auth key or Config.getDomain");
      }
    };
    Domain.getDomain = function() {
      if (this.useTestValue) {
        return this.testValue;
      }
      if (typeof Demandbase.Config.getDomain === "function") {
        return Demandbase.Config.getDomain.call(Demandbase.Config);
      }
      Demandbase.Utilities.Logging.log("Warning: Config.getDomain fcn not defined.");
      return "getDomain function is not defined";
    };
    Domain.key = Demandbase.Utilities.dig(Demandbase, "Config", "key") || Demandbase.Utilities.dig(Demandbase, "Config", "analytics", "key") || Demandbase.Utilities.dig(Demandbase, "Config", "ads", "key") || Demandbase.Utilities.dig(Demandbase, "Config", "forms", "key") || "ERR_NO_AUTH_KEY";
    Domain.CompanyProfile = null;
    Domain.useTestValue = Demandbase.Utilities.getQueryParam(Demandbase.Utilities.Constants.QS_USE_TEST_DOMAIN) === "true" || Demandbase.Config.useTestDomain || false;
    Domain.testValue = Demandbase.Utilities.getQueryParam(Demandbase.Utilities.Constants.QS_QUERY_DOMAIN) || Demandbase.Config.testDomain || "No Test Domain Set";
    return Domain;
  }();
  Demandbase.Domain = Domain;
})(Demandbase || (Demandbase = {}));

if (typeof window.__db === "undefined") {
  var __db = {
    segments: null,
    conditions: null
  };
}

window.Demandbase.DBCondition = function(name, attrVal, op, val, attrName) {
  this.name = name;
  this.attributeValue = attrVal;
  this.operator = op;
  this.value = val;
  this.attributeName = attrName;
  this._checkValue = function(chkVal) {
    switch (op) {
     case "equals":
      return this.attributeValue == chkVal;

     case "not equals":
      return this.attributeValue !== chkVal;

     case "contains":
      return Demandbase.Shims.indexOf(this.attributeValue, chkVal) !== -1;

     default:
      return false;
    }
  };
  this.evaluate = function() {
    op = this.operator.toLowerCase();
    op = window.Demandbase.DBCondition.prototype.supportedOperators[op];
    if (typeof this.value === "object") {
      for (var eachVal in this.value) {
        if (this._checkValue(this.value[eachVal]) === true) {
          return true;
        }
      }
      return false;
    }
    return this._checkValue(this.value);
  };
};

window.Demandbase.DBCondition.prototype.name = "DBCondition";

window.Demandbase.DBCondition.prototype.supportedOperators = {
  "=": "equals",
  "==": "equals",
  equal: "equals",
  equals: "equals",
  "!=": "not equals",
  "!==": "not equals",
  "not equal": "not equals",
  "not equals": "not equals",
  contains: "contains",
  contain: "contains"
};

window.Demandbase.DBConditionBuilder = {
  isValid: function(condition) {
    var reqdPropsList = [ "name", "attributeValue", "operator", "value", "attributeName" ];
    for (var i = 0; i < reqdPropsList.length; i++) {
      if (typeof condition[reqdPropsList[i]] === "undefined") {
        return false;
      }
    }
    return true;
  },
  build: function(condition, data) {
    if (condition && !condition.name) return null;
    if (typeof condition.constructor.prototype.name !== "undefined" && condition.constructor.prototype.name === "DBCondition") {
      return condition;
    }
    if (!condition.attributeName) condition.attributeName = condition.attribute || "NO_ATTR_SET";
    condition.attributeValue = data[condition.attribute] || "";
    if (!this.isValid(condition)) return null;
    var name = condition.name;
    var apiValue = condition.attributeValue;
    var op = condition.operator;
    var val = condition.value;
    var apiName = condition.attributeName;
    var condObj = new window.Demandbase.DBCondition(name, apiValue, op, val, apiName);
    return condObj;
  }
};

var DBSegment = function(n, c) {
  this.name = n;
  this.rules = [];
  this.operator = "";
  this.addCondition = function(c) {
    if (!c || !c.evaluate) {
      if (typeof c.constructor.prototype.name === "undefined" || c.constructor.prototype.name !== "DBCondition") {
        var c = window.Demandbase.DBConditionBuilder.build(c, window.Demandbase.Segments.CompanyProfile);
        if (!c) {
          throw new Error("Invalid Condition: " + c.name);
        } else {
          Demandbase.Utilities.Logging.log("DBSegmentBuilder converted condition successfully...");
        }
      }
    }
    this.rules.push(c);
    var op = this.operator || DBSegment.prototype.supportedOperators.any;
    switch (op) {
     case "and":
      return this.value = this.value && c.evaluate();

     case "or":
      return this.value = this.value || c.evaluate();

     default:
      return c.evaluate();
    }
  };
  this.value = this.addCondition(c);
};

DBSegment.prototype.name = "DBSegment";

DBSegment.prototype.supportedOperators = {
  "&&": "and",
  "&": "and",
  and: "and",
  "||": "or",
  "|": "or",
  or: "or",
  any: "or",
  all: "and"
};

window.Demandbase.DBSegmentBuilder = {
  isArray: function(arg) {
    if (Array.isArray) {
      return Array.isArray(arg);
    }
    return Object.prototype.toString.call(arg) === "[object Array]";
  },
  isValid: function(segment) {
    var reqdPropsList = [ "name", "operator", "rules" ];
    for (var i = 0; i < reqdPropsList.length; i++) {
      if (typeof segment[reqdPropsList[i]] === "undefined") {
        return false;
      }
    }
    if (!this.isArray(segment.rules)) return false;
    return true;
  },
  build: function(segment) {
    if (!this.isValid(segment)) {
      return null;
    }
    var segmentObj;
    var name = segment.name;
    var condition = segment.rules[0];
    var op = segment.operator;
    if (condition) {
      segmentObj = new DBSegment(name, condition);
      segmentObj.operator = DBSegment.prototype.supportedOperators[op] || DBSegment.prototype.supportedOperators.any;
      if (segment.rules.length > 1) {
        for (var i = 1; i < segment.rules.length; i += 1) {
          var condition = segment.rules[i];
          if (typeof condition.constructor.prototype.name === "undefined" || condition.constructor.prototype.name !== "DBCondition") {
            var dbCond = window.Demandbase.DBConditionBuilder.build(condition, undefined);
            if (dbCond) condition = dbCond;
          }
          segmentObj.addCondition(condition);
        }
      }
      return segmentObj;
    }
  }
};

window.Demandbase.Segments = window.Demandbase.Segments || {
  name: "Demandbase Segments",
  CompanyProfile: null,
  AccountWatchVisitor: false,
  IsCompany: false,
  version: "1.2.2",
  _debug: false,
  _allConditions: [],
  _allSegments: [],
  _isInitialized: false,
  _setup: function() {
    if (this._isInitialized) {
      this._reset();
    }
    if (!this.CompanyProfile && (window.Demandbase.IP || window.Demandbase.Domain)) {
      this.CompanyProfile = window.Demandbase.IP.CompanyProfile || window.Demandbase.Domain.CompanyProfile || {};
    }
    if (this.CompanyProfile.information_level === "Detailed") {
      this.IsCompany = true;
    }
    for (var eachAttr in this.CompanyProfile) {
      if (this.CompanyProfile.hasOwnProperty(eachAttr)) {
        if (Demandbase.Shims.indexOf(eachAttr, "watch_list_") === 0) {
          this.AccountWatchVisitor = true;
        }
      }
    }
    for (var eachCond in this._allConditions) {
      if (this._allConditions.hasOwnProperty(eachCond) && this._allConditions[eachCond] && (typeof this._allConditions[eachCond].constructor.prototype.name === "undefined" || this._allConditions[eachCond].constructor.prototype.name !== "DBCondition")) {
        this.add("condition", this._allConditions[eachCond]);
      }
    }
    for (var eachSegment in this._allSegments) {
      if (this._allSegments.hasOwnProperty(eachSegment) && this._allSegments[eachSegment].name && (typeof this._allSegments[eachSegment].constructor.prototype.name === "undefined" || this._allSegments[eachSegment].constructor.prototype.name !== "DBSegment")) {
        this.add("segment", this._allSegments[eachSegment]);
      }
    }
  },
  _reset: function() {
    this._allConditions = Demandbase.Config.conditions || __db.conditions || [];
    this._allSegments = Demandbase.Config.segments || __db.segments || [];
  },
  load: function() {
    Demandbase.Utilities.Callbacks.registerCallback(this.init.bind(this));
  },
  init: function(data) {
    window.Demandbase.Segments._debug = Demandbase.Utilities.Logging.debug || false;
    window.Demandbase.Segments._allConditions = Demandbase.Config.conditions || __db.conditions || [];
    window.Demandbase.Segments._allSegments = Demandbase.Config.segments || __db.segments || [];
    var dbs = window.Demandbase.Segments;
    dbs.CompanyProfile = data;
    dbs._setup();
    dbs._isInitialized = true;
  },
  getActiveSegments: function() {
    var segList = [];
    for (var eachSegment in this._allSegments) {
      if (this._allSegments.hasOwnProperty(eachSegment)) {
        if (this._allSegments[eachSegment].value) {
          segList.push(this._allSegments[eachSegment]);
        }
      }
    }
    return segList;
  },
  getInactiveSegments: function() {
    var segList = [];
    for (var eachSegment in this._allSegments) {
      if (this._allSegments.hasOwnProperty(eachSegment)) {
        if (!this._allSegments[eachSegment].value) {
          segList.push(this._allSegments[eachSegment]);
        }
      }
    }
    return segList;
  },
  add: function(type, newObject) {
    if (!type || !newObject || newObject == {}) {
      Demandbase.Utilities.Logging.log("Demandbase.Segments.add operation failed due to invalid/empty parameters.");
      return null;
    }
    if (type === "condition") {
      var newCondObj = void 0;
      var condPos = this._allConditions.length;
      for (var eachCond = 0; eachCond < this._allConditions.length; eachCond++) {
        if (this._allConditions[eachCond].name === newObject.name) {
          condPos = eachCond;
          break;
        }
      }
      newCondObj = window.Demandbase.DBConditionBuilder.build(newObject, this.CompanyProfile);
      if (newCondObj) {
        this._allConditions[condPos] = newCondObj;
      } else {
        Demandbase.Utilities.Logging.log("Invalid Condition (not created) from: " + Demandbase.Shims.JSON.stringify(newObject));
      }
      if (typeof newObject.standalone === "undefined" || newObject.standalone !== false) {
        var condName = newObject.name;
        this.add("segment", {
          name: condName,
          rules: [ condName ],
          operator: DBSegment.prototype.supportedOperators.any
        });
      }
    } else if (type === "segment") {
      if (this.isValid(newObject) !== "segment") {
        return null;
      }
      var newSegName = newObject.name;
      var newSegmentObj = void 0;
      var condObj = void 0;
      var segPos = this._allSegments.length;
      var segArr = newObject.rules || [];
      for (var eachSeg = 0; eachSeg < this._allSegments.length; eachSeg++) {
        if (this._allSegments[eachSeg].name === newObject.name) {
          segPos = eachSeg;
          break;
        }
      }
      for (var eachItem = 0; eachItem < segArr.length; eachItem++) {
        var segItem = segArr[eachItem];
        if (DBSegment.prototype.supportedOperators[segItem]) continue;
        if (!DBSegment.prototype.supportedOperators[segItem]) {
          condObj = this.get("condition", segItem);
        }
        if (condObj) {
          segArr[eachItem] = condObj;
        } else {
          Demandbase.Utilities.Logging.log("Segment: " + newObject + " uses a Condition (" + segArr[eachItem] + ") that is not defined.");
        }
      }
      newObject.rules = segArr;
      newSegmentObj = window.Demandbase.DBSegmentBuilder.build(newObject);
      if (newSegmentObj) {
        this._allSegments[segPos] = newSegmentObj;
        if (this.hasOwnProperty(newSegmentObj.name)) {
          this[newSegmentObj.name] = newSegmentObj;
        } else {
          try {
            Object.defineProperty(this, newSegmentObj.name, {
              value: newSegmentObj.value,
              writable: true
            });
          } catch (error) {
            window.Demandbase.Segments[newSegmentObj.name] = newSegmentObj.value;
          }
        }
      } else {
        Demandbase.Utilities.Logging.log("Invalid Segment (not created) from: " + Demandbase.Shims.JSON.stringify(newObject));
      }
    } else {
      Demandbase.Utilities.Logging.log('Invalid "type" parameter (' + type + ') passed to "add" function.  Must be "segment" or "condition".');
    }
  },
  get: function(type, itemName) {
    var itList = [];
    if (arguments.length === 1) itemName = type;
    if (type === "condition") {
      if (typeof itemName.constructor.prototype.name !== "undefined" && itemName.constructor.prototype.name === "DBCondition") {
        return itemName;
      }
      itList = this._allConditions;
    } else {
      if (typeof itemName.constructor.prototype.name !== "undefined" && itemName.constructor.prototype.name === "DBSegment") {
        return itemName;
      }
      itList = this._allSegments;
    }
    for (var eachCond in itList) {
      if (this._allConditions[eachCond].name === itemName) {
        return this._allConditions[eachCond];
      }
    }
    if (!DBSegment.prototype.supportedOperators[itemName]) {
      Demandbase.Utilities.Logging.log('No item with type: "' + type + '" found with name: ' + itemName);
    }
    return null;
  },
  isValid: function(objToCheck) {
    var result;
    var retCondition = "condition";
    var retSegment = "segment";
    var segProps = [ "name", "rules" ];
    var condProps = [ "name", "attribute", "operator", "value" ];
    if (!objToCheck) return false;
    if (typeof objToCheck.constructor.prototype.name !== "undefined" && objToCheck.constructor.prototype.name === "DBSegment") return retSegment;
    if (typeof objToCheck.constructor.prototype.name !== "undefined" && objToCheck.constructor.prototype.name === "DBCondition") return retCondition;
    try {
      if (objToCheck.hasOwnProperty("name") && objToCheck.hasOwnProperty("rules")) {
        if (typeof objToCheck.rules === "object") {
          return retSegment;
        }
      } else {
        for (var prop in segProps) {
          if (!objToCheck.hasOwnProperty(segProps[prop])) {
            Demandbase.Utilities.Logging.log('Invalid DBSegment definition.  Missing property:"' + segProps[prop] + '"');
            return false;
          }
        }
      }
      if (result) return result;
      for (var prop in condProps) {
        if (objToCheck.hasOwnProperty(condProps[prop])) {
          result = retCondition;
        } else {
          Demandbase.Utilities.Logging.log('Invalid DBCondition definition.  Missing property:"' + condProps[prop] + '"');
          return false;
        }
      }
      return result;
    } catch (error) {
      Demandbase.ErrorReporter.send(error);
      return false;
    }
  }
};

var Demandbase;

(function(Demandbase) {
  function initialize(force) {
    if (Demandbase._isInitialized && !force) return;
    Demandbase._isInitialized = true;
    if (Demandbase.Config.isInIFrame == null) {
      Demandbase.Config.isInIFrame = Demandbase.Utilities.detectIFrame();
    }
    Demandbase.AssetReporter = new Demandbase.AssetReporterModule();
    if (Demandbase.AssetReporter.isEnabled()) {
      Demandbase.AssetReporter.initialize();
    }
    Demandbase.Advertising = new Demandbase.AdvertisingModule();
    Demandbase.Ads = Demandbase.Advertising;
    if (Demandbase.Advertising.isEnabled()) {
      Demandbase.IpApiReportingOnly = new Demandbase.IpApiModule();
      Demandbase.Advertising.initialize();
    }
    Demandbase.IpApi = new Demandbase.IpApiModule();
    Demandbase.IP = Demandbase.IpApi;
    Demandbase.IpApi.getOnce();
    window.Demandbase.Segments.load();
    if (Demandbase.Config.callback) {
      Demandbase.Utilities.Callbacks.registerCallback(Demandbase.Config.callback);
    }
    Demandbase.FormsLoader = new Demandbase.FormsLoaderModule();
    if (Demandbase.FormsLoader.isEnabled()) {
      Demandbase.FormsLoader.initialize();
      window.Demandbase.utils.loadFormModule = Demandbase.FormsLoader.load.bind(Demandbase.FormsLoader);
      window.Demandbase.utils.isFormPage = Demandbase.FormsLoader.isFormPage.bind(Demandbase.FormsLoader);
    }
    Demandbase.SiteOptimizationLoader = new Demandbase.SiteOptimizationLoaderModule();
    if (Demandbase.SiteOptimizationLoader.isEnabled()) {
      Demandbase.SiteOptimizationLoader.initialize();
    }
    Demandbase.Connectors.Google_Analytics = new Demandbase.Google_AnalyticsModule();
    if (Demandbase.Connectors.Google_Analytics.isEnabled()) {
      Demandbase.Connectors.Google_Analytics.initialize();
    }
    Demandbase.Connectors.Google_TagManager = new Demandbase.Google_TagManagerModule();
    if (Demandbase.Connectors.Google_TagManager.isEnabled()) {
      Demandbase.Connectors.Google_TagManager.initialize();
    }
    Demandbase.Content = new Demandbase.ContentModule();
    if (Demandbase.Content.isEnabled()) {
      Demandbase.Content.initialize();
    }
    Demandbase.SiteCustomization = new Demandbase.SiteCustomizationModule();
    if (Demandbase.SiteCustomization.isEnabled()) {
      Demandbase.SiteCustomization.initialize();
    }
    if (typeof Demandbase.Config.getDomain === "function") {
      var domain = Demandbase.Config.getDomain();
      if (domain) {
        Demandbase.Domain.load();
      }
    }
    Demandbase.EmailDomainReporter = new Demandbase.EmailDomainReporterModule();
    if (Demandbase.EmailDomainReporter.isEnabled()) {
      Demandbase.EmailDomainReporter.initialize();
    }
    var ConfigPropToConstructorMap = {
      Advertising: Demandbase.AdvertisingModule,
      AssetReporter: Demandbase.AssetReporterModule,
      Content: Demandbase.ContentModule,
      ErrorReporter: Demandbase.ErrorReporterModule,
      Google_Analytics: Demandbase.Google_AnalyticsModule,
      SiteCustomization: Demandbase.SiteCustomization
    };
    new Demandbase.ModuleFactory(Demandbase.Config, ConfigPropToConstructorMap, Demandbase).build();
    if (typeof Demandbase.Config.onLoad === "function") {
      Demandbase.Config.onLoad.call(Demandbase);
    }
  }
  Demandbase.initialize = initialize;
})(Demandbase || (Demandbase = {}));

/*! */Demandbase.Config.Google_Analytics = {
  fieldMap: null
};


Demandbase.Config.forms = {
  "companyID": "noCompanyDB",
  "emailID": "Email",
  "fieldMap": {
    "company_name": "dB1FormCompanyName",
    "industry": "dB1FormIndustry",
    "sub_industry": "tesSubIndustry",
    "annual_sales": "dB1FormRevenue",
    "employee_count": "dB1FormEmployees",
    "web_site": "dB1FormWebsite",
  }
}
  
// Demandbase.Config.isFormPage = function(){ 
//   var testingMode = Demandbase.utils.getQueryParam("testDB");
//   if(testingMode === "forms"){
//     return Demandbase.utils.isFormPage();
//   } else {
//     return false;
//   }
// };
// just a test
    //personalization_site_customization::[{"id": 91, "state": "INACTIVE"}, {"id": 121, "state": "INACTIVE"}, {"id": 122, "state": "ACTIVE"}, {"id": 217, "state": "ACTIVE"}]

        Demandbase.Config.SiteCustomization = {
            "isEnabled": true,
            "experiences": {
              
                    122: {
                        "name": "Redirect-6Sense",
                        "id": 122,
                        "pages": ["www.demandbase.com/6sense"],
                        "isEnabled": true,
                        "modify": function () {
                            if (Demandbase.IP.CompanyProfile.marketing_alias === '6sense Insights'){
                                window.location.replace('https://www.demandbase.com/company/careers/');
                            }
                            
                        }
                    },
                    121: {
                        "name": "Redirect-Terminus",
                        "id": 121,
                        "pages": ["www.demandbase.com/terminus"],
                        "isEnabled": false,
                        "modify": function () {
                            if (Demandbase.IP.CompanyProfile.marketing_alias === 'Terminus Software'){
                                window.location.replace('https://www.demandbase.com/company/careers/');
                            }
                            
                        }
                    },
                    217: {
                                "name": "Career Page Redirect",
                                "priority": "5000",
                                "id": 217,
                                "pages": ["https://support.demandbase.com/hc/en-us"],
                                "isEnabled": true,
                                "modify": function() {
                                  setTimeout(function(){
                                      if (Demandbase.IP.CompanyProfile.web_site === 'adroll.com' || Demandbase.IP.CompanyProfile.web_site === 'rollworks.com' || Demandbase.IP.CompanyProfile.web_site === '6sense.com' || Demandbase.IP.CompanyProfile.web_site === 'terminus.com' || Demandbase.IP.CompanyProfile.web_site === 'zoominfo.com' || Demandbase.IP.CompanyProfile.web_site === 'triblio.com' || Demandbase.IP.CompanyProfile.web_site === 'dnb.com'){
                                              window.location.replace('https://www.demandbase.com/company/careers/');
                                            }
                                        }, 500)
                                   
                    
                                }
                            },
                   

                    91: {
                        "name": "Homepage_Customer",
                        "id": 91,
                        "pages": ["https://www.demandbase.com/"],
                        "isEnabled": false,
                        "modify": function () {
                            
                            document.querySelector(
                                "#cta-topNav-request-demo-popup"
                            ).innerHTML = "Customer Support"
                

                            document.querySelector(
                                "#cta-topNav-request-demo-popup"
                            ).href = "https://support.demandbase.com/"
                            
                            
                

                            document.querySelector(
                                "#cta-merch-3-2021-abm-benchmark-study-revops > .row > .col-xs-9 > .SubheadDarkRegular"
                            ).innerHTML = "For our Customers: 2021 ABM Benchmark Study"
                

                            document.querySelector(
                                "#cta-merch-1-20min-demo"
                            ).href = "https://www.demandbase.com/resources/demandbase-academy/"
                

                            document.querySelector(
                                ".HandwrittenSmallOrangeRegular"
                            ).innerHTML = "Yes, It's Possible! Unified Sales & Marketing"
                

                            document.querySelector(
                                ".col-md-8 > h1"
                            ).innerHTML = "<span class=\"fw-300\">Accelerate Your</span> ABX Expertise"
                

                            document.querySelector(
                                ".col-md-8 > :nth-child(2) > p"
                            ).innerHTML = "Demandbase Academy was designed in-house by our experts for customers like you to increase productivity and maximize the value of your investment. Achieve Demandbase One excellence across your entire team through skills training and enablement. Start Today!"
                

                            document.querySelector(
                                "#cta-homepage-featured-hypercharged-pipeline"
                            ).innerHTML = "Check out Demandbase Academy"
                

                            document.querySelector(
                                "#cta-homepage-featured-hypercharged-pipeline"
                            ).href = "https://www.demandbase.com/resources/demandbase-academy/"
                

                            document.querySelector(
                                ".HandwrittenYellowBold"
                            ).innerHTML = "For Our Customers"
                

                            document.querySelector(
                                ".col-md-6 > .H1WhiteLight"
                            ).innerHTML = "Visit Our Success Center for Support & Resources"
                

                            document.querySelector(
                                "#cta-wide-content-request-demo"
                            ).innerHTML = "Customer Support"
                

                            document.querySelector(
                                "#cta-wide-content-request-demo"
                            ).href = "https://support.demandbase.com/"
                

                            document.querySelector(
                                ".col-md-5 > .H1WhiteLight"
                            ).innerHTML = "Become a Certified Demandbase Expert"
                

                            document.querySelector(
                                "#cta-wide-content-ondemand-demo"
                            ).innerHTML = "Demandbase Academy"
                

                            document.querySelector(
                                "#cta-wide-content-ondemand-demo"
                            ).href = "https://www.demandbase.com/resources/demandbase-academy/"
                

                            document.querySelector(
                              "#cta-merch-1-20min-demo > div > div.col-xs-3.col-lg-4.d-md-none.d-lg-block.pr-3 > img"
                            ).src = "https://www.demandbase.com/wp-content/uploads/demandbase-academy-cap-transparent.png"
                

                            document.querySelector(
                                "body > div.page-default > div.module-featured-resource > div > div > div > div.col-12.col-md-4 > a > img"
                            ).src = "https://www.demandbase.com/wp-content/uploads/demandbase-academy-cap-transparent.png"
                

                            document.querySelector(
                                "#cta-merch-1-20min-demo > .row > .col-xs-9 > .SubheadDarkRegular"
                            ).innerHTML = "Become an Expert with Demandbase Academy"
                            
                            document.querySelector(
                              "#cta-topNav-request-demo-popup"
                              ).dataset.popup = ''
                
                            
                            var addEvent = function(element, evt, func) {
                                if (element.attachEvent) return element.attachEvent("on" + evt, func);
                                else return element.addEventListener(evt, func, false);
                            };

                            window.Demandbase.Connectors.Google_Analytics.sendEvent(
                              "Demandbase - Personalization",
                              "View Page as Experience",
                              "Homepage_CustomerExperience"
                            );

                            addEvent(
                              document.querySelector("#cta-topNav-request-demo-popup"),
                              "click",
                              function() {
                                window.Demandbase.Connectors.Google_Analytics.sendEvent(
                                  "Demandbase - Personalization",
                                  "Click CTA button",
                                  "Hompage_CustomerExperience_CustomerSupportCTA"
                                );
                              }
                            );

                            addEvent(
                              document.querySelector("#cta-merch-1-20min-demo"),
                              "click",
                              function() {
                                window.Demandbase.Connectors.Google_Analytics.sendEvent(
                                  "Demandbase - Personalization",
                                  "Click CTA button",
                                  "Homepage_CustomerExperience_MerchBar_DBAcademyCTA"
                                );
                              }
                            );

                            addEvent(
                              document.querySelector("#cta-homepage-featured-hypercharged-pipeline"),
                              "click",
                              function() {
                                window.Demandbase.Connectors.Google_Analytics.sendEvent(
                                  "Demandbase - Personalization",
                                  "Click CTA button",
                                  "Homepage_CustomerExperience_Featured_DBAcademyCTA"
                                );
                              }
                            );

                            addEvent(
                              document.querySelector("#cta-wide-content-request-demo"),
                              "click",
                              function() {
                                window.Demandbase.Connectors.Google_Analytics.sendEvent(
                                  "Demandbase - Personalization ",
                                  "Click CTA button",
                                  "Homepage_CustomerExperience_WideContent_CustomerSupportCTA_"
                                );
                              }
                            );

                            addEvent(
                              document.querySelector("#cta-wide-content-ondemand-demo"),
                              "click",
                              function() {
                                window.Demandbase.Connectors.Google_Analytics.sendEvent(
                                  "Demandbase - Personalization ",
                                  "Click CTA button",
                                  "Homepage_CustomerExperience_WideContent_DBAcademyCTA"
                                );
                              }
                            );
                        }
                    }
                  }
                }



/* **|**|** SYSTEM GENERATED CODE - DO NOT MODIFY BELOW THIS LINE **|**|** */
Demandbase.Config.clientId = 'be33254a43aa5a3a';
Demandbase.Config.isVoltronEnabled = true;
Demandbase.Config.key = 'engagio_nWJBI2U3pY1JKw8wkeFwb6OMThwTfpfsYa6BRfHS'
Demandbase.Config.Advertising = {
  enableBW: true
};/* !*/

 Demandbase.ErrorReporter = new Demandbase.ErrorReporterModule();

Demandbase.ErrorReporter.initialize();

Demandbase.ErrorReporter.wrap(Demandbase.initialize.bind(Demandbase))();
})(window.Demandbase);
