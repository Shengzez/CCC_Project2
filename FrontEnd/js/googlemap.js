/**
 * @license
 * Copyright 2019 Google LLC. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */


 const mapStyle = [
  {
    stylers: [{ visibility: "on" }],
  },
  {
    featureType: "landscape",
    elementType: "geometry",
    stylers: [{ visibility: "on" }, { color: "#fcfcfc" }],
  },
  
  {
    featureType: "water",
    elementType: "geometry",
    stylers: [{ visibility: "on" }, { color: "#bfd4ff" }],
  },
];

let map;
let censusMin = Number.MAX_VALUE,
  censusMax = -Number.MAX_VALUE;

function initMap() {
  // load the map
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: -37.8136276, lng: 144.9630576 },
    // center: { lat: 40, lng: -100 },
    zoom: 13,
    styles: mapStyle,
  });
  // set up the style rules and events for google.maps.Data
  map.data.setStyle(styleFeature);
  map.data.addListener("mouseover", mouseInToRegion);
  map.data.addListener("mouseout", mouseOutOfRegion);

  // wire up the button
  const selectBox = document.getElementById("census-variable");

  google.maps.event.addDomListener(selectBox, "change", () => {
    clearCensusData();
    // load data from the previous selection
    loadCensusData(selectBox.options[selectBox.selectedIndex].value);
  });
  // state polygons only need to be loaded once, do them now
  loadMapShapes();
}

/** Loads the state boundary polygons from a GeoJSON source. */
function loadMapShapes() {
  
  // load US state outline polygons from a GeoJson file
  map.data.loadGeoJson(
    // "https://storage.googleapis.com/mapsdevsite/json/states.js",
    "https://raw.githubusercontent.com/tonywr71/GeoJson-Data/master/suburb-2-vic.geojson",
    { idPropertyName: "vic_loca_2" }
  );

  // wait for the request to complete by listening for the first feature to be
  // added
  google.maps.event.addListenerOnce(map.data, "addfeature", () => {
    google.maps.event.trigger(
      document.getElementById("census-variable"),
      "change"
    );
  });
}

/**
 * Loads the census data from a simulated API call to the US Census API.
 *
 * @param {string} variable
 */
// dealing with the data(need more discussion )
function loadCensusData(variable) {
  // load the requested variable from the census API (using local copies)
  const xhr = new XMLHttpRequest();

  xhr.open("GET", variable );
  xhr.onload = function () {
    const censusData = JSON.parse(xhr.responseText);
    //console.log(censusData);
    // censusData.shift(); // the first row contains column names
    // censusData.forEach((row) => {
    //   console.log(row)
    //   const censusVariable = parseFloat(90);
    //   // const stateId = row[1];
    //   const stateId = "MELBOURNE";
    //   console.log(stateId)

    //   // keep track of min and max values
    //   if (censusVariable < censusMin) {
    //     censusMin = censusVariable;
    //   }
      

    //   if (censusVariable > censusMax) {
    //     censusMax = censusVariable;
    //   }

    //   const state = map.data.getFeatureById(stateId);

    //   // update the existing row with the new data
    //   if (state) {
    //     state.setProperty("census_variable", censusVariable);
    //   }
    // });
    for (const [key, value] of Object.entries(censusData)) {
      const censusVariable = value['positive_rate']*100;
      const pos = value["positive"];
      const neg = value["negative"];
      const neu = value["neutural"];
      const name = value["name"];

      const stateId = key;
      console.log(key, value);
      if (censusVariable < censusMin) {
        censusMin = censusVariable;
      }
      
      if (censusVariable > censusMax) {
        censusMax = censusVariable;
      }
      
      const state = map.data.getFeatureById(stateId);
      if (state) {
          state.setProperty("positive", pos);
          state.setProperty("negative", neg);
          state.setProperty("neutural", neu);
          state.setProperty("stateId", key);
          state.setProperty("name", name);
            state.setProperty("census_variable", censusVariable);
          }

    };
    // update and display the legend
    document.getElementById("census-min").textContent =
      censusMin.toLocaleString();
    document.getElementById("census-max").textContent =
      censusMax.toLocaleString();
  };

  xhr.send();
}

/** Removes census data from each shape on the map and resets the UI. */
function clearCensusData() {
  censusMin = Number.MAX_VALUE;
  censusMax = -Number.MAX_VALUE;
  map.data.forEach((row) => {
    row.setProperty("census_variable", undefined);
  });
  document.getElementById("data-box").style.display = "none";
  document.getElementById("data-caret").style.display = "none";
}

/**
 * Applies a gradient style based on the 'census_variable' column.
 * This is the callback passed to data.setStyle() and is called for each row in
 * the data set.  Check out the docs for Data.StylingFunction.
 *
 * @param {google.maps.Data.Feature} feature
 */
function styleFeature(feature) {
  const low = [5, 69, 54]; // color of smallest datum
  const high = [151, 83, 34]; // color of largest datum
  // delta represents where the value sits between the min and max
  const delta =
    (feature.getProperty("census_variable") ) /
    (100);
  const color = [];

  for (let i = 0; i < 3; i++) {
    // calculate an integer color based on the delta
    color.push((high[i] - low[i]) * delta + low[i]);
  }

  // determine whether to show this shape or not
  let showRow = true;

  if (
    feature.getProperty("census_variable") == null ||
    isNaN(feature.getProperty("census_variable"))
  ) {
    showRow = false;
  }

  let outlineWeight = 0.5,
    zIndex = 1;

  if (feature.getProperty("state") === "hover") {
    outlineWeight = zIndex = 2;
  }
  return {
    strokeWeight: outlineWeight,
    strokeColor: "#fff",
    zIndex: zIndex,
    fillColor: "hsl(" + color[0] + "," + color[1] + "%," + color[2] + "%)",
    fillOpacity: 0.75,
    visible: showRow,
  };
}

/**
 * Responds to the mouse-in event on a map shape (state).
 *
 * @param {?google.maps.MapMouseEvent} e
 */
function mouseInToRegion(e) {
  // set the hover state so the setStyle function can change the border
  e.feature.setProperty("state", "hover");

  const percent =e.feature.getProperty("census_variable");

  // update the label
  // document.getElementById("data-label").textContent =
  //   e.feature.getProperty("NAME");
  document.getElementById("data-label").textContent =e.feature.getProperty("stateId");
  document.getElementById("data-value").textContent = e.feature
    .getProperty("census_variable")
    .toLocaleString();
  document.getElementById("data-box").style.display = "block";
  document.getElementById("data-caret").style.display = "block";
  document.getElementById("data-caret").style.paddingLeft = percent + "%";
}

/**
 * Responds to the mouse-out event on a map shape (state).
 *
 */
function mouseOutOfRegion(e) {
  // reset the hover state, returning the border to normal
  e.feature.setProperty("state", "normal");
}

window.initMap = initMap;
index.js
 