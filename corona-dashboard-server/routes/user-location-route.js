const express = require('express');
const router = express.Router();

router.get('/getUserLocation', (req,res) => {
    console.log('i am here.')
    res.send({sucess:100, msg:'i am here.'});
})

module.exports = router;