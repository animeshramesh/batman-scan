var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.sendFile("/Users/admin/Downloads/batman-scan/maps/views/index.html"); 
});

module.exports = router;
