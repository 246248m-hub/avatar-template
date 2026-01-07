// viewer_scripts/viewer.js (6 FPS Capture Version)

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const archiver = require('archiver');

// --- إعدادات ---
const VIDEO_URL = 'https://m.youtube.com/watch?v=QMj7MjZNEkg';
const START_SECONDS = 9;
const END_SECONDS = 680; // 11 minutes 20 seconds
const FPS = 6; // <<<--- هذا هو التغيير الوحيد والمهم
// ----------------

const CAPTURE_INTERVAL_MS = 1000 / FPS;
const DURATION_SECONDS = END_SECONDS - START_SECONDS;
const TOTAL_FRAMES = Math.floor(DURATION_SECONDS * FPS);

async function captureFrames() {
    console.log(`Starting frame capture at ${FPS} FPS.`);
    const framesDir = path.join(__dirname, 'frames');
    if (fs.existsSync(framesDir)) {
        fs.rmSync(framesDir, { recursive: true, force: true });
    }
    fs.mkdirSync(framesDir);

    console.log('Launching Puppeteer...');
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 720 });

    const startUrl = `${VIDEO_URL}&t=${START_SECONDS}s`;
    console.log(`Navigating to: ${startUrl}`);
    await page.goto(startUrl, { waitUntil: 'networkidle2' });

    console.log('Page loaded. Waiting for video to start...');
    await new Promise(resolve => setTimeout(resolve, 5000));
    try {
        await page.click('.ytp-large-play-button');
        console.log('Clicked play button.');
    } catch (e) {
        console.log('Play button not found or video already playing.');
    }

    console.log(`Starting capture loop for ${DURATION_SECONDS} seconds. Total frames: ${TOTAL_FRAMES}`);
    let frameCount = 0;
    const captureEndTime = Date.now() + DURATION_SECONDS * 1000;

    const captureLoop = async () => {
        if (Date.now() >= captureEndTime || frameCount >= TOTAL_FRAMES) {
            return;
        }
        
        const framePath = path.join(framesDir, `frame_${String(frameCount).padStart(5, '0')}.jpg`);
        try {
            await page.screenshot({ path: framePath, type: 'jpeg', quality: 80 });
            process.stdout.write(`Captured frame ${++frameCount}/${TOTAL_FRAMES}\r`);
        } catch (error) {
            // تجاهل الأخطاء العشوائية
        }
        
        setTimeout(captureLoop, CAPTURE_INTERVAL_MS);
    };

    await captureLoop();
    await new Promise(resolve => setTimeout(resolve, 2000)); // انتظار إضافي

    console.log(`\nFinished capturing ${frameCount} frames.`);
    await browser.close();

    console.log('Zipping captured frames...');
    const output = fs.createWriteStream(path.join(__dirname, 'captured_frames.zip'));
    const archive = archiver('zip', { zlib: { level: 1 } }); // ضغط سريع
    archive.pipe(output);
    archive.directory(framesDir, false);
    await archive.finalize();

    console.log('Zipping complete. Script finished.');
}

captureFrames().catch(error => {
    console.error('An error occurred:', error);
    process.exit(1);
});
