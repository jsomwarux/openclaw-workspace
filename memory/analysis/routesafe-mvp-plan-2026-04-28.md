# RouteSafe MVP Plan — 2026-04-28

## Verdict
**Hold on full build; create a no-code validation page first.** The idea is strong, but a real route planner needs map/routing APIs, safety data, geocoding, mobile UX, and liability-sensitive language. Building the full MVP overnight would be sloppy. The better move is a landing page + manually generated route scorecards for one city.

## Product Hypothesis
Runners do not only want shortest-distance routes. They want routes that feel safe, well-lit, hard to get lost on, and practical: bathrooms, water, elevation, road crossings, and neighborhood comfort matter.

## Narrow MVP
**City:** NYC, starting with Brooklyn/Manhattan waterfront + park loops.  
**User input:** start area, target distance, vibe: safe/easy/scenic/hill/late-night.  
**Output:** 3 route cards with:
- distance estimate
- safety/friction score
- lighting confidence
- bathroom/water notes
- elevation difficulty
- turn complexity
- “why this route” explanation
- CTA: join waitlist / request custom route

## Data Sources to Use Later
- Routing: Mapbox Directions, Google Routes, or OpenRouteService
- Places: OpenStreetMap Overpass for toilets/water/parks/paths
- Safety/friction proxy: road class, park path availability, lighting tags where present, crossing density, crime-data only if used carefully with caveats
- Elevation: Mapbox Terrain or Open-Elevation
- LLM layer: convert structured signals into plain-English route scorecards

## Build Sequence
1. Landing page with waitlist and 3 static example routes.
2. Manual route generation for first 10 users to validate demand.
3. Add geocoding + route candidate generation.
4. Add scoring pipeline.
5. Add SEO pages: `/running-routes/[city]`, `/safe-running-routes/[neighborhood]`, `/best-running-routes/[distance]-miles-[city]`.

## Positioning
**Not:** “AI running route planner.”  
**Better:** “Running routes that account for the stuff maps ignore: lighting, turns, bathrooms, water, elevation, and how sketchy it feels at 6AM.”

## Recommendation
Create a Mission Control follow-up task for a landing-page validation build, not a full map app. Done criteria: one-page site, 3 NYC example routes, waitlist capture, and one SEO template. If 20+ waitlist signups or 5 paid custom-route requests happen, then build dynamic routing.
