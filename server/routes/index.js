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
  var options = {
    method: "POST",
    url: 'http://35.185.14.82:8080/check',
    gzip: true,
    json: {
      target: req.body.target,
      cluster: req.body.cluster
      }
  };

  request(options, function(error, response, body) {
    console.log(response);
    console.log(error);
    if (!error) {
      res.send({
        status: 'success',
        output: response.body
      });
    } else {
      res.send({
        status: 'error',
        error: error
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
