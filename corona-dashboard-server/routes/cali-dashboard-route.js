const express = require('express');
const {spawn} = require('child_process');
const router = express.Router();

router.post('/getDailyData', (req,res) => {
    console.log(`cali-dashboard.py --calDailyData [INFO]: Start.`);
    const subprocess =  spawn('python', ["-u", './scripts/cali-dashboard.py','--calDailyData' , JSON.parse(req.body['county'])  ]);
    // print output of script
    subprocess.stdout.on('data', (data) => {
        console.log(`cali-dashboard.py --calDailyData [INFO]:${data}`);
        res.send({sucess:100, msg: 'Success.', data:JSON.parse(data.toString().trim())});
    });
    subprocess.stderr.on('data', (data) => {
        console.log(`cali-dashboard.py --calDailyData [ERROR]:${data}`);
        res.send({sucess:501, msg:data.toString().trim()});
    });
    subprocess.on('close', () => {
        console.log("cali-dashboard.py --calDailyData [INFO]: Closed.");
    });
})

router.post('/getPlotNewKind', (req,res) => {
    const data = JSON.parse(req.body['data'])
    console.log(`cali-dashboard.py --updateNewPlot [INFO]: Start.`);
    console.log(data['county'])
    const subprocess =  spawn('python', ["-u", './scripts/cali-dashboard.py','--updateNewPlot' , data['plotKindId'], data['plotTraceId'], data['plotTimeline'], data['county'] ]);
    // print output of script
    subprocess.stdout.on('data', (data) => {
        console.log(`cali-dashboard.py --updateNewPlot [INFO]:${data}`);
        res.send({sucess:100, msg: 'Success.', data:JSON.parse(data.toString().trim())});
    });
    subprocess.stderr.on('data', (data) => {
        console.log(`cali-dashboard.py --updateNewPlot [ERROR]:${data}`);
        res.send({sucess:501, msg:data.toString().trim()});
    });
    subprocess.on('close', () => {
        console.log("cali-dashboard.py --updateNewPlot [INFO]: Closed.");
    });
})

router.post('/getPlotTotalKind', (req,res) => {
    res.send({sucess:100, msg: 'Success.', data:req.body});
})

module.exports = router;