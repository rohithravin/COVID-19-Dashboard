const express = require('express');
const {spawn} = require('child_process');
const router = express.Router();

router.post('/getWorldPlot', (req,res) => {
    const data = JSON.parse(req.body['data'])
    console.log(`world-dashboard.py --updateWorldPlot [INFO]: Start.`);
    const subprocess =  spawn('python', ["-u", './scripts/world-dashboard.py','--updateWorldPlot' , data['plotTraceId'], data['plotTimeline'] ]);
    // print output of script
    subprocess.stdout.on('data', (data) => {
        console.log(`world-dashboard.py --updateWorldPlot [INFO]:${data}`);
        res.send({sucess:100, msg: 'Success.', data:JSON.parse(data.toString().trim())});
    });
    subprocess.stderr.on('data', (data) => {
        console.log(`world-dashboard.py --updateWorldPlot [ERROR]:${data}`);
        res.send({sucess:501, msg:data.toString().trim()});
    });
    subprocess.on('close', () => {
        console.log("world-dashboard.py --updateWorldPlot [INFO]: Closed.");
    });
})

router.post('/getTopCountriesData', (req,res) => {
    const data = JSON.parse(req.body['data'])
    console.log(data)
    console.log(`world-dashboard.py --updateTopCountriesData [INFO]: Start.`);
    const subprocess =  spawn('python', ["-u", './scripts/world-dashboard.py','--updateTopCountriesData' , data['plotTraceId'], data['numLimit'] ]);
    // print output of script
    subprocess.stdout.on('data', (data) => {
        console.log(`world-dashboard.py --updateTopCountriesData [INFO]:${data}`);
        res.send({sucess:100, msg: 'Success.', data:JSON.parse(data.toString().trim())});
    });
    subprocess.stderr.on('data', (data) => {
        console.log(`world-dashboard.py --updateTopCountriesData [ERROR]:${data}`);
        res.send({sucess:501, msg:data.toString().trim()});
    });
    subprocess.on('close', () => {
        console.log("world-dashboard.py --updateTopCountriesData [INFO]: Closed.");
    });
})

router.post('/getTopCountriesPlots', (req,res) => {
    const data = JSON.parse(req.body['data'])
    console.log(data)
    console.log(`world-dashboard.py --updateTopCountriesPlot [INFO]: Start.`);
    const subprocess =  spawn('python', ["-u", './scripts/world-dashboard.py','--updateTopCountriesPlot', data['plotTraceId'], data['plotTimeline'], data['numLimit'] ]);
    // print output of script
    subprocess.stdout.on('data', (data) => {
        console.log(`world-dashboard.py --updateTopCountriesPlot [INFO]:${data}`);
        res.send({sucess:100, msg: 'Success.', data:JSON.parse(data.toString().trim())});
    });
    subprocess.stderr.on('data', (data) => {
        console.log(`world-dashboard.py --updateTopCountriesPlot [ERROR]:${data}`);
        res.send({sucess:501, msg:data.toString().trim()});
    });
    subprocess.on('close', () => {
        console.log("world-dashboard.py --updateTopCountriesPlot [INFO]: Closed.");
    });
})

module.exports = router;