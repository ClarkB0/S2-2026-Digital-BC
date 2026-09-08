const API_ENDPOINT = "https://seneye-proxy.ezankov.workers.dev/";

let aquariumData = null;
let lastUpdated = "";

console.log('testing');


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
    if (aquariumData) {
        let temp = aquariumData[0].exps.temperature.curr || 999;
        let ph = aquariumData[0].exps.ph.curr || 999;
        let nh3 = aquariumData[0].exps.nh3.curr || 999;

        let stats = [
            "Temperature: " + temp,
            "PH: " + ph,
            "NH3: " + nh3
        ]

        fill(0);
        textSize(24);
        textAlign(LEFT, TOP);
        text(stats.join("\n"), 0, 0);
    } else {
        fill(0);
        textSize(24);
        textAlign(LEFT, TOP);
        text("Connecting to sensor stream...", 30, 120);
    }
}