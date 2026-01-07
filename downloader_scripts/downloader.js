// downloader_scripts/downloader.js
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function downloadFreeFire() {
    console.log('Launching Puppeteer...');
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();

    // تحديد مسار التنزيل داخل بيئة GitHub
    const downloadPath = path.resolve('./');
    await page._client().send('Page.setDownloadBehavior', {
        behavior: 'allow',
        downloadPath: downloadPath,
    });

    const gameUrl = 'https://apkpure.com/garena-free-fire-rampage/com.dts.freefireth/download';
    console.log(`Navigating to ${gameUrl}`);
    await page.goto(gameUrl, { waitUntil: 'networkidle2' });

    console.log('Page loaded. Looking for the download button...');
    
    // انتظر حتى يظهر رابط التنزيل الذي يحتوي على النص "Download XAPK"
    const downloadSelector = 'a.download-btn[href*="download-xapk"]';
    await page.waitForSelector(downloadSelector, { timeout: 60000 });
    
    console.log('Download button found. Clicking it...');
    await page.click(downloadSelector);

    console.log('Download initiated. Waiting for the download to complete...');
    
    // حيلة للانتظار حتى يكتمل التنزيل
    // سننتظر حتى يظهر ملف .crdownload (ملف التنزيل المؤقت) ثم يختفي
    let downloadCompleted = false;
    let attempts = 0;
    const maxAttempts = 180; // 180 محاولة * 5 ثواني = 15 دقيقة كحد أقصى

    while (attempts < maxAttempts) {
        const files = fs.readdirSync(downloadPath);
        const downloadingFile = files.find(file => file.endsWith('.crdownload'));
        
        if (downloadingFile) {
            console.log(`Downloading in progress: ${downloadingFile}`);
        } else {
            // تحقق مما إذا كان هناك ملف xapk موجود
            const xapkFile = files.find(file => file.endsWith('.xapk'));
            if (xapkFile) {
                console.log(`Download completed! File found: ${xapkFile}`);
                // إعادة تسمية الملف إلى اسم ثابت
                fs.renameSync(path.join(downloadPath, xapkFile), path.join(downloadPath, 'freefire.xapk'));
                console.log('File renamed to freefire.xapk');
                downloadCompleted = true;
                break;
            }
        }
        attempts++;
        await new Promise(resolve => setTimeout(resolve, 5000)); // انتظر 5 ثوانٍ
    }

    if (!downloadCompleted) {
        throw new Error('Download did not complete within the time limit.');
    }

    await browser.close();
    console.log('Puppeteer finished successfully.');
}

downloadFreeFire().catch(error => {
    console.error('An error occurred:', error);
    process.exit(1);
});
