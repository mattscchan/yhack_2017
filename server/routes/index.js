var express = require('express');
var router = express.Router();
var request = require('request');
var PythonShell = require('python-shell');
var fs = require('fs');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.post('/bias', function(req, res, next) {
  var content = req.body.content;
  console.log(content);
  var options = {
    method: "POST",
    url: 'https://language.googleapis.com/v1/documents:analyzeSentiment?key=AIzaSyAFFJOT6JFOIbd6mAVdfREyZ3pVEPtjQRI',
    gzip: true,
    json: {
      "encodingType": "UTF8",
      "document": {
        "type": "PLAIN_TEXT",
        "content": content
      }
    }
  };

  request(options, function(error, response, body) {
    if (response.body) {
      console.log(response.body);
      var sentimentScore = response.body.documentSentiment.score;
      res.send({
        score: sentimentScore,
        isBias: Math.abs(sentimentScore) > 0.4
      })

    } else {
      return {
        score: 123456789,
        isBias: false
      }
    }

  });

});

router.post('/check', function(req, res, next) {
  var target = req.body.target;
  var cluster = req.body.cluster;

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
    args: ['input.json']
  };

  PythonShell.run('ml_model.py', options, function (err, results) {
    if (err) {
      res.send({
        status: 'failed'
      })
    } else {
      // results is an array consisting of messages collected during execution
      var output = require(pathToMatthew + 'output.json');
      console.log('results:', results);
      console.log('output.json:', output);
      res.send({
        status: 'success',
        output: JSON.parse(output)
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
