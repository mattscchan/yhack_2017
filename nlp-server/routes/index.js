var express = require('express');
var router = express.Router();
var request = require('request');
var PythonShell = require('python-shell');
var fs = require('fs');
var pathToMatthew = __dirname + '/../../src/';
var options = {
  mode: 'text',
  pythonOptions: ['-u'],
  scriptPath: pathToMatthew,
  args: [pathToMatthew + 'input.json'],
  pythonPath: '/usr/bin/python3'
};

var pyshell = new PythonShell('ml_model.py', options);

pyshell.on('message', function(message) {
  console.log('log:', message);
});

pyshell.on('error', function(error) {
  console.log('error received', error);
});

pyshell.on('close', function(error) {
  console.log('python script closed', error);
});

router.post('/check', function(req, res, next) {
  console.log('got request', req.body);
  fs.writeFile(pathToMatthew + 'input.json', JSON.stringify(req.body), 'utf8', function (err) {
    if (err) {
      console.log('error writing file', err);
      res.send({
        status: 'error',
        output: err
      });
      next();
    } else {
      // sends a message to the Python script via stdin
      pyshell.send(pathToMatthew + 'input.json');

      pyshell.on('message', function (message) {
        var output = require(pathToMatthew + '../output.json');
        console.log('results:', message);
        console.log('output.json:', output);
        res.send({
          status: 'success',
          output: output
        });
        next();
      });

      pyshell.on('error', function(error) {
        console.log('got error', error);
        res.send({
          status: 'error',
          output: error
        });
        next();
      });
    }
  });
});

router.get('/alive', function(req, res, next) {
  res.send({
    status: 'alive'
  });
});

module.exports = router;
