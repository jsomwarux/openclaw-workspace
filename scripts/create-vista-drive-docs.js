// Google Apps Script — Run this at script.google.com
// Creates Vista draft docs in the Eve — Drafts > Vista subfolders

function createVistaDrafts() {
  const root = DriveApp.getFoldersByName("Eve — Drafts").next();
  const vista = root.getFoldersByName("Vista").next();
  const xF = vista.getFoldersByName("X Threads").next();
  const redF = vista.getFoldersByName("Reddit").next();
  const phF = vista.getFoldersByName("Product Hunt").next();
  const lcF = vista.getFoldersByName("Launch Copy").next();

  function makeDoc(name, folder, content) {
    const doc = DocumentApp.create(name);
    doc.getBody().setText(content);
    DriveApp.getFileById(doc.getId()).moveTo(folder);
    Logger.log(name + ": " + doc.getUrl());
  }

  makeDoc("Vista — X Thread (Launch)", xF,
    "POST WHEN: Day App Store clears (or 24h before if you get a heads up)\n" +
    "BEST TIME: Tue–Thu, 9–11 AM or 7–9 PM EST\n\n" +
    "— TWEET 1 (hook) —\n" +
    "I built the movie app I wanted because Letterboxd frustrates me.\n\n" +
    "Just submitted Vista to the App Store. Here's what it does differently. 🧵\n\n" +
    "— TWEET 2 —\n" +
    "Letterboxd is great for logging. It's not great for showing you who you are as a film person.\n\n" +
    "Vista builds a taste profile around you:\n\n" +
    "→ Your all-time highest rated film\n" +
    "→ Your highest rated film in the last 30 days\n" +
    "→ Your favorite performer (calculated, not picked)\n\n" +
    "— TWEET 3 —\n" +
    "The 'favorite performer' thing is my favorite feature.\n\n" +
    "Vista looks at every movie you've rated highly and finds the performer who shows up most often in your top films.\n\n" +
    "You don't pick them. The data picks them for you.\n\n" +
    "Sometimes the answer surprises you.\n\n" +
    "— TWEET 4 —\n" +
    "The UI is clean. No clutter. No noise.\n\n" +
    "I wanted something that felt like a personal film record, not a social media feed with movie logging bolted on.\n\n" +
    "— TWEET 5 (CTA) —\n" +
    "Currently in App Store review.\n\n" +
    "Drop a reply or follow @jts_14 — I'll post when it's live.\n\n" +
    "If you're a Letterboxd user who's wanted something cleaner, this is for you."
  );

  makeDoc("Vista — Launch Day Post", lcF,
    "POST THE DAY IT GOES LIVE\n\n" +
    "Vista is live on the App Store.\n\n" +
    "Movie ratings + taste profiles. Shows you your all-time faves, what you're into right now, " +
    "and your favorite performer (calculated from your ratings — not picked).\n\n" +
    "Built it because I wanted it. Here it is.\n\n" +
    "[App Store link]"
  );

  makeDoc("Vista — Reddit r/Letterboxd", redF,
    "POST WHEN: After launch only (communities are skeptical of 'coming soon' posts)\n\n" +
    "TITLE: I built a movie rating app focused on taste profiles — Vista (iOS)\n\n" +
    "BODY:\n" +
    "Long-time Letterboxd user here. Love what it does, but I wanted something that felt more personal and less social-feed.\n\n" +
    "Built Vista — it focuses on taste profiles:\n" +
    "- All-time highest rated film\n" +
    "- Last 30 days highest rated (your recent phase)\n" +
    "- Favorite performer (calculated from your ratings — who shows up most in your top films?)\n\n" +
    "The UI is clean and minimal. No activity feed, no followers pressure, just your film record.\n\n" +
    "Just went live on the App Store: [link]\n\n" +
    "Would love to hear what you think, especially from people who've been using Letterboxd for years. What's missing from your current setup?"
  );

  makeDoc("Vista — Reddit r/iOSProgramming", redF,
    "POST WHEN: After launch\n\n" +
    "TITLE: Shipped my first solo iOS app — Vista, a movie rating app. Here's what I learned.\n\n" +
    "BODY:\n" +
    "After about [X weeks] of building, Vista just went live on the App Store.\n\n" +
    "It's a movie rating app that builds a taste profile for you: all-time favorites, recent favorites (last 30 days), " +
    "and your favorite performer (calculated from which performers show up most in your high-rated films).\n\n" +
    "What I built it with: [FILL IN — Swift/SwiftUI? React Native?]\n\n" +
    "Biggest lessons:\n" +
    "- The App Store review process is [FILL IN]\n" +
    "- The hardest part technically was [FILL IN]\n" +
    "- Most proud of: the performer calculation logic — deceptively simple, produces surprisingly accurate results\n\n" +
    "App Store link: [link]\n\n" +
    "Happy to answer questions for anyone building their first solo app."
  );

  makeDoc("Vista — Product Hunt Listing", phF,
    "SUBMIT: Night before launch (midnight PT = top of the day's list)\n\n" +
    "NAME: Vista\n\n" +
    "TAGLINE: Movie ratings that build your taste profile\n\n" +
    "SHORT DESCRIPTION:\n" +
    "Vista is a cleaner alternative to Letterboxd. Rate movies, and Vista builds a taste profile: " +
    "your all-time highest rated film, what you're into right now (last 30 days), and your favorite performer — " +
    "calculated from the data, not hand-picked.\n\n" +
    "LONG DESCRIPTION:\n" +
    "Most movie apps are about tracking what you've watched. Vista is about understanding who you are as a film person.\n\n" +
    "All-time highest rated — your definitive, current #1 film based on your actual ratings.\n\n" +
    "Recent highest rated (last 30 days) — your current phase. Your taste shifts. Vista shows what you're into now.\n\n" +
    "Favorite performer — Vista analyzes every highly-rated film and identifies which performer appears most often " +
    "in your top films. You don't pick them — your ratings do.\n\n" +
    "Built for people who love film and want a cleaner, more personal record than the social-feed alternatives.\n\n" +
    "TOPICS: iOS, Entertainment, Productivity, Lifestyle\n\n" +
    "MAKER COMMENT (post as your first comment after launch):\n" +
    "Hey PH! I built Vista because I've been a film obsessive for years and wanted a record that felt personal, " +
    "not like a social media feed. The performer calculation is my favorite part — it often surprises you. " +
    "Would love to hear from other film people: what's missing from your current movie app?"
  );

  Logger.log("Done! 5 Vista docs created across Vista subfolders.");
}
