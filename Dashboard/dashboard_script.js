const API_ENDPOINT = "https://seneye-proxy.ezankov.workers.dev/";

let aquariumData = null;
let lastUpdated = "";
let connectionStatus = "";

const temperatureRanges = [[15, 20], [20, 22], [22, 26], [26, 28], [28, 35]];
const phRanges = [[6, 6.5], [6.5, 6.8], [6.8, 7.8], [7.8, 8.2], [8.2, 9]];
const ammoniaRanges = [[0, 0], [0, 0], [0, 0.02], [0.02, 0.05], [0.05, 0.08]]

let warningBlink = false;


function loadData() {
    data = loadJSON(API_ENDPOINT, onDataLoaded, onError);
    return data;
}


function onDataLoaded(data) {
    aquariumData = data;
    lastUpdated = new Date();
    console.log(lastUpdated, "Data refreshed successfully.");
    connectionStatus = "OK";
}


function onError(err) {
    console.log('Failed to load aquarium data. Check network and URL.', err);
    connectionStatus = "NOT OK";
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
    text("Last updated: " + lastUpdated.toLocaleTimeString(), windowWidth - 15, 15);

    const timeSinceUpdate = new Date() - lastUpdated;
    const minutesSinceUpdate = Math.floor(timeSinceUpdate / 60000);

    text(minutesSinceUpdate + " minutes ago", windowWidth - 15, 40);

    if (connectionStatus === "OK") {
        text("Connection status: " + connectionStatus, windowWidth - 15, 65);
    } else {
        fill("red");
        text("Connection status: " + connectionStatus, windowWidth - 15, 65);
        text("Check network and URL", windowWidth - 15, 90);
    }

    const temperature = aquariumData[0].exps.temperature.curr;
    const ph = aquariumData[0].exps.ph.curr;
    const ammonia = aquariumData[0].exps.nh3.curr;

    if (frameCount % 40 === 0) {
        warningBlink = !warningBlink;
    }

    drawCard([windowWidth / 2, 150], "Temperature", temperature, "°C", [temperatureRanges[0][0], temperatureRanges[4][1]], 2.5, temperatureRanges, warningBlink)
    drawCard([windowWidth / 5, 150], "pH Level", ph, "", [phRanges[0][0], phRanges[4][1]], 0.5, phRanges, warningBlink)
    drawCard([4 * windowWidth / 5, 150], "Ammonia Level", ammonia, "mg/L", [ammoniaRanges[0][0], ammoniaRanges[4][1]], 0.01, ammoniaRanges, warningBlink)
}


function drawMeter(position, extrema, interval, value, ranges) {
    const range = extrema[1] - extrema[0];
    const spacing = 200 / range;
    const valueY = position[1] + 200 - value * spacing + extrema[0] * spacing;

    const colours = ["orange", "yellow", "chartreuse", "yellow", "orange"]
    for (let i = 0; i < 5; i++) {
        const rangeY = position[1] + 200 - ranges[i][1] * spacing + extrema[0] * spacing;
        const rangeHeight = (ranges[i][1] - ranges[i][0]) * spacing;
        fill(colours[i]);
        rect(position[0], rangeY, 50, rangeHeight);
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


function drawCard(position, measurement, value, unit, extrema, interval, ranges, blink=false) {
    fill("black");
    textSize(24);
    textAlign(CENTER, TOP);
    text(measurement + ": " + +(+value).toPrecision(4) + unit, position[0], position[1]);

    drawMeter([position[0] - 25, position[1] + 50], extrema, interval, value, ranges);

    const colourMap = {"good": "green", "suboptimal": "chocolate", "bad": "red"}
    const measurementStatus = checkRange(ranges, value)

    fill(colourMap[measurementStatus[0]]);
    textSize(20);
    textAlign(CENTER, TOP);
    text(measurement + " is " + measurementStatus[0], position[0], position[1] + 275);

    if (measurementStatus[0] === "suboptimal") {
        text(measurement + " is " + measurementStatus[1], position[0], position[1] + 300)
    } else if (measurementStatus[0] === "bad" && !blink) {
        text("Warning: " + measurement + " is too " + measurementStatus[1], position[0], position[1] + 300)
    }
}


function checkRange(ranges, value) {
    const inRange = (num, extrema) => num >= extrema[0] && num <= extrema[1];

    if (inRange(value, ranges[2])) {
        return ["good", null]
    } else if (inRange(value, ranges[1])) {
        return ["suboptimal", "low"]
    } else if (inRange(value, ranges[3])) {
        return ["suboptimal", "high"]
    } else if (value < ranges[0][1]) {
        return ["bad", "low"]
    } else if (value > ranges[4][0]) {
        return ["bad", "high"]
    } else {
        return ["error", null]
    }
}