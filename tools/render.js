// Renders avatar/*.svg, social/*.svg and app-icon/*.svg to PNGs next to them, using Playwright's Chromium.
// The avatar also gets a 2x (1000px) export. Needs Sauce Code Pro (Nerd Font Mono) installed for the text.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const root = path.join(__dirname, '..');

(async () => {
  const browser = await chromium.launch();
  for (const dir of ['avatar', 'social', 'app-icon']) {
    for (const f of fs.readdirSync(path.join(root, dir)).filter(f => f.endsWith('.svg'))) {
      const svg = fs.readFileSync(path.join(root, dir, f), 'utf8');
      const [, w, h] = svg.match(/width="(\d+)" height="(\d+)"/);
      const scales = dir === 'avatar' ? [1, 2] : [1];
      for (const scale of scales) {
        const page = await browser.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: scale });
        await page.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
        const out = f.replace('.svg', scale === 1 ? '.png' : `@${scale}x.png`);
        await page.screenshot({ path: path.join(root, dir, out), omitBackground: true });
        await page.close();
      }
    }
  }
  await browser.close();
})();
