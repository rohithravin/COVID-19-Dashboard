const express = require('express');
const {spawn} = require('child_process');
const router = express.Router();

router.post('/getUserLocation', (req,res) => {
    console.log(`user-location.py [INFO]: Start.`);
    const subprocess =  spawn('python', ["-u", './scripts/user-location.py',parseInt(req.body['zipcode'])]);
    // print output of script
    subprocess.stdout.on('data', (data) => {
        console.log(`user-location.py [INFO]:${data}`);
        res.send({sucess:100, msg: 'Success.', data:JSON.parse(data.toString().trim())});
    });
    subprocess.stderr.on('data', (data) => {
        console.log(`user-location.py [ERROR]:${data}`);
        res.send({sucess:501, msg:data.toString().trim()});
    });
    subprocess.on('close', () => {
        console.log("user-location.py [INFO]: Closed.");
    });
    
})

module.exports = router;