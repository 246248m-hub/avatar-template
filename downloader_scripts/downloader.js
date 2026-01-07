// downloader_scripts/downloader.js (Stealth Version)

// استدعاء الإضافات الجديدة
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

const fs = require('fs');
const path = require('path');

async function downloadFreeFire() {
    console.log('Launching Puppeteer in Stealth Mode...');
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();

    const downloadPath = path.resolve('../'); // <-- تعديل بسيط: التنزيل في المجلد الرئيسي
    await page._client().send('Page.setDownloadBehavior', {
        behavior: 'allow',
        downloadPath: downloadPath,
    });

    const gameUrl = 'https://apkpure.com/garena-free-fire-rampage/com.dts.freefireth/download';
    console.log(`Navigating to ${gameUrl}`);
    await page.goto(gameUrl, { waitUntil: 'networkidle2' });

    console.log('Page loaded. Looking for the download button...');
    
    // حفظ لقطة شاشة للمساعدة في تشخيص المشكلة إذا فشلت مرة أخرى
    await page.screenshot({ path: '../debug_screenshot.png' });
    console.log('Debug screenshot saved.');

    const downloadSelector = 'a.download-btn[href*="download-xapk"]';
    await page.waitForSelector(downloadSelector, { timeout: 60000 });
    
    console.log('Download button found. Clicking it...');
    await page.click(downloadSelector);

    console.log('Download initiated. Waiting for completion...');
    
    let downloadCompleted = false;
    let attempts = 0;
    const maxAttempts = 180;

    while (attempts < maxAttempts) {
        const files = fs.readdirSync(downloadPath);
        const downloadingFile = files.find(file => file.endsWith('.crdownload'));
        
        if (downloadingFile) {
            console.log(`Downloading in progress...`);
        } else {
            const xapkFile = files.find(file => file.endsWith('.xapk'));
            if (xapkFile) {
                console.log(`Download completed! File found: ${xapkFile}`);
                fs.renameSync(path.join(downloadPath, xapkFile), path.join(downloadPath, 'freefire.xapk'));
                console.log('File renamed to freefire.xapk');
                downloadCompleted = true;
                break;
            }
        }
        attempts++;
        await new Promise(resolve => setTimeout(resolve, 5000));
    }

    if (!downloadCompleted) {
        // حفظ لقطة شاشة أخرى عند الفشل
        await page.screenshot({ path: '../debug_screenshot_failure.png' });
        throw new Error('Download did not complete within the time limit.');
    }

    await browser.close();
    console.log('Puppeteer finished successfully.');
}

downloadFreeFire().catch(error => {
    console.error('An error occurred:', error);
    process.exit(1);
});
