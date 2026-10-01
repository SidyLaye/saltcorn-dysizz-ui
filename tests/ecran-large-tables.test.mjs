import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const require = createRequire(path.join(root, "tools", "package.json"));
const { chromium } = require("playwright");
const css = fs.readFileSync(path.join(root, "build", "dz-core.css"), "utf8");
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });

try {
  for (const width of [1697, 1280, 900]) {
    const page = await browser.newPage({ viewport: { width, height: 900 } });
    await page.setContent(`<html><head><style>${css}</style></head><body>
      <main class="dz-ecran" style="--dz-ecran-max:1600px">
        <div class="dz-ecran-grille dz-ecran-principale">
          <section class="dz-ecran-col" data-col="left">
            <div class="dzw-tb" data-card="portfolio"><table style="width:1250px"><tr>
              ${Array.from({ length: 8 }, (_, i) => `<th style="width:155px">Colonne ${i}</th>`).join("")}
            </tr></table></div>
          </section>
          <section class="dz-ecran-col" data-col="right"><div class="dzw-tb" data-card="fiche">Fiche</div></section>
        </div>
      </main></body></html>`);
    const box = async (selector) => page.locator(selector).boundingBox();
    const left = await box('[data-col="left"]');
    const right = await box('[data-col="right"]');
    const card = await box('[data-card="portfolio"]');
    assert.ok(left && right && card);
    if (width > 980) {
      assert.ok(left.x + left.width <= right.x + 1, `colonnes superposées à ${width}px`);
      assert.ok(card.x + card.width <= right.x + 1, `carte sur la fiche à ${width}px`);
    } else {
      assert.ok(left.y + left.height <= right.y + 1, `colonnes superposées à ${width}px`);
    }
    assert.equal(await page.locator('[data-card="portfolio"]').evaluate((e) => e.scrollWidth > e.clientWidth), true);
    await page.close();
  }
  console.log("Grandes tables : colonnes séparées et défilement horizontal à 1697, 1280 et 900 px");
} finally {
  await browser.close();
}
