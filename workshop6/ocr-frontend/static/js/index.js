function checkAndEnablePermissions() {
   // Check and enable geolocation permission
   if ("geolocation" in navigator) {
      navigator.permissions.query({
         name: 'geolocation'
      }).then(function (geolocationResult) {
         if (geolocationResult.state === 'prompt') {
            navigator.geolocation.getCurrentPosition(function () {
               // Geolocation permission is granted, you can proceed
            }, function (error) {
               console.error("Geolocation permission denied:", error);
            });
         }
      });
   } else {
      console.error("Geolocation is not supported by this browser.");
   }

   // Check and enable camera permission
   if ("mediaDevices" in navigator && "getUserMedia" in navigator.mediaDevices) {
      navigator.mediaDevices.getUserMedia({
         video: true
      }).then(function (stream) {
         // Camera permission is granted, you can proceed
      }).catch(function (error) {
         console.error("Camera permission denied:", error);
      });
   } else {
      console.error("Camera access is not supported by this browser.");
   }
}

// Call the function to check and enable both permissions when the page loads
document.addEventListener('DOMContentLoaded', function () {
   checkAndEnablePermissions();
});

function updateCameraButtonPosition() {
   const cameraButton = document.getElementById("capture-button");
   const timestamp = document.getElementById("timestamp");
   // Get the current orientation (0, 90, -90, or 180 degrees)
   const orientation = window.orientation || window.screen.orientation.angle;

   if (orientation === 90 || orientation === -90) {
      // Landscape orientation
      cameraButton.style.transform = "translate(0, -50%)"; // Center the button vertically
      timestamp.style.display = 'none';
   } else {
      // Portrait orientation (default)
      cameraButton.style.transform = "translate(0, -50%)"; // Center the button vertically
   }
}


// Listen for changes in orientation
window.addEventListener("orientationchange", updateCameraButtonPosition);
window.addEventListener("resize", updateCameraButtonPosition);

// Initial call to set the initial position
updateCameraButtonPosition();


//Event Scripts
document.addEventListener('DOMContentLoaded', function () {
   // Function to display the popup
   function displayPopup() {
      var popup = document.getElementById('popup');
      popup.style.display = 'block';
      // Lock body scrolling
      document.body.style.overflow = 'hidden';
   }

   // Show the popup when the page loads
   displayPopup();

   // Close the popup when the "Close" button is clicked
   document.getElementById('close-popup').addEventListener('click', function () {
      var popup = document.getElementById('popup');
      popup.style.display = 'none';
      // Unlock body scrolling
      document.body.style.overflow = 'auto';
   });

   // Enable swiping for elements with the class 'swipable-container'
   document.querySelectorAll('.swipable-container').forEach(function (el) {
      el.classList.add('swiper-no-swiping');
   });

   // Enable touch events when clicking on the map
   document.getElementById('map').addEventListener('click', function () {
      swiper.allowTouchMove = false;
   });

   // Disable touch events when clicking outside of the map
   document.body.addEventListener('click', function (event) {
      if (event.target.closest('#map')) {
         swiper.allowTouchMove = false;
      } else {
         swiper.allowTouchMove = true;
      }
   });
});

function padTo2Digits(num) {
   return num.toString().padStart(2, '0');
}

function formatTimestampToYYYYMMDDHHMMSS(timestamp) {
   const date = new Date(timestamp);
   const year = date.getFullYear();
   const month = String(date.getMonth() + 1).padStart(2, '0');
   const day = String(date.getDate()).padStart(2, '0');
   const hours = String(date.getHours()).padStart(2, '0');
   const minutes = String(date.getMinutes()).padStart(2, '0');
   const seconds = String(date.getSeconds()).padStart(2, '0');

   return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}


// Define global variables to store selected values
let selectedSession = null;
let selectedReportingType = null;

// Get session buttons
const sessionButtons = document.querySelectorAll('.session-btn');

// Get reporting type buttons
const reportingButtons = document.querySelectorAll('.reporting-btn');

sessionButtons.forEach(button => {
   button.addEventListener('click', function onClick() {
      // Reset all buttons to their default state
      sessionButtons.forEach(b => {
         b.style.backgroundColor = '';
         b.style.color = '';
      });

      // Set the clicked button's style
      this.style.backgroundColor = 'salmon';
      this.style.color = 'white';

      selectedSession = this.textContent.trim();
   });
});

reportingButtons.forEach(button => {
   button.addEventListener('click', function onClick() {
      // Reset all buttons to their default state
      reportingButtons.forEach(b => {
         b.style.backgroundColor = '';
         b.style.color = '';
      });

      // Set the clicked button's style
      this.style.backgroundColor = 'salmon';
      this.style.color = 'white';

      selectedReportingType = this.textContent.trim();
   });
});


const currentHour = new Date().getHours();

if (currentHour < 12) {
   const morningSessionButton = document.getElementById('morning-session');
   morningSessionButton.click();
} else {
   const afternoonSessionButton = document.getElementById('afternoon-session');
   afternoonSessionButton.click();
}
const normalReportingButton = document.getElementById('normal-reporting');
normalReportingButton.click();


// Modify the existing "Submit!" button to capture and upload the photo
var submitButton = document.getElementById("submit-form");

const form = document.getElementById("weightForm");

// Attach a click event listener to the custom trigger button
submitButton.addEventListener("click", triggerFormSubmit);

// Trigger the onsubmit event of the form
function triggerFormSubmit() {
   if (form.onsubmit) {
      // Execute the onsubmit event handler
      const onSubmitResult = form.onsubmit();

      // Check if the onsubmit handler returns true (allowing submission)
      if (onSubmitResult !== false) {
         // Trigger the click event of the submit button
         existingClickEventListener();
      }
   }
}

function existingClickEventListener() {
   if (!manualWeightForm && !extractedWeight) {
      alert("Key in Weight Manually");
      return;
   }

   if (!timestamp) {
      swiper.slidePrev();
      swiper.slidePrev();
   }

   // Upload the captured photo to Flask
   var imageBase64 = capturedImage.src;
   var formData = new FormData();
   var imageFilename = "captured_image"; // Replace this with the actual image filename
   timestamp = formatTimestampToYYYYMMDDHHMMSS(timestamp);
   var formattedTimestamp = timestamp
      .replace(/[\/:,\s]/g, '_')
      .replace(/__/g, '_');
   var imageWithTimestamp = imageFilename + "_" + formattedTimestamp + ".png";
   console.log(imageWithTimestamp);
   formData.append("image", dataURItoBlob(imageBase64), imageWithTimestamp);
   formData.append("extractedWeight", extractedWeight);
   formData.append("selectedBinCenter", selectedBinCenter);
   formData.append("manualWeightForm", manualWeightForm);
   formData.append("timestamp", timestamp);
   formData.append("latitude", latitude);
   formData.append("longitude", longitude);
   formData.append("selectedSession", selectedSession);
   formData.append("selectedReportingType", selectedReportingType);

   var xhr = new XMLHttpRequest();
   xhr.open("POST", "/results", true);
   xhr.send(formData);

   xhr.onload = function () {
      if (xhr.status === 200) {
         alert("Submission successful!");
         window.location.reload();
      } else {
         alert("Submission failed! Please try again.");
      }
   };
};

function dataURItoBlob(dataURI) {
   var byteString = atob(dataURI.split(",")[1]);
   var mimeString = dataURI.split(",")[0].split(":")[1].split(";")[0];
   var ab = new ArrayBuffer(byteString.length);
   var ia = new Uint8Array(ab);
   for (var i = 0; i < byteString.length; i++) {
      ia[i] = byteString.charCodeAt(i);
   }
   return new Blob([ab], {
      type: mimeString
   });
}

function validateWeight() {
   var weightInput = parseFloat(document.getElementById("weight").value);

   if (weightInput < 0) {
      alert("Weight must be greater than or equal to 0. Please input again.");
      return false; // Prevent form submission
   } else if (isNaN(weightInput)) {
      // No value provided for weight input
      return true; // Prevent form submission
   }
   manualWeightForm = weightInput; // Update extractedWeight with the input value
   return true; // Allow form submission
}

// Define the coordinates of the National University of Singapore
const nusCoordinates = [1.2921, 103.7769];

// Create a green marker icon
const greenIcon = new L.Icon({
   iconUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png",
   shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
   iconSize: [25, 41],
   iconAnchor: [12, 41],
   popupAnchor: [1, -34],
   shadowSize: [41, 41],
});

// Initialize the map
const map = L.map("map").setView(nusCoordinates, 15);

// Add a tile layer to the map (you can replace the tile URL with your desired map)
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
   attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

const markerDropdown = document.getElementById("marker-dropdown");

markerDropdown.innerHTML = '';

binCenters.sort((a, b) => a.binCenterID - b.binCenterID);

binCenters.forEach((binCenter) => {
   const option = document.createElement("option");
   option.value = binCenter.binCenterName;
   option.setAttribute("data-lat", binCenter.binCenterLat);
   option.setAttribute("data-lon", binCenter.binCenterLon);
   option.textContent = binCenter.binCenterName;
   markerDropdown.appendChild(option);
});

markerDropdown.addEventListener("change", () => {
   const selectedValue = markerDropdown.value;
   const selectedOption = markerDropdown.options[markerDropdown.selectedIndex];
   const selectedMarkerIndex = markerDropdown.selectedIndex; // Since the values match the marker indices

   // Reset all markers to the default icon
   markers.forEach((marker, index) => {
      if (index === selectedMarkerIndex) {
         // Change the icon to green for the selected marker
         marker.setIcon(greenIcon);
         marker.setLatLng([parseFloat(selectedOption.getAttribute("data-lat")), parseFloat(selectedOption.getAttribute("data-lon"))]);
         marker.openPopup();
      } else {
         // Reset other markers to the default icon
         marker.setIcon(defaultIcon);
      }
   });
});


// Create an array of markers with popups
const markers = binCenters.map((binCenter, index) => {
   const coords = [binCenter.binCenterLat, binCenter.binCenterLon];
   const marker = L.marker(coords).addTo(map);
   const popupContent = `${binCenter.binCenterName}`;
   marker.bindPopup(popupContent);

   // Add click event listener to change the icon to green
   marker.on("click", () => {
      // Reset all markers to the default icon
      markers.forEach((m, i) => {
         if (i === index) {
            // Change the icon to green for the clicked marker
            m.setIcon(greenIcon);
            m.openPopup(); // Open the popup for the clicked marker
         } else {
            // Reset other markers to the default icon
            m.setIcon(defaultIcon);
         }
      });

      // Update the dropdown value
      document.getElementById("marker-dropdown").value = binCenter.binCenterName;
   });

   // Set the initial icon to green for the default marker
   if (index === 0) {
      marker.setIcon(greenIcon);
      marker.openPopup(); // Open the popup for the default marker
   }

   return marker;
});


// Default marker 
const defaultIcon = new L.Icon({
   iconUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
   shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
   iconSize: [25, 41],
   iconAnchor: [12, 41],
   popupAnchor: [1, -34],
   shadowSize: [41, 41],
});


const cameraFeedVideo = document.getElementById("camera-feed-video");
const boundingBox = document.getElementById("bounding-box");
const captureButton = document.getElementById("capture-button");
const capturedImage = document.getElementById("captured-image");
const confirmButton = document.getElementById("confirm-button");
const retakeButton = document.getElementById("retake-button");
const customDialog = document.getElementById("custom-dialog");
const dialogInput = document.getElementById("dialog-input");
const dialogOK = document.getElementById("dialog-ok");
const dialogCancel = document.getElementById("dialog-cancel");
const instructions = document.getElementById("instructions");

let extractedWeight = null; // To store the extracted weight
let selectedBinCenter = null; // To store the selected bin center
let timestamp = null; //To store timestamp
let manualWeightForm = null; //To store manual weight input by user
let latitude = null;
let longitude = null;

async function startCamera() {
   try {
      const stream = await navigator.mediaDevices.getUserMedia({
         video: {
            facingMode: "environment"
         }
      });
      cameraFeedVideo.srcObject = stream;
   } catch (error) {
      console.error("Error accessing the camera:", error);
   }
}

startCamera();

captureButton.addEventListener("click", () => {
   getLocation();
   document.getElementById("instructions").style.display = 'none';
   const photoCanvas = document.createElement("canvas");
   const photoCtx = photoCanvas.getContext("2d");

   // Get the video element
   const cameraFeedVideo = document.getElementById("camera-feed-video");

   // Calculate the new width and height (70% of the original dimensions)
   const newWidth = cameraFeedVideo.videoWidth * 0.7;
   const newHeight = cameraFeedVideo.videoHeight * 0.7;

   // Set the dimensions of the canvas to the new width and height
   photoCanvas.width = newWidth;
   photoCanvas.height = newHeight;

   // Draw the resized image onto the canvas
   photoCtx.drawImage(cameraFeedVideo, 0, 0, newWidth, newHeight);

   const isLandscape = window.matchMedia("(orientation: landscape)").matches;
   // Display the captured photo
   capturedImage.src = photoCanvas.toDataURL();
   cameraFeedVideo.style.display = "none";
   timestamp = new Date().toLocaleString();
   document.getElementById('timestamp').textContent = `Timestamp: ${timestamp}`;

   if (isLandscape) {
      capturedImage.style.display = 'block';
      const windowHeight = window.innerHeight;
      // Adjust the height of the captured image based on the window height
      capturedImage.style.height = windowHeight * 0.7 + 'px'; // Set to 70% of the window height, adjust as needed
      document.getElementById('timestamp').style.display = 'none';
      document.getElementById('bounding-box').style.display = 'none';
      confirmButton.style.display = "block";
      retakeButton.style.display = "block";
      // Hide the capture button
      captureButton.style.display = "none";
      skipButton.style.display = "none";
   } else {
      capturedImage.style.display = 'block';
      document.getElementById('timestamp').style.display = 'block';
      document.getElementById('bounding-box').style.display = 'none';
      confirmButton.style.display = "block";
      retakeButton.style.display = "block";
      captureButton.style.display = "none";
      skipButton.style.display = "none";
   }
});


dialogCancel.addEventListener("click", () => {
   // Hide the custom dialog box
   customDialog.style.display = "none";
});

var retakenPhoto = false;
// Add a click event listener to the confirm button
confirmButton.addEventListener("click", () => {
   // Call the simulate50PercentChance function
   simulate50PercentChance();
});

retakeButton.addEventListener("click", () => {
   // Handle retake (e.g., clear the captured image)
   capturedImage.style.display = "none";
   confirmButton.style.display = "none";
   retakeButton.style.display = "none";
   captureButton.style.display = "inline-block"; // Show the capture button again
   // Show the camera feed again
   cameraFeedVideo.style.display = "block";
   document.getElementById('bounding-box').style.display = 'block';
   // Hide the timestamp element when the "Retake" button is clicked
   document.getElementById('timestamp').style.display = 'none';
   if (window.orientation === 90 || window.orientation === -90) {
      // Landscape orientation
      document.getElementById("instructions").style.display = 'none';
   }
});


function getLocation() {
   if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(showPosition);
   } else {
      alert("Geolocation is not supported by this browser.");
   }
}

function showPosition(position) {
   latitude = position.coords.latitude;
   longitude = position.coords.longitude;
}


function showManualInputLabel() {
   var weightInput = document.getElementById("weight").value;
   var manualInputLabel = document.getElementById("manual-input-label");
   var manualWeight = document.getElementById("manual-weight");
   var hrElement = document.querySelector(".gradient");
   manualWeightForm = document.getElementById("weight").value;

   if (weightInput.trim() !== "") {
      manualInputLabel.style.display = "block";
      manualWeight.textContent = weightInput + " kg";
      hrElement.style.display = "block"; // Show the <hr> element
   } else {
      manualInputLabel.style.display = "none";
      hrElement.style.display = "none"; // Hide the <hr> element
   }
}


// Define swiper in a higher scope
var swiper = new Swiper('.swiper-container', {
   slidesPerView: 1, // Display one card at a time
   spaceBetween: 15, // Adjust the spacing between cards
   navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
   },
   allowTouchMove: true, // Initially disable touch events
});


swiper.on('slideChange', function () {
   // Check if the last slide is reached
   if (swiper.isEnd) {
      // Load the data when the last slide is reached
      loadDataForLastSlide();
   }
});

// Function to load the data for the last slide
function loadDataForLastSlide() {
   // Get the selected bin center when Show Results is clicked
   selectedBinCenter = document.getElementById("marker-dropdown").value;
   // Update the displayed results
   document.getElementById("selected-bin-center").textContent = selectedBinCenter;
   document.getElementById("extracted-weight").textContent = extractedWeight ? extractedWeight + " kg" : "Not available";
   document.getElementById("time-stamp").textContent = timestamp ? timestamp : "Not taken";
}


// Function to perform OCR extraction with backend
function simulate50PercentChance() {
   const randomNumber = Math.random(); // Generate a random number between 0 and 1
   var imageBase64 = capturedImage.src;
   var formData = new FormData();
   formData.append("image", dataURItoBlob(imageBase64), "captured_image.png");
   console.log(formData);
   var xhr = new XMLHttpRequest();
   xhr.open("POST", "/upload", true);

   xhr.onload = function () {
      if (xhr.status === 200) {
         // If the request was successful, parse the JSON response
         var response = JSON.parse(xhr.responseText);

         // Access the 'result' property from the JSON response
         var result = response.result;

         console.log("Result: " + result);

         if (result == "Approved") {
            // 50% chance of success, proceed to store weights
            extractedWeight = response.weight;

            alert("Success! Proceeding to the next page.");
            // Use the swiper API to move to the next slide/page
            setTimeout(function () {
               swiper.slideNext();
            }, 1000); // Adjust the timeout duration (in milliseconds) as needed
         } else {
            // 50% chance of failure, show an error popup and ask to retake
            if (!retakenPhoto) {
               // User has not retaken a photo yet
               alert("Error! Please retake the picture.");

               // Show retake and skip buttons
               retakeButton.style.display = "inline-block";
               skipButton.style.display = "inline-block";

               // Set retakenPhoto to true to track that the user has retaken a photo
               retakenPhoto = true;
            }

            // Navigate back to the capture
            capturedImage.style.display = "none";
            confirmButton.style.display = "none";
            retakeButton.style.display = "none";
            captureButton.style.display = "inline-block"; // Show the capture button again
            cameraFeedVideo.style.display = "block";
            document.getElementById('bounding-box').style.display = 'block';

            // Hide the timestamp element when the "Retake" button is clicked
            document.getElementById('timestamp').style.display = 'none';
         }

         // Perform any further actions based on the result here
      } else {
         // Handle the case where the request was not successful
         console.error("Error: " + xhr.status);
      }
   };

   xhr.send(formData);

}

function skipToNextPage() {
   swiper.slideNext();
}

// Add a click event listener to the "Skip" button
var skipButton = document.getElementById('skip-button');
skipButton.addEventListener('click', skipToNextPage);