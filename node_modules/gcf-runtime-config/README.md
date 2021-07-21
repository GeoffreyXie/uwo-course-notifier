# gcf-runtime-config 

[`gcf-runtime-config`](https://www.npmjs.com/package/gcf-runtime-config) helps you
get environment variables within Google Cloud Functions (GCF) through
[`Runtime Config`](https://cloud.google.com/deployment-manager/runtime-configurator/reference/rest/).

[![CircleCI](https://circleci.com/gh/Noless/gcf-runtime-config.svg?style=svg)](https://circleci.com/gh/Noless/gcf-runtime-config)
[![Coverage Status](https://coveralls.io/repos/github/Noless/gcf-runtime-config/badge.svg?branch=master)](https://coveralls.io/github/Noless/gcf-runtime-config?branch=master)
[![MIT License](https://img.shields.io/npm/l/gcf-runtime-config.svg?style=flat-square)](http://opensource.org/licenses/MIT)
[![version](https://img.shields.io/npm/v/gcf-runtime-config.svg?style=flat-square)](http://npm.im/gcf-runtime-config)

## Usage

### Install it:
~~~bash
$ npm install --save gcf-runtime-config
~~~

### Enable Google Cloud's Runtime Config API:
~~~bash
$ gcloud services enable runtimeconfig.googleapis.com
~~~

Create a new config:
~~~
$ gcloud beta runtime-config configs create EXAMPLE_ENVIRONMENT 
$ gcloud beta runtime-config configs variables \
    set PAYPAL_SECRET_KEY "NOTREAL1234!@#$" \
    --config-name EXAMPLE_ENVIRONMENT \
    --is-text
$ gcloud beta runtime-config configs variables \
    set STRIPE_SECRET_KEY "YESREAL1234!@#$" \
    --config-name EXAMPLE_ENVIRONMENT \
    --is-text
~~~

### Sample function code:
~~~javascript
const gcfRuntimeConfig = require('gcf-runtime-config');

exports.testRuntimeConfig = (req, res) => {
  gcfRuntimeConfig
    .getVariables('EXAMPLE_ENVIRONMENT')
    .then(variablesObj => res.send(variablesObj))
    .catch(err => res.send(err));
};
~~~

The [`example`](https://github.com/noless/gcf-runtime-config/tree/master/example)
directory is a ready-to-deploy sample function that uses
[`gcf-runtime-config`](https://www.npmjs.com/package/gcf-runtime-config) 
and extracts a runtime config (environment).


### Deploy:

~~~ bash
$ gcloud beta functions deploy testExpressApp --trigger-http
~~~

### Test:
~~~ bash
$ curl https://<YOUR_PROJECT>.cloudfunctions.net/testRuntimeConfig
{"PAYPAL_SECRET_KEY":"NOTREAL1234!@#$","STRIPE_SECRET_KEY":"YESREAL1234!@#$"}
~~~

### Cleanup:
~~~ bash
$ gcloud beta functions delete testExpressApp
~~~

## API

### runtimeConfig.getVariables(config[, objectify=true])

**Arguments:**
- **config** is a the name of the config, in our example its `EXAMPLE_ENVIRONMENT`.
- **objectify** defaults to **true**, it means the function resolves to an object 
where its keys and values are the variable names and values. 
  * **objectify=true** in our example results in: `{"PAYPAL_SECRET_KEY":"NOTREAL1234!@#$","STRIPE_SECRET_KEY":"YESREAL1234!@#$"}`
  * **objectify=false** in our example results in: `[{"name":"STRIPE_SECRET_KEY","updateTime":"2018-05-20T09:53:11.383980095Z","text":"YESREAL1234!@#$"},{"name":"PAYPAL_SECRET_KEY","updateTime":"2018-05-20T09:53:09.683262561Z","text":"NOTREAL1234!@#$"}]`

**Returns:**
A `Promise` that depending on `objectify` resolves to either an object where its
keys and values are the config's parameters and values or to an array of parameter objects.

## Why 

We needed a way to inject secret keys to a Google Cloud Function.
Storing keys in code base is wrong.

## License

MIT
