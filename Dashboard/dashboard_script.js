const API_ENDPOINT = "https://seneye-proxy.ezankov.workers.dev/";

let aquariumData = null;
let lastUpdated = "";

// format these as the correct arrays later
const temperatureRanges = [15, 20, 22, 26, 28, 35]
const phRanges = [6, 6.5, 6.8, 7.8, 8.2, 9]


function loadData() {
    data = loadJSON(API_ENDPOINT, onDataLoaded, onError);
    return data;
}


function onDataLoaded(data) {
    aquariumData = data;
    lastUpdated = new Date().toLocaleTimeString();
    console.log(lastUpdated, "Data refreshed successfully");
}


function onError(err) {
    console.log('Failed to load aquarium data. Check network and URL.', err);
}


function preload() {
    aquariumData = loadData()
}


function setup() {
    createCanvas(windowWidth, windowHeight);
    setInterval(loadData, 300000);
}


function draw() {
    background("lightblue");

    fill("black");
    textSize(36);
    textAlign(CENTER, TOP);
    text("Pedare Aquaponics Dashboard", windowWidth / 2, 30)

    fill("gray");
    textSize(16);
    textAlign(RIGHT, TOP);
    text("Last updated: " + (lastUpdated || "Loading..."), windowWidth - 15, 15);

    const ranges = [[0, 20], [20, 40], [40, 60], [60, 80], [80, 100]]

    drawMeter([100, 150], [0, 100], 10, 43, ranges)
}


function drawMeter(position, extrema, interval, value, ranges=null) {
    const range = extrema[1] - extrema[0];
    const spacing = 200 / range;
    const valueY = position[1] + 200 - value * spacing;

    if (ranges) {
        const colours = ["orange", "yellow", "chartreuse", "yellow", "orange"]
        for (let i = 0; i < 5; i++) {
            const rangeY = position[1] + 200 - ranges[i][1] * spacing;
            const rangeHeight = (ranges[i][1] - ranges[i][0]) * spacing;
            fill(colours[i]);
            rect(position[0], rangeY, 50, rangeHeight);
        }
    }

    noFill();
    stroke("black");
    strokeWeight(2);
    rect(position[0], position[1], 50, 200);

    let label = extrema[0];
    noStroke();
    while (label <= extrema[1]) {
        fill(0);
        textAlign(RIGHT, CENTER);
        textSize(10);
        text(label, position[0] - 4, position[1] + 200 - label * spacing);
        label += interval;
    }
    stroke("red");
    strokeWeight(2);
    line(position[0] + 2, valueY, position[0] + 48, valueY);
    noStroke()
}