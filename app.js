// app.js
const express = require('express');
const cron = require('node-cron');
const { spawn } = require('child_process');

const app = express();

// Define a cron job to run the Python script every 2 minutes
cron.schedule('*/2 * * * *', () => {
    const pyProcess = spawn('python', ['main.py']);
    pyProcess.stdout.on('data', (data) => {
        console.log(`Python script output: ${data}`);
    });
    pyProcess.stderr.on('data', (data) => {
        console.error(`Error executing Python script: ${data}`);
    });
});

// Start the Express server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
