/* ============================================================
   InvestPuppy — Price Configuration
   prices.js · v2.1 · May 2026

   THIS IS THE SINGLE SOURCE OF TRUTH FOR ALL PRICING.

   To update a price: edit the relevant value below.
   To add a currency: add it to every price key and to
   IP_AUM_TIERS, IP_AUM_SAMPLE, and IP_CURRENCIES in currency.js.

   USD prices are the published, binding subscription rates.
   All other currencies are illustrative for comparison only.
   All subscriptions are quoted and billed in USD.

   Last updated: May 18 2026
   Changes v2.1: Institutional raised to 105,000 USD.
                 Enterprise raised to 175,000 USD.
                 Proof Partner config added (IP_PP_CONFIG).
                 Enterprise supplement added.
   ============================================================ */

const IP_PRICES = {

  /* Annual subscription rates -------------------------------- */
  'entry': {
    USD: 18000,  SGD: 24000,  GBP: 14000,
    EUR: 16500,  CHF: 16000,  AUD: 28000,  HKD: 140000,
  },
  'growth': {
    USD: 36000,  SGD: 48000,  GBP: 28500,
    EUR: 33000,  CHF: 32500,  AUD: 56000,  HKD: 280000,
  },
  'institutional': {
    USD: 105000, SGD: 141000, GBP: 83000,
    EUR: 96500,  CHF: 94500,  AUD: 163000, HKD: 820000,
  },
  'enterprise': {
    USD: 175000, SGD: 235000, GBP: 138500,
    EUR: 161000, CHF: 157500, AUD: 272000, HKD: 1365000,
  },

  /* Reference prices (used in comparatives) ------------------ */
  'bloomberg-seat': {
    USD: 32000,  SGD: 43000,  GBP: 25000,
    EUR: 29500,  CHF: 29000,  AUD: 49500,  HKD: 249000,
  },
};

/* Proof Partner configuration --------------------------------
   Single source of truth for all PP commercial terms.
   ------------------------------------------------------------ */
const IP_PP_CONFIG = {

  /* Tier A: AUM below this threshold (million USD) at signing  */
  tierAThresholdUSD: 55,

  /* Tier A flat rates — Year 1 and ongoing                     */
  tierA: {
    USD: 13500,  SGD: 18000,  GBP: 10500,
    EUR: 12500,  CHF: 12000,  AUD: 21000,  HKD: 105000,
  },

  /* Tier B discounts — applied to natural tier standard rate   */
  tierBYear1Discount:    0.35,  /* 35% off standard Year 1      */
  tierBOngoingDiscount:  0.20,  /* 20% off standard ongoing     */

  /* Available slots — update as slots fill                     */
  slotsTotal: 3,
  slotsTaken: 0,

  /* AUM definition footnote text                               */
  aumDefinition: 'AUM means the aggregate value of assets in mandates actively managed using the Vektor platform at the measurement date.',
};

/* Enterprise AUM supplement ----------------------------------
   Applies above the standard Enterprise AUM threshold.
   Supplement thresholds are in USD millions.
   ------------------------------------------------------------ */
const IP_ENTERPRISE_SUPPLEMENT = {
  base:  { thresholdM: 550,  USD: 175000 },
  mid:   { thresholdM: 750,  USD: 200000 },
  top:   { thresholdM: 1000, USD: 225000 },
  above: { note: 'Above USD 1B — contact us' },
};

/* AUM tier thresholds (millions) — clean round numbers -------- */
const IP_AUM_TIERS = {
  USD: { t1: 55,   t2: 185,  t3: 550  },
  SGD: { t1: 75,   t2: 250,  t3: 750  },
  GBP: { t1: 43,   t2: 145,  t3: 435  },
  EUR: { t1: 50,   t2: 170,  t3: 505  },
  CHF: { t1: 50,   t2: 165,  t3: 500  },
  AUD: { t1: 85,   t2: 285,  t3: 855  },
  HKD: { t1: 425,  t2: 1450, t3: 4300 },
};

/* AUM form placeholder text ----------------------------------- */
const IP_AUM_SAMPLE = {
  USD: 'e.g. USD\u00a01.5B across 12 mandates',
  SGD: 'e.g. SGD\u00a02B across 12 mandates',
  GBP: 'e.g. GBP\u00a01.2B across 12 mandates',
  EUR: 'e.g. EUR\u00a01.4B across 12 mandates',
  CHF: 'e.g. CHF\u00a01.4B across 12 mandates',
  AUD: 'e.g. AUD\u00a02.3B across 12 mandates',
  HKD: 'e.g. HKD\u00a012B across 12 mandates',
};
