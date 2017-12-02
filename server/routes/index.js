var express = require('express');
var router = express.Router();
var request = require('request');
var PythonShell = require('python-shell');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.post('/check/', function(req, res, next) {
  var target = req.body.target;
  var cluster = req.body.cluster;

  // var parsedQuery = title.split(" ").join("+").replace(/<[^<>]*>/g, "");
  //
  // var options = {
  //   method: "GET",
  //   url: 'https://api.cognitive.microsoft.com/bing/v7.0/news/search',
  //   gzip: true,
  //   headers: {
  //     "Ocp-Apim-Subscription-Key": "c87d294a9c8e4effb43d6a3d0ef9859b"
  //   },
  //   qs: {
  //     "q": parsedQuery,
  //     "mkt": "en-us"
  //   }
  // };
  //
  // request(options, function(error, response, body) {
  //   if (response.body) {
  //     response.body.value
  //   }
  //
  // });

  var options = {
    mode: 'text',
    pythonPath: 'path/to/python',
    pythonOptions: ['-u'],
    scriptPath: 'path/to/my/scripts',
    args: ['value1', 'value2', 'value3']
  };

  PythonShell.run('my_script.py', options, function (err, results) {
    if (err) throw err;
    // results is an array consisting of messages collected during execution
    console.log('results: %j', results);
  });


});

router.get('/alive', function(req, res, next) {
  res.send({
    status: 'alive'
  });
});

module.exports = router;
