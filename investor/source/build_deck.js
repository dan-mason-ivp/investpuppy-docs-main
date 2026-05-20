"use strict";
/**
 * InvestPuppy — Seed Round Investor Deck  v2
 * Rebuilt per panel feedback:
 * — Brand voice throughout (direct, honest, specific)
 * — Vektor identity on product slides (gold #C8A96E, V3 logo)
 * — Slide 4: Vektor (merged solution+platform, dual-brand)
 * — Slide 5: What Vektor Is Not (new)
 * — Slide 8: Traction rewritten in brand voice
 * — Slide 10: Use of Funds + Milestone Timeline
 * — Slide 11: Ask rewritten — direct
 * — White paper series + Unvarnished surfaced explicitly
 */
const pptxgen = require("pptxgenjs");
const path    = require("path");
const fs      = require("fs");

const REPO    = path.resolve(__dirname, "../..");
const LOGOS   = path.join(REPO, "_shared", "logos");
const OUT_DIR = path.resolve(__dirname, "../output/pptx");
fs.mkdirSync(OUT_DIR, { recursive: true });
const OUT     = path.join(OUT_DIR, "ip-investor-deck.pptx");

const LOGO_D   = path.join(LOGOS, "ip_logo_dark_bg.png");
const LOGO_L   = path.join(LOGOS, "ip_logo_light_bg.png");
const VEKTOR_L = path.join(LOGOS, "VEKTOR-transparent-v3.png");

const IP_RATIO = 911 / 746;   // 1.221
const VK_RATIO = 1030 / 496;  // 2.077

const GREEN   = "85D155";
const GOLD    = "C8A96E";
const DARKBG  = "0F0F14";
const VEKTBG  = "0A0A0F";
const WHITE   = "FFFFFF";
const TEXT    = "1A1A1A";
const MID     = "5A5A5A";
const CARD    = "F3F4F3";
const BORDER  = "E2E2E2";

const pres  = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "InvestPuppy";
pres.title  = "InvestPuppy — Seed Round Investor Deck";

const mkShadow = () => ({ type:"outer", color:"000000", blur:5, offset:1, angle:135, opacity:0.07 });

function footer(s, dark = false) {
  s.addText("InvestPuppy · investpuppy.com · contact@investpuppy.com · CONFIDENTIAL",
    { x:0.4, y:5.44, w:8.3, h:0.16, margin:0, fontSize:6.5,
      color: dark ? "444444" : "CCCCCC", fontFace:"Poppins", valign:"middle" });
  const lh = 0.2, lw = +(lh * IP_RATIO).toFixed(3);
  s.addImage({ path: dark ? LOGO_D : LOGO_L, x:9.5-lw, y:5.38, w:lw, h:lh });
}

function secLabel(s, t, color = GREEN) {
  s.addText(t.toUpperCase(), { x:0.5, y:0.27, w:6, h:0.22, margin:0,
    fontSize:7, color, fontFace:"Poppins", bold:true, charSpacing:1.5, valign:"middle" });
}

function title(s, t, color = TEXT) {
  s.addText(t, { x:0.5, y:0.55, w:9, h:0.7, margin:0,
    fontSize:26, color, fontFace:"Poppins", bold:true, valign:"middle" });
}

function card(s, x, y, w, h, fill = CARD) {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h,
    fill:{ color:fill }, line:{ color:BORDER, width:0.5 }, shadow:mkShadow() });
}

function accentCard(s, x, y, w, h, ac = GREEN) {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h,
    fill:{ color:CARD }, line:{ color:BORDER, width:0.5 }, shadow:mkShadow() });
  s.addShape(pres.shapes.RECTANGLE, { x, y, w:0.045, h,
    fill:{ color:ac }, line:{ color:ac, width:0 } });
}

function dot(s, x, y, d = 0.1, c = GREEN) {
  s.addShape(pres.shapes.OVAL, { x:x-d/2, y:y-d/2, w:d, h:d,
    fill:{ color:c }, line:{ color:c, width:0 } });
}

function bigCircle(s, cx, cy, d, op = 0.12, c = GREEN) {
  s.addShape(pres.shapes.OVAL, { x:cx-d/2, y:cy-d/2, w:d, h:d,
    fill:{ color:c, transparency:Math.round((1-op)*100) },
    line:{ color:c, width:0 } });
}

// ── SLIDE 1 — Cover ────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color:DARKBG };
  bigCircle(s, 9.0, 1.4, 2.4, 0.10);
  bigCircle(s, 9.4, 4.2, 1.0, 0.15);

  const lh = 0.72, lw = +(lh*IP_RATIO).toFixed(3);
  s.addImage({ path:LOGO_D, x:0.5, y:0.36, w:lw, h:lh });

  s.addShape(pres.shapes.RECTANGLE, { x:0.5, y:1.1, w:2.55, h:0.28,
    fill:{ color:"1D1D24" }, line:{ color:"333340", width:0.5 } });
  s.addText("SEED ROUND  ·  S$1M – S$2M", { x:0.5, y:1.1, w:2.55, h:0.28, margin:0,
    fontSize:7.5, color:GREEN, fontFace:"Poppins", bold:true,
    align:"center", valign:"middle", charSpacing:0.8 });

  s.addText([
    { text:"Systematic equity intelligence", options:{ breakLine:true } },
    { text:"for serious portfolio managers.", options:{ color:GREEN } }
  ], { x:0.5, y:1.62, w:7.6, h:1.5, margin:0,
    fontSize:34, fontFace:"Poppins", bold:true, color:WHITE, valign:"middle" });

  s.addText(
    "We are pre-revenue. The platform is built and runs in simulation mode. " +
    "We are raising S$1–2M to make it live. This is the honest case for why that is interesting.",
    { x:0.5, y:3.28, w:6.8, h:0.95, margin:0,
      fontSize:11, color:"888888", fontFace:"Poppins", valign:"top" });

  s.addText("contact@investpuppy.com  ·  investpuppy.com",
    { x:0.5, y:5.12, w:5, h:0.24, margin:0,
      fontSize:8, color:"555555", fontFace:"Poppins", valign:"middle" });
  s.addText("CONFIDENTIAL", { x:7.6, y:5.12, w:1.9, h:0.24, margin:0,
    fontSize:7, color:"404040", fontFace:"Poppins",
    bold:true, align:"right", valign:"middle", charSpacing:1.5 });
}

// ── SLIDE 2 — The Problem ──────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color:WHITE };
  secLabel(s, "The Problem");
  title(s, "Wealth managers are flying blind.");

  s.addText(
    "Boutique DPMs, independent RIAs, and family offices manage real money for real clients. " +
    "They know systematic portfolio construction matters. But institutional-grade quant tools " +
    "are built — and priced — for institutions. The middle market is ignored.",
    { x:0.5, y:1.38, w:4.3, h:1.05, margin:0, fontSize:10.5, color:MID, fontFace:"Poppins", valign:"top" });

  s.addText("~$32,000", { x:0.5, y:2.55, w:3.2, h:0.82, margin:0,
    fontSize:46, color:TEXT, fontFace:"Poppins", bold:true, valign:"middle" });
  s.addText("Bloomberg Terminal — per seat, per year (2026 verified).\nBefore Bloomberg PORT or any quant tooling is added.",
    { x:0.5, y:3.4, w:4.3, h:0.52, margin:0, fontSize:9.5, color:MID, fontFace:"Poppins", valign:"top" });
  s.addText(
    "Enterprise platforms (Refinitiv, FactSet) run $24K–$50K+ per seat. " +
    "The managers who need systematic tools most cannot access them.",
    { x:0.5, y:4.05, w:4.3, h:0.56, margin:0,
      fontSize:9.5, color:TEXT, fontFace:"Poppins", bold:true, valign:"top" });

  const ps = [
    { head:"Priced for institutions",
      body:"Bloomberg and FactSet charge tens of thousands per seat. Bespoke quant builds take years. Boutique managers face a bill designed for large buy-side desks." },
    { head:"Built for institutions",
      body:"Existing platforms assume large quant teams and complex infrastructure. Boutique managers get the wrong product even when they can afford the price tag." },
    { head:"No credible middle-market option",
      body:"Spreadsheets and gut feel fill the gap. Portfolio construction decisions lack rigour — not from lack of ambition, but lack of accessible tools." },
  ];
  let py = 1.33;
  for (const p of ps) {
    accentCard(s, 5.1, py, 4.4, 1.04);
    s.addText(p.head, { x:5.25, y:py+0.1, w:4.1, h:0.26, margin:0, fontSize:10.5, color:TEXT, fontFace:"Poppins", bold:true, valign:"middle" });
    s.addText(p.body, { x:5.25, y:py+0.38, w:4.1, h:0.58, margin:0, fontSize:8.8, color:MID, fontFace:"Poppins", valign:"top" });
    py += 1.17;
  }
  footer(s);
}

// ── SLIDE 3 — Why Now ──────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color:WHITE };
  secLabel(s, "Why Now");
  title(s, "Three forces converging — right now.");

  const cols = [
    { num:"01", head:"Singapore's wealth\nmanagement moment",
      body:"MAS-regulated clarity, a dense independent advisor community, and record family office formation make Singapore the world's cleanest entry point. 2,000+ single family offices (MAS, 2024). 500+ independent wealth managers. The regulatory framework is settled. The clients are here. The timing is precise." },
    { num:"02", head:"The cost of systematic\nanalysis has collapsed",
      body:"Running 10,000 portfolio configurations was computationally expensive a decade ago. Today it is not. The infrastructure exists to deliver institutional-grade systematic analysis at a fraction of historical cost. No one has productised this for the wealth management middle market." },
    { num:"03", head:"Incumbents have no\nincentive to move",
      body:"Bloomberg and FactSet price for large institutions — their economics depend on it. The boutique wealth manager segment is too fragmented for them to serve directly. This gap is structural, not temporary. It will not be closed by the incumbents." },
  ];
  const xs = [0.5, 3.55, 6.6];
  for (let i = 0; i < cols.length; i++) {
    const { num, head, body } = cols[i]; const x = xs[i];
    card(s, x, 1.35, 2.85, 3.78);
    s.addText(num, { x:x+0.2, y:1.48, w:0.9, h:0.52, margin:0, fontSize:28, color:GREEN, fontFace:"Poppins", bold:true, valign:"middle" });
    s.addText(head, { x:x+0.2, y:2.06, w:2.45, h:0.62, margin:0, fontSize:11, color:TEXT, fontFace:"Poppins", bold:true, valign:"top" });
    s.addText(body, { x:x+0.2, y:2.74, w:2.45, h:2.2, margin:0, fontSize:9, color:MID, fontFace:"Poppins", valign:"top" });
  }
  footer(s);
}

// ── SLIDE 4 — Vektor (merged solution+platform, dual-brand) ───────────────────
{
  const s = pres.addSlide();
  s.background = { color:WHITE };
  secLabel(s, "The Platform");
  title(s, "Vektor.");

  s.addText(
    "Vektor is a systematic listed equity portfolio management platform " +
    "built specifically for boutique wealth managers, family offices, and independent RIAs. " +
    "It delivers institutional-grade rigour — without the institutional price tag, " +
    "team size, or infrastructure requirement.",
    { x:0.5, y:1.38, w:4.5, h:0.88, margin:0, fontSize:10.5, color:MID, fontFace:"Poppins", valign:"top" });

  const caps = [
    { label:"10,000 portfolio configurations per strategy", body:"Systematic construction at scale. Not guesswork. Not intuition." },
    { label:"Market-agnostic architecture", body:"Any listed equity exchange, any currency. SGX is the primary use case." },
    { label:"Workflow-native integration", body:"Sits alongside existing custody and reporting infrastructure." },
    { label:"Data-layer independent", body:"Runs on IBKR market data as standard. Does not require Bloomberg feeds. Custom data connections available." },
    { label:"Audit-ready output", body:"99.94% availability target. Every decision documented from day one." },
  ];
  let dy = 2.34;
  for (const cap of caps) {
    dot(s, 0.58, dy+0.11);
    s.addText(cap.label, { x:0.75, y:dy, w:4.25, h:0.24, margin:0, fontSize:9.5, color:TEXT, fontFace:"Poppins", bold:true, valign:"middle" });
    s.addText(cap.body, { x:0.75, y:dy+0.26, w:4.25, h:0.26, margin:0, fontSize:8.2, color:MID, fontFace:"Poppins", valign:"top" });
    dy += 0.57;
  }

  // Vektor-branded dark panel — right side
  s.addShape(pres.shapes.RECTANGLE, { x:5.1, y:1.3, w:4.4, h:3.85,
    fill:{ color:VEKTBG }, line:{ color:VEKTBG, width:0 } });
  s.addShape(pres.shapes.RECTANGLE, { x:5.1, y:1.3, w:4.4, h:0.04,
    fill:{ color:GOLD }, line:{ color:GOLD, width:0 } });

  const vlh = 0.4, vlw = +(vlh*VK_RATIO).toFixed(3);
  s.addImage({ path:VEKTOR_L, x:5.28, y:1.5, w:vlw, h:vlh });

  s.addText("METHODOLOGY", { x:5.28, y:2.08, w:4.0, h:0.2, margin:0,
    fontSize:7, color:GOLD, fontFace:"Poppins", bold:true, charSpacing:1.5, valign:"middle" });
  s.addText(
    "The quantitative methodology behind Vektor is documented " +
    "across 11 research papers — WP-00 through WP-10 — covering " +
    "systematic construction, risk management, and portfolio analysis. " +
    "Available on request.",
    { x:5.28, y:2.3, w:4.0, h:0.72, margin:0,
      fontSize:8.8, color:"AAAAAA", fontFace:"Poppins", valign:"top" });

  s.addText("THOUGHT LEADERSHIP", { x:5.28, y:3.14, w:4.0, h:0.2, margin:0,
    fontSize:7, color:GOLD, fontFace:"Poppins", bold:true, charSpacing:1.5, valign:"middle" });
  s.addText(
    "InvestPuppy: Unvarnished — 9 papers, 38 pages on financial software " +
    "implementation failure. Panel-reviewed by 20 independent professionals. " +
    "Already in circulation. Strapline: field notes from decades of bad projects.",
    { x:5.28, y:3.36, w:4.0, h:0.72, margin:0,
      fontSize:8.8, color:"AAAAAA", fontFace:"Poppins", valign:"top" });

  s.addText("VEKTOR BY INVESTPUPPY", { x:5.28, y:4.88, w:4.0, h:0.2, margin:0,
    fontSize:7, color:"444444", fontFace:"Poppins", bold:true, charSpacing:1.5, valign:"middle" });

  footer(s);
}

// ── SLIDE 5 — What Vektor Is Not ──────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color:WHITE };
  secLabel(s, "Positioning");
  title(s, "What Vektor is not.");

  s.addText(
    "Precision about what a product is not is rarer than precision about what it is. " +
    "Both matter to a serious buyer — and a serious investor.",
    { x:0.5, y:1.35, w:9, h:0.38, margin:0,
      fontSize:10, color:MID, fontFace:"Poppins", italic:true, valign:"middle" });

  const nots = [
    { not:"Not a data terminal",
      reality:"Vektor does not compete with Bloomberg or Refinitiv. It uses the data infrastructure the client already has and builds a systematic construction layer on top of it." },
    { not:"Not a replacement project",
      reality:"For most clients, nothing disappears — Vektor sits alongside existing custody, reporting, and CRM in days, not months. Exception: for Bloomberg PORT users, Vektor directly replaces the portfolio construction module. That is a replacement worth making." },
    { not:"Not algorithmic trading",
      reality:"Vektor is systematic portfolio management — construction, analysis, documentation. It is not a prop desk tool, not high-frequency, not speculative. It is what regulated wealth managers need." },
    { not:"Not priced for institutions",
      reality:"The middle market is the market. Boutique DPMs, independent RIAs, and family offices cannot justify enterprise pricing. Vektor is designed from the ground up for the segment every incumbent has ignored." },
  ];

  const positions = [
    { x:0.5, y:1.9 }, { x:5.1, y:1.9 },
    { x:0.5, y:3.62 }, { x:5.1, y:3.62 }
  ];
  const CW = 4.4, CH = 1.58;

  for (let i = 0; i < nots.length; i++) {
    const { x, y } = positions[i];
    s.addShape(pres.shapes.RECTANGLE, { x, y, w:CW, h:CH,
      fill:{ color:CARD }, line:{ color:BORDER, width:0.5 }, shadow:mkShadow() });
    s.addShape(pres.shapes.RECTANGLE, { x:x+0.18, y:y+0.14, w:0.58, h:0.24,
      fill:{ color:DARKBG }, line:{ color:DARKBG, width:0 } });
    s.addText("NOT", { x:x+0.18, y:y+0.14, w:0.58, h:0.24, margin:0,
      fontSize:7.5, color:GREEN, fontFace:"Poppins", bold:true,
      align:"center", valign:"middle", charSpacing:1 });
    s.addText(nots[i].not, { x:x+0.88, y:y+0.12, w:CW-1.06, h:0.28, margin:0,
      fontSize:10, color:TEXT, fontFace:"Poppins", bold:true, valign:"middle" });
    s.addText(nots[i].reality, { x:x+0.18, y:y+0.48, w:CW-0.36, h:1.0, margin:0,
      fontSize:8.8, color:MID, fontFace:"Poppins", valign:"top" });
  }
  footer(s);
}

// ── SLIDE 6 — Market ──────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color:WHITE };
  secLabel(s, "Market Opportunity");
  title(s, "A clear market. A clear entry point.");

  const stages = [
    { when:"Now", mkt:"Singapore",
      body:"2,000+ single family offices (MAS, 2024) — up from 400 in 2020. 500+ independent wealth managers. MAS regulatory clarity. Vektor is distribution-ready for this market today." },
    { when:"12–24 months", mkt:"Southeast Asia",
      body:"Hong Kong, Malaysia, Thailand. Similar regulatory profiles. Existing InvestPuppy professional network extends here." },
    { when:"24–36 months", mkt:"Established markets",
      body:"UK (FCA — regulatory content in development). Australia. Middle East. Platform requires no structural change to enter." },
  ];
  let sy = 1.35;
  for (let i = 0; i < stages.length; i++) {
    const { when, mkt, body } = stages[i];
    dot(s, 0.63, sy+0.2, 0.18);
    if (i < stages.length-1) {
      s.addShape(pres.shapes.LINE, { x:0.63, y:sy+0.3, w:0, h:0.78, line:{ color:BORDER, width:1, dashType:"dash" } });
    }
    s.addText(when, { x:0.9, y:sy, w:3.7, h:0.22, margin:0, fontSize:7.5, color:GREEN, fontFace:"Poppins", bold:true, charSpacing:0.8, valign:"middle" });
    s.addText(mkt, { x:0.9, y:sy+0.2, w:3.7, h:0.32, margin:0, fontSize:13, color:TEXT, fontFace:"Poppins", bold:true, valign:"middle" });
    s.addText(body, { x:0.9, y:sy+0.54, w:3.7, h:0.54, margin:0, fontSize:9, color:MID, fontFace:"Poppins", valign:"top" });
    sy += 1.3;
  }

  const clients = [
    { type:"No PORT — capability provision",
      body:"Bloomberg Terminal without PORT. Add systematic construction for 56% of what one Terminal seat costs. Longer conversion path — value must be demonstrated, not compared." },
    { type:"Bloomberg PORT users — replacement",
      body:"PORT stays for risk reporting. Vektor replaces PORT's equity construction function. Total Bloomberg spend falls. Construction capability improves. Fastest to close." },
    { type:"Data feed clients — development termination",
      body:"Running Bloomberg feeds for in-house quant work. Vektor ends the build. Note: sunk cost psychology requires quantifying continued build cost vs switching." },
  ];
  let cy = 1.33;
  for (const cl of clients) {
    accentCard(s, 5.1, cy, 4.4, 1.08);
    s.addText(cl.type, { x:5.28, y:cy+0.1, w:4.0, h:0.28, margin:0, fontSize:11, color:TEXT, fontFace:"Poppins", bold:true, valign:"middle" });
    s.addText(cl.body, { x:5.28, y:cy+0.4, w:4.0, h:0.58, margin:0, fontSize:9, color:MID, fontFace:"Poppins", valign:"top" });
    cy += 1.22;
  }
  footer(s);
}

// ── SLIDE 7 — Business Model ──────────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color:WHITE };
  secLabel(s, "Business Model");
  title(s, "AUM-tiered annual subscription.");

  // Positioning statement
  s.addText(
    "Pricing is set. The model is AUM-tiered subscription — predictable SaaS revenue that grows " +
    "as clients grow. Indicative pricing below, subject to Founding Mandate validation.",
    { x:0.5, y:1.37, w:9, h:0.42, margin:0,
      fontSize:9.5, color:MID, fontFace:"Poppins", italic:true, valign:"top" });

  // Pricing table — left panel (light)
  const tiers = [
    { tier:"Entry",       aum:"Up to S$75M AUM",     price:"S$24,000/yr",  context:"< 1 Bloomberg seat (S$43K+)" },
    { tier:"Growth",      aum:"S$75M – S$250M AUM",  price:"S$48,000/yr",  context:"32–63% of 2–4 seat Bloomberg bill" },
    { tier:"Institutional",aum:"S$250M – S$750M AUM",price:"S$108,000/yr", context:"40–57% of total Bloomberg spend incl. PORT (S$190K–S$270K typical)" },
    { tier:"Enterprise",  aum:"S$750M+",             price:"S$168,000+/yr",context:"< 30% of typical Bloomberg + PORT infrastructure at scale" },
  ];

  const thdr = ["Tier", "AUM", "Annual price", "Bloomberg context"];
  const tcw  = [1.2, 2.1, 1.4, 2.5];
  const tstart = 0.5;

  // Header row
  let tx = tstart;
  thdr.forEach((h, i) => {
    s.addShape(pres.shapes.RECTANGLE, { x:tx, y:1.9, w:tcw[i], h:0.26,
      fill:{ color:DARKBG }, line:{ color:DARKBG, width:0 } });
    s.addText(h, { x:tx+0.05, y:1.9, w:tcw[i]-0.1, h:0.26, margin:0,
      fontSize:7.5, color:WHITE, fontFace:"Poppins", bold:true, valign:"middle" });
    tx += tcw[i] + 0.04;
  });

  // Data rows
  tiers.forEach((t, ri) => {
    const rowY = 2.2 + ri * 0.46;
    const bg = ri % 2 === 0 ? CARD : "FAFAFA";
    tx = tstart;
    [t.tier, t.aum, t.price, t.context].forEach((val, ci) => {
      s.addShape(pres.shapes.RECTANGLE, { x:tx, y:rowY, w:tcw[ci], h:0.42,
        fill:{ color:bg }, line:{ color:BORDER, width:0.3 } });
      s.addText(val, { x:tx+0.08, y:rowY, w:tcw[ci]-0.16, h:0.42, margin:0,
        fontSize: ci === 2 ? 9.5 : 8.2,
        color: ci === 2 ? GREEN : (ci === 0 ? TEXT : MID),
        fontFace:"Poppins", bold: ci === 0 || ci === 2,
        valign:"middle" });
      tx += tcw[ci] + 0.04;
    });
  });

  // Founding Mandate band
  s.addShape(pres.shapes.RECTANGLE, { x:0.5, y:4.1, w:7.25, h:0.52,
    fill:{ color:"EEF7E6" }, line:{ color:GREEN, width:0.5 } });
  s.addText(
    "Founding Mandate pricing: S$18,000/year for the first 12 months — 25% below the entry tier. " +
    "From year two: permanently 1 tier below their AUM tier (floor: Entry at S$24,000). " +
    "The permanent benefit scales with client growth — and generates NRR.",
    { x:0.66, y:4.1, w:6.95, h:0.52, margin:0,
      fontSize:8.5, color:TEXT, fontFace:"Poppins", valign:"middle" });

  // Three entry motions — right dark panel
  s.addShape(pres.shapes.RECTANGLE, { x:7.88, y:1.88, w:1.7, h:2.8,
    fill:{ color:DARKBG }, line:{ color:DARKBG, width:0 } });
  s.addText("THREE\nENTRY\nMOTIONS", { x:7.96, y:2.0, w:1.54, h:0.7, margin:0,
    fontSize:8, color:GOLD, fontFace:"Poppins", bold:true,
    align:"center", valign:"middle", charSpacing:0.5 });

  const motions = [
    { label:"Capability", body:"No PORT. Terminal only. 56% of Terminal cost." },
    { label:"Replacement", body:"PORT users. Construction replaced. Risk stays." },
    { label:"Termination", body:"Data feed clients. Ends in-house build." },
  ];
  let my = 2.78;
  for (const m of motions) {
    s.addText(m.label, { x:7.96, y:my, w:1.54, h:0.2, margin:0,
      fontSize:7.5, color:GREEN, fontFace:"Poppins", bold:true, align:"center", valign:"middle" });
    s.addText(m.body, { x:7.96, y:my+0.2, w:1.54, h:0.3, margin:0,
      fontSize:7, color:"AAAAAA", fontFace:"Poppins", align:"center", valign:"top" });
    my += 0.62;
  }

  footer(s);
}

// ── SLIDE 8 — Traction (brand voice rewrite) ──────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color:WHITE };
  secLabel(s, "Traction");
  title(s, "Where we are. Honestly.");

  const items = [
    { head:"The platform is built",
      body:"Vektor runs in IBKR simulation mode. Full portfolio construction capability is live. " +
           "It has not yet executed in a live account. That is what the seed round is for. " +
           "The engineering gap is defined and costed." },
    { head:"The commercial machine is ready",
      body:"25 client-facing documents. 5 presentation decks. A fully specified Founding Mandate Programme. " +
           "A DD Navigation Guide. An NDA. A First 90 Days onboarding plan. " +
           "Ready to deploy. Waiting for the first conversation to become a signed mandate." },
    { head:"The thought leadership is in circulation",
      body:"InvestPuppy: Unvarnished — 9 papers, 38 pages on financial software implementation failure. " +
           "Panel-reviewed by 20 independent professionals. " +
           "Already reaching the professionals who will buy Vektor." },
    { head:"The methodology is documented",
      body:"11 research papers (WP-00 – WP-10) document the quantitative approach behind Vektor. " +
           "Available on request. This is not a black box. We can show our working." },
  ];

  const positions = [{ x:0.5, y:1.35 }, { x:5.1, y:1.35 }, { x:0.5, y:3.2 }, { x:5.1, y:3.2 }];
  for (let i = 0; i < items.length; i++) {
    const { x, y } = positions[i];
    accentCard(s, x, y, 4.4, 1.72);
    s.addText(items[i].head, { x:x+0.2, y:y+0.12, w:4.05, h:0.3, margin:0, fontSize:10.5, color:TEXT, fontFace:"Poppins", bold:true, valign:"middle" });
    s.addText(items[i].body, { x:x+0.2, y:y+0.47, w:4.05, h:1.16, margin:0, fontSize:8.8, color:MID, fontFace:"Poppins", valign:"top" });
  }
  footer(s);
}

// ── SLIDE 9 — Team ────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color:WHITE };
  secLabel(s, "The Team");
  title(s, "Two founders. One focus.");

  s.addText(
    "Senior leadership in fintech and financial software. Direct experience in this market. " +
    "The problem Vektor solves is one we have encountered firsthand.",
    { x:0.5, y:1.32, w:9, h:0.28, margin:0, fontSize:10.5, color:MID, fontFace:"Poppins", valign:"middle" });

  const founders = [
    { role:"CEO", name:"[FOUNDER A — NAME]",
      bio:"Senior leadership background in fintech and financial software. Extensive B2B sales experience selling into wealth managers, independent RIAs, and institutional clients. Deep familiarity with the operational context Vektor is built for.",
      skills:["Commercial leadership", "Client relationships", "Market strategy"] },
    { role:"CTO", name:"[FOUNDER B — NAME]",
      bio:"[Biography to be completed. Fintech / financial software background. Experience directly relevant to platform architecture and quantitative systems development underpinning Vektor.]",
      skills:["Platform architecture", "Quantitative systems", "Engineering leadership"] },
  ];

  for (let i = 0; i < founders.length; i++) {
    const f = founders[i]; const x = [0.5, 5.1][i];
    card(s, x, 1.72, 4.4, 3.35);
    s.addShape(pres.shapes.RECTANGLE, { x:x+0.22, y:1.9, w:0.7, h:0.28,
      fill:{ color:GREEN }, line:{ color:GREEN, width:0 } });
    s.addText(f.role, { x:x+0.22, y:1.9, w:0.7, h:0.28, margin:0,
      fontSize:9, color:"0A0A0A", fontFace:"Poppins", bold:true, align:"center", valign:"middle" });
    s.addText(f.name, { x:x+1.05, y:1.89, w:3.12, h:0.3, margin:0,
      fontSize:11, color:TEXT, fontFace:"Poppins", bold:true, valign:"middle" });
    s.addText(f.bio, { x:x+0.22, y:2.32, w:3.96, h:1.35, margin:0,
      fontSize:9.5, color:MID, fontFace:"Poppins", valign:"top", italic:true });
    let ky = 3.76;
    for (const sk of f.skills) {
      dot(s, x+0.31, ky+0.1);
      s.addText(sk, { x:x+0.46, y:ky, w:3.74, h:0.22, margin:0,
        fontSize:8.5, color:TEXT, fontFace:"Poppins", valign:"middle" });
      ky += 0.26;
    }
  }
  footer(s);
}

// ── SLIDE 10 — Use of Funds + Milestone Timeline ──────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color:WHITE };
  secLabel(s, "Use of Funds");
  title(s, "S$1M–S$2M — where it goes and what it delivers.");

  const buckets = [
    { pct:"~45%", head:"Engineering & product",
      body:"Live-account validation and deployment. Platform hardening, security, performance. Capability build-out for launch." },
    { pct:"~30%", head:"Sales & BD headcount",
      body:"First commercial hires to execute the Founding Mandate Programme and build the Singapore client base." },
    { pct:"~25%", head:"Operational runway",
      body:"18–24 months of operational coverage. MAS regulatory engagement. FCA content pipeline. Legal and compliance." },
  ];
  const bx = [0.5, 3.55, 6.6];
  for (let i = 0; i < buckets.length; i++) {
    const b = buckets[i]; const x = bx[i];
    card(s, x, 1.3, 2.85, 2.35);
    s.addText(b.pct, { x:x+0.18, y:1.42, w:2.49, h:0.58, margin:0,
      fontSize:40, color:GREEN, fontFace:"Poppins", bold:true, valign:"middle" });
    s.addText(b.head, { x:x+0.18, y:2.04, w:2.49, h:0.3, margin:0,
      fontSize:10, color:TEXT, fontFace:"Poppins", bold:true, valign:"middle" });
    s.addText(b.body, { x:x+0.18, y:2.38, w:2.49, h:1.15, margin:0,
      fontSize:8.8, color:MID, fontFace:"Poppins", valign:"top" });
  }

  s.addText("MILESTONE TIMELINE — CLOSE TO FIRST REVENUE", { x:0.5, y:3.78, w:6, h:0.2, margin:0,
    fontSize:7, color:GREEN, fontFace:"Poppins", bold:true, charSpacing:1.5, valign:"middle" });

  const milestones = [
    { label:"M1–3", text:"Commercial hire. Engineering sprint. Founding Mandate conversations open." },
    { label:"M4–6", text:"Platform live-account validated. First Founding Mandate demos." },
    { label:"M7–9", text:"First client signed. WP-07 complete — UK distribution unlocked." },
    { label:"M9–13", text:"First revenue. Second and third clients. Series A preparation." },
  ];
  const msx = [0.5, 2.9, 5.3, 7.7];
  for (let i = 0; i < milestones.length; i++) {
    const x = msx[i];
    s.addShape(pres.shapes.RECTANGLE, { x, y:4.05, w:2.2, h:1.1,
      fill:{ color:DARKBG }, line:{ color:DARKBG, width:0 } });
    s.addShape(pres.shapes.RECTANGLE, { x, y:4.05, w:2.2, h:0.04,
      fill:{ color:GREEN }, line:{ color:GREEN, width:0 } });
    s.addText(milestones[i].label, { x:x+0.1, y:4.1, w:2.0, h:0.22, margin:0,
      fontSize:8.5, color:GREEN, fontFace:"Poppins", bold:true, valign:"middle" });
    s.addText(milestones[i].text, { x:x+0.1, y:4.34, w:2.0, h:0.76, margin:0,
      fontSize:7.8, color:"AAAAAA", fontFace:"Poppins", valign:"top" });
  }
  footer(s);
}

// ── SLIDE 11 — The Ask (brand voice) ─────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color:WHITE };
  secLabel(s, "The Ask");
  title(s, "The ask is S$1–2M. Here is exactly what it funds.");

  s.addText([
    { text:"S$1,000,000 – S$2,000,000", options:{ bold:true, breakLine:true } },
    { text:"Seed round  ·  Singapore-led close", options:{ color:MID } }
  ], { x:0.5, y:1.38, w:4.4, h:0.88, margin:0, fontSize:17, color:TEXT, fontFace:"Poppins", valign:"middle" });

  s.addText(
    "We have not fixed the valuation because we believe the right investor " +
    "conversation determines the right number. We have a range in mind. " +
    "If you are the right investor, we will share it.",
    { x:0.5, y:2.38, w:4.4, h:0.62, margin:0,
      fontSize:9.5, color:MID, fontFace:"Poppins", italic:true, valign:"top" });

  s.addText("What we want in an investor partner:", { x:0.5, y:3.1, w:4.4, h:0.28, margin:0,
    fontSize:10, color:TEXT, fontFace:"Poppins", bold:true, valign:"middle" });
  const wants = [
    "Domain experience in fintech, wealth management, or financial infrastructure",
    "Network into Singapore's family office and independent RIA community",
    "Patient capital — this is a relationship-driven B2B market",
    "Alignment with the principle of building honestly",
  ];
  let wy = 3.48;
  for (const w of wants) {
    dot(s, 0.58, wy+0.12);
    s.addText(w, { x:0.75, y:wy, w:4.1, h:0.3, margin:0,
      fontSize:9.5, color:MID, fontFace:"Poppins", valign:"middle" });
    wy += 0.36;
  }

  s.addShape(pres.shapes.RECTANGLE, { x:5.1, y:1.33, w:4.4, h:3.78,
    fill:{ color:DARKBG }, line:{ color:DARKBG, width:0 }, shadow:mkShadow() });
  s.addText("What you get", { x:5.3, y:1.5, w:4.0, h:0.28, margin:0,
    fontSize:10, color:GREEN, fontFace:"Poppins", bold:true, valign:"middle" });

  const gets = [
    { head:"Equity stake", body:"Seed-round equity in InvestPuppy. Instrument and cap table discussed with interested investors — not before." },
    { head:"Founding Mandate access", body:"12-month founding rate at S$18,000/year, then permanently 1 tier below their AUM tier. Investors with client relationships can facilitate introductions." },
    { head:"Transparent reporting", body:"Quarterly updates. Honest assessment of progress and setbacks. Not a promise we make lightly. Consistent with our governing principle." },
    { head:"First-mover position", body:"Entry before the category is competed. Singapore architecture ready now. Global architecture already in place." },
  ];
  let gy = 1.9;
  for (const g of gets) {
    s.addText(g.head, { x:5.3, y:gy, w:4.0, h:0.26, margin:0,
      fontSize:9.5, color:WHITE, fontFace:"Poppins", bold:true, valign:"middle" });
    s.addText(g.body, { x:5.3, y:gy+0.28, w:4.0, h:0.46, margin:0,
      fontSize:8.5, color:"999999", fontFace:"Poppins", valign:"top" });
    gy += 0.84;
  }
  footer(s);
}

// ── SLIDE 12 — Closing ────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color:DARKBG };
  bigCircle(s, 9.6, 0.9, 2.0, 0.1);
  bigCircle(s, 0.2, 5.4, 1.0, 0.1);

  const lh = 0.65, lw = +(lh*IP_RATIO).toFixed(3);
  s.addImage({ path:LOGO_D, x:0.5, y:0.36, w:lw, h:lh });

  s.addText("Honest by design.", { x:0.5, y:1.62, w:9, h:1.0, margin:0,
    fontSize:50, color:WHITE, fontFace:"Poppins", bold:true, valign:"middle" });
  s.addText([
    { text:"Serious", options:{ color:GREEN, bold:true } },
    { text:" when it matters.", options:{ color:"888888" } }
  ], { x:0.5, y:2.65, w:9, h:0.55, margin:0, fontSize:24, fontFace:"Poppins", valign:"middle" });

  s.addText(
    "We are building a platform that wealth managers can trust — in the rigour of its " +
    "construction, the clarity of its output, and the honesty of the team behind it. " +
    "We apply the same standard to this investor pack.",
    { x:0.5, y:3.35, w:7, h:0.92, margin:0,
      fontSize:11, color:"666666", fontFace:"Poppins", valign:"top" });

  s.addText([
    { text:"contact@investpuppy.com", options:{ breakLine:true } },
    { text:"investpuppy.com", options:{ color:"555555" } }
  ], { x:0.5, y:4.44, w:4, h:0.65, margin:0,
    fontSize:11, color:GREEN, fontFace:"Poppins", valign:"middle" });

  s.addText("CONFIDENTIAL · NOT AN OFFER OF SECURITIES", {
    x:6.2, y:5.1, w:3.5, h:0.24, margin:0, fontSize:6.5, color:"3A3A3A",
    fontFace:"Poppins", bold:true, align:"right", valign:"middle", charSpacing:0.8 });
}

// ── Write ─────────────────────────────────────────────────────────────────────
pres.writeFile({ fileName:OUT })
  .then(() => console.log(`Built: ${OUT}`))
  .catch(err => { console.error(err); process.exit(1); });
