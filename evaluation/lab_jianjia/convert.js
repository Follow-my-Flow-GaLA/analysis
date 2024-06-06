const
	arraySyntax = /\[([^\]]*)]/g,
	normalizeURLRgxp = /[^?]*\?/;
Object.isPlainObject = function(val) {
  return !!val && typeof val === "object" && val.constructor === ({}).constructor;
};
var url_convert={};
url_convert.fromQueryString = function(
	query,
	optsOrDecode
) {
	query = query.replace(normalizeURLRgxp, '');

	const
		queryObj = {};

	if (query === '') {
		return queryObj;
	}

	let
		opts;

	if (Object.isPlainObject(optsOrDecode)) {
		opts = optsOrDecode;

	} else {
		opts = {decode: optsOrDecode};
	}

	if (opts.decode !== false) {
		query = decodeURIComponent(query);
	}

	const
		indexes = {},
		//indexes = Object.createDict<number>(),
		objOpts = {separator: opts.arraySyntax ? ']' : opts.separator},
		variables = query.split('&');

	for (let i = 0; i < variables.length; i++) {
		let
			[key, val = null] = variables[i].split('=');

		if (opts.arraySyntax) {
			let
				path = '',
				nestedArray = false;

			key = key.replace(arraySyntax, (str, prop, lastIndex) => {
				if (path === '') {
					path += key.slice(0, lastIndex);
				}

				path += str;

				if (prop === '') {
					if (nestedArray) {
						prop = '0';

					} else {
						prop = indexes[path] || '0';
						indexes[path] = Number(prop) + 1;
					}

					nestedArray = true;
				}

				return `]${prop}`;
			});
		}
		const
            oldVal = objOpts.separator != null ? Object.get(queryObj, key, objOpts) : queryObj[key];

        let
            normalizedVal = opts.convert !== false ? Object.parse(val, convertIfDate) : val;

        if (oldVal !== undefined) {
            normalizedVal = Array.concat([], oldVal, Object.isArray(normalizedVal) ? [normalizedVal] : normalizedVal);
        }

        if (objOpts.separator != null) {
            Object.set(queryObj, key, normalizedVal, objOpts);

        } else {
            queryObj[key] = normalizedVal;
        }
	}

	return queryObj;
};
url_convert.fromQueryString(location.search, {arraySyntax: true});
