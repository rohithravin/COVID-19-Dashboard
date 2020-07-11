const express = require('express');
const {spawn} = require('child_process');
const router = express.Router();

router.post('/getDailyData', (req,res) => {
    console.log(`cali-dashboard.py --calDailyData [INFO]: Start.`);
    const subprocess =  spawn('python', ["-u", './scripts/cali-dashboard.py','--calDailyData' , JSON.parse(req.body['county'])  ]);
    // print output of script
    subprocess.stdout.on('data', (data) => {
        console.log(`ali-dashboard.py --calDailyData [INFO]:${data}`);
        res.send({sucess:100, msg: 'Success.', data:JSON.parse(data.toString().trim())});
    });
    subprocess.stderr.on('data', (data) => {
        console.log(`ali-dashboard.py --calDailyData [ERROR]:${data}`);
        res.send({sucess:501, msg:data.toString().trim()});
    });
    subprocess.on('close', () => {
        console.log("uali-dashboard.py --calDailyData [INFO]: Closed.");
    });
    
})

module.exports = router;