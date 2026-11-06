// Renders avatar/*.svg, social/*.svg, app-icon/*.svg and banner/*.svg to PNGs next to them, using Playwright's Chromium.
// The avatar and the README banners also get a 2x export. Needs Sauce Code Pro (Nerd Font Mono) installed for the text.
// With arguments (paths to SVGs, relative to the repository root), renders only those.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const root = path.join(__dirname, '..');

const files = process.argv.length > 2 ? process.argv.slice(2)
  : ['avatar', 'social', 'app-icon', 'banner'].flatMap(dir =>
      fs.readdirSync(path.join(root, dir)).filter(f => f.endsWith('.svg')).map(f => path.join(dir, f)));

(async () => {
  const browser = await chromium.launch();
  for (const rel of files) {
    const file = path.resolve(root, rel), dir = path.basename(path.dirname(file));
    const svg = fs.readFileSync(file, 'utf8');
    const [, w, h] = svg.match(/width="(\d+)" height="(\d+)"/);
    const scales = dir === 'avatar' || dir === 'banner' ? [1, 2] : [1];
    for (const scale of scales) {
      const page = await browser.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: scale });
      await page.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
      const out = file.replace(/\.svg$/, scale === 1 ? '.png' : `@${scale}x.png`);
      await page.screenshot({ path: out, omitBackground: true });
      await page.close();
    }
  }
  await browser.close();
})();
