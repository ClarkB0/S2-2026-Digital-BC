const API_ENDPOINT = "https://seneye-proxy.ezankov.workers.dev/";

let aquariumData = null;
let lastUpdated = "";

// format these as the correct arrays later
const temperatureRanges = [[15, 20], [20, 22], [22, 26], [26, 28], [28, 35]];
const phRanges = [[6, 6.5], [6.5, 6.8], [6.8, 7.8], [7.8, 8.2], [8.2, 9]];
const ammoniaRanges = [[0, 0], [0, 0], [0, 0.02], [0.02, 0.05], [0.05, 0.06]]


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
    text("Last updated: " + lastUpdated, windowWidth - 15, 15);

    const temperature = aquariumData[0].exps.temperature.curr;
    const ph = aquariumData[0].exps.ph.curr;
    const ammonia = aquariumData[0].exps.nh3.curr;

    drawMeter([100, 150], [temperatureRanges[0][0], temperatureRanges[4][1]], 2.5, temperature, temperatureRanges);
    drawMeter([300, 150], [phRanges[0][0], phRanges[4][1]], 1, ph, phRanges);
    drawMeter([500, 150], [ammoniaRanges[0][0], ammoniaRanges[4][1]], 0.01, ammonia, ammoniaRanges);
}


function drawMeter(position, extrema, interval, value, ranges=null) {
    const range = extrema[1] - extrema[0];
    const spacing = 200 / range;
    const valueY = position[1] + 200 - value * spacing + extrema[0] * spacing;

    if (ranges) {
        const colours = ["orange", "yellow", "chartreuse", "yellow", "orange"]
        for (let i = 0; i < 5; i++) {
            const rangeY = position[1] + 200 - ranges[i][1] * spacing + extrema[0] * spacing;
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
    while (label < extrema[1] + interval) {
        fill(0);
        textAlign(RIGHT, CENTER);
        textSize(10);
        text(+label.toPrecision(4), position[0] - 4, position[1] + 200 - label * spacing + extrema[0] * spacing);
        label += interval;
    }
    stroke("red");
    strokeWeight(2);
    line(position[0] + 2, valueY, position[0] + 48, valueY);
    noStroke()
}