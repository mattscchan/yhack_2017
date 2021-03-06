var express = require('express');
var router = express.Router();
var request = require('request');
var PythonShell = require('python-shell');
var fs = require('fs');
var pathToMatthew = __dirname + '/../../src/';

router.post('/check', function(req, res, next) {
  console.log('got request', req.body);

  var options = {
    mode: 'text',
    pythonOptions: ['-u'],
    scriptPath: pathToMatthew,
    args: [pathToMatthew + 'input.json'],
    pythonPath: '/usr/bin/python3'
  };

  fs.writeFile(pathToMatthew + 'input.json', JSON.stringify(req.body), 'utf8', function (err) {
    if (err) {
      console.log('error writing file', err);
      res.send({
        status: 'error',
        output: err
      });
    } else {

      PythonShell.run('ml_model.py', options, function (err, results) {
        if (err) {
          console.log('error!', err);
          res.send({
            status: 'error',
            output: {
              payload: [],
              confidence: -1
            }
          })
        } else {
          var output = require(pathToMatthew + '../output.json');
          console.log('output.json:', output);
          res.send({
            status: 'success',
            output: output
          });
        }
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
