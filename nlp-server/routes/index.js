var express = require('express');
var router = express.Router();
var request = require('request');
var PythonShell = require('python-shell');
var fs = require('fs');
var pyshell = new PythonShell('ml_model.py', options);

router.post('/check', function(req, res, next) {
  var pathToMatthew = __dirname + '/../../src/';
  fs.writeFile(pathToMatthew + 'input.json', JSON.stringify(req.body), 'utf8', function (err) {
    if (err) {
      return console.log(err);
    }
    console.log("The file was saved!");
  });

  var options = {
    mode: 'text',
    pythonOptions: ['-u'],
    scriptPath: pathToMatthew,
    args: [pathToMatthew + 'input.json'],
    pythonPath: '/usr/bin/python3'
  };

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
  });
});

router.get('/alive', function(req, res, next) {
  res.send({
    status: 'alive'
  });
});

module.exports = router;
