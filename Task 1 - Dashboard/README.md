# Year 11 p5.js Aquarium Dashboard Project

Your task is to design and code an interactive visual dashboard in p5.js that reads live data from our school's fish environment monitoring system.

## Setup Instructions
1. Open `sketch.js`.
2. Ensure `PROXY_URL` points to the Cloudflare Worker URL provided to you.
3. Open `index.html` using **Live Server** (or your browser) to preview your sketch.

## Project Requirements
- [ ] Display real-time values for **Temperature**, **pH**, and **Ammonia (NH3)**.
- [ ] Use visual indicators (colors, gauges, shapes, or graphs) to show if water parameters are in a safe range.
- [ ] Add an alert graphic (e.g., changing color to red) if parameters exceed safe limits.
- [ ] Include clear text labeling and a "Last Updated" timestamp.

## Tips
- To work offline, set `USE_OFFLINE_MOCK = true` in `sketch.js`.
- Do NOT place `loadJSON()` inside the `draw()` loop without a timer, as this will overload the server!