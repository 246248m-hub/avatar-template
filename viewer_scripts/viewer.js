// viewer_scripts/viewer.js

const puppeteer = require('puppeteer');

async function watchYouTube() {
    console.log('Launching Puppeteer...');
    // مهم: يجب تشغيل puppeteer ليتصل بالمتصفح الموجود داخل المحاكي
    // هذه الخطوة معقدة، سنبدأ بتشغيل متصفح عادي أولاً كاختبار
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();

    // تغيير حجم الشاشة ليبدو كشاشة هاتف
    await page.setViewport({ width: 360, height: 640 });

    const videoUrl = 'https://m.youtube.com/watch?v=dQw4w9WgXcQ'; // سنستخدم رابطًا وهميًا للاختبار
    console.log(`Navigating to YouTube video: ${videoUrl}`);
    
    await page.goto(videoUrl, { waitUntil: 'networkidle2' });

    console.log('Page loaded. Taking screenshot...');
    await page.screenshot({ path: 'youtube_page.png' });
    console.log('Screenshot saved as youtube_page.png');

    // هنا سنضيف لاحقًا كود تحليل الإطارات
    console.log('Simulating video watching for 20 seconds...');
    await new Promise(resolve => setTimeout(resolve, 20000));

    await browser.close();
    console.log('Viewer script finished successfully.');
}

watchYouTube().catch(error => {
    console.error('An error occurred:', error);
    process.exit(1);
});
