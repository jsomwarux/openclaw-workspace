// Google Apps Script — Run at script.google.com
// Creates Nash Satoshi draft docs in Eve — Drafts > Nash Satoshi subfolders
// Usage: select createNashSatoshiDrafts, click Run

function createNashSatoshiDrafts() {
  const root = DriveApp.getFoldersByName("Eve — Drafts").next();
  const ns = root.getFoldersByName("Nash Satoshi").next();
  const xF = ns.getFoldersByName("X Threads").next();
  const phF = ns.getFoldersByName("Product Hunt").next();

  function makeDoc(name, folder, content) {
    const doc = DocumentApp.create(name);
    doc.getBody().setText(content);
    DriveApp.getFileById(doc.getId()).moveTo(folder);
    Logger.log(name + ": " + doc.getUrl());
  }

  makeDoc("Nash Satoshi — X Thread (Methodology Teaser)", xF,
    "AUDIENCE: @jt__crypto (crypto) + @jts_14 (builder/AI)\n" +
    "ANGLE: What makes Nash Satoshi different — 4-LLM consensus + game theory\n" +
    "POST WHEN: Any time, strongest Tue–Thu 9–11 AM EST\n\n" +
    "— TWEET 1 (hook) —\n" +
    "Most crypto rankings are vibes.\n\n" +
    "Nash Satoshi uses a 4-model AI ensemble + game theory to rank tokens by optimal strategy — not hype.\n\n" +
    "Here's how it works. 🧵\n\n" +
    "— TWEET 2 —\n" +
    "The problem with most rankings:\n\n" +
    "One model, one perspective, one set of biases.\n\n" +
    "GPT says buy. Claude says hold. Gemini says sell.\n\n" +
    "Who do you trust?\n\n" +
    "— TWEET 3 —\n" +
    "Nash Satoshi's answer: make them agree.\n\n" +
    "4 models analyze every token independently:\n" +
    "→ GPT-5.2\n" +
    "→ Claude Opus 4.5\n" +
    "→ Gemini 3 Pro\n" +
    "→ Grok 4\n\n" +
    "They cross-check each other. Consensus becomes the signal.\n\n" +
    "— TWEET 4 —\n" +
    "The game theory layer is what makes it different.\n\n" +
    "It's not 'what's the best token.' It's 'what's the optimal strategy given what everyone else is doing.'\n\n" +
    "Nash equilibrium applied to crypto markets.\n\n" +
    "— TWEET 5 —\n" +
    "Output: a ranked leaderboard + individual token scorecards.\n\n" +
    "Each scorecard shows:\n" +
    "→ Consensus recommendation across all 4 models\n" +
    "→ Where the models disagreed (and why)\n" +
    "→ Game-theory optimal position\n\n" +
    "— TWEET 6 (CTA) —\n" +
    "Still in development. Following along? 👀\n\n" +
    "Drop a reply — curious what tokens you'd want ranked first."
  );

  makeDoc("Nash Satoshi — X Thread (Build Story)", xF,
    "AUDIENCE: @jts_14 (builder audience)\n" +
    "ANGLE: Why I built this / the idea origin\n" +
    "POST WHEN: After launching, or when Nash Satoshi has a landing page\n\n" +
    "— TWEET 1 (hook) —\n" +
    "I got tired of asking one AI what to think about a crypto token.\n\n" +
    "So I made four of them argue about it instead.\n\n" +
    "That became Nash Satoshi. 🧵\n\n" +
    "— TWEET 2 —\n" +
    "The original frustration:\n\n" +
    "Every AI analysis tool uses a single model. One set of biases. One worldview.\n\n" +
    "Crypto is adversarial by design. You need adversarial analysis to match.\n\n" +
    "— TWEET 3 —\n" +
    "The insight from game theory:\n\n" +
    "John Nash showed that in competitive systems, the optimal strategy depends on what everyone else is doing.\n\n" +
    "Applied to token analysis: the right call isn't just 'is this fundamentally good.'\n" +
    "It's 'what's the rational position given how other actors are positioned.'\n\n" +
    "— TWEET 4 —\n" +
    "So I built an ensemble:\n\n" +
    "4 frontier models, each analyzing a token independently.\n" +
    "They cross-check. They surface disagreements. Consensus becomes the signal.\n\n" +
    "It's not averaging opinions. It's structured debate with a verdict.\n\n" +
    "— TWEET 5 (CTA) —\n" +
    "Nash Satoshi launches soon — ranked leaderboard + token scorecards.\n\n" +
    "What tokens would you want to see ranked first? 👇"
  );

  makeDoc("Nash Satoshi — Product Hunt Listing", phF,
    "SUBMIT: Day of launch or night before (midnight PT = top of day)\n\n" +
    "NAME: Nash Satoshi\n\n" +
    "TAGLINE: Crypto rankings by 4-AI consensus + game theory — not hype\n\n" +
    "SHORT DESCRIPTION:\n" +
    "Nash Satoshi uses a 4-model AI ensemble (GPT-5.2, Claude Opus 4.5, Gemini 3 Pro, Grok 4) to analyze crypto tokens through a game theory lens. Each model analyzes independently, they cross-check each other, and consensus becomes the ranking signal. Less vibes, more signal.\n\n" +
    "LONG DESCRIPTION:\n" +
    "Most crypto ranking tools use a single model, a single data source, or a single analyst's biases. Nash Satoshi is different by design.\n\n" +
    "The 4-LLM ensemble: Four frontier AI models — GPT-5.2, Claude Opus 4.5, Gemini 3 Pro, and Grok 4 — analyze each token independently. They don't share answers. They don't average their outputs. They cross-check each other's reasoning and surface where they agree and where they diverge. Consensus = signal. Disagreement = risk flag.\n\n" +
    "The game theory layer: Named after John Nash, Nash Satoshi applies Nash equilibrium thinking to token analysis. The question isn't just 'is this token fundamentally strong.' It's 'what is the optimal position given how other rational actors are likely to move.' That's a different — and more honest — question.\n\n" +
    "What you get:\n" +
    "- A ranked leaderboard updated by consensus\n" +
    "- Individual token scorecards showing each model's verdict, where they disagreed, and the game-theory optimal position\n" +
    "- Transparent reasoning — not black-box scores\n\n" +
    "TOPICS: Crypto, AI, Finance, Investing, Web3\n\n" +
    "MAKER COMMENT (post as first comment after launch):\n" +
    "Hey PH! Built Nash Satoshi because I was frustrated with single-model crypto analysis tools. One AI, one perspective, one set of biases.\n\n" +
    "The 4-model cross-check was the breakthrough: when all four models agree, that's a real signal. When they disagree, that's a risk flag — and most tools hide that information.\n\n" +
    "The game theory layer is what I'm most excited to hear feedback on. Crypto markets are adversarial environments. Nash equilibrium thinking feels like the right framework. Curious if others see it the same way.\n\n" +
    "What tokens would you want to see on the leaderboard?"
  );

  Logger.log("All 3 Nash Satoshi docs created.");
}
