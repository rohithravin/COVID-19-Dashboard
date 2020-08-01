const express = require('express');
const {spawn} = require('child_process');
const router = express.Router();


router.post('/getWorldForecast', (req,res) => {
    console.log(req.body['data'])
    const data = JSON.parse(req.body['data'])
    console.log(`country-forecast.py --getForcast [INFO]: Start.`);
    const subprocess =  spawn('python', ["-u", './scripts/country-forecast.py','--getForcast' , data['traceId'], data['dualDisplay'], data['country'] ]);
    // print output of script
    subprocess.stdout.on('data', (data) => {
        console.log(`country-forecast.py --getForcast [INFO]:${data}`);
        res.send({sucess:100, msg: 'Success.', data:JSON.parse(data.toString().trim())});
    });
    subprocess.stderr.on('data', (data) => {
        console.log(`country-forecast.py --getForcast [ERROR]:${data}`);
        res.send({sucess:501, msg:data.toString().trim()});
    });
    subprocess.on('close', () => {
        console.log("country-forecast.py --getForcast [INFO]: Closed.");
    });
})

router.post('/verifyCountry', (req,res) => {
    console.log(req.body['data'])
    const data = JSON.parse(req.body['data'])
    console.log(`country-forecast.py --validateCountry [INFO]: Start.`);
    const subprocess =  spawn('python', ["-u", './scripts/country-forecast.py','--validateCountry' , data['country'] ]);
    // print output of script
    subprocess.stdout.on('data', (data) => {
        console.log(`country-forecast.py --validateCountry [INFO]:${data}`);
        res.send({sucess:100, msg: 'Success.', data:JSON.parse(data.toString().trim())});
    });
    subprocess.stderr.on('data', (data) => {
        console.log(`country-forecast.py --validateCountry [ERROR]:${data}`);
        res.send({sucess:501, msg:data.toString().trim()});
    });
    subprocess.on('close', () => {
        console.log("country-forecast.py --validateCountry [INFO]: Closed.");
    });
})






module.exports = router;
