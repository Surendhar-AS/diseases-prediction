function addSymptom() {
    var symptomsText = document.getElementById("symptomsText");
    var symptomsDropdown = document.getElementById("symptomsDropdown");
    var selectedSymptom = symptomsDropdown.value.trim(); // Trim whitespace
    if (selectedSymptom !== "") {
      // Check if the symptom is already present
      var symptoms = symptomsText.querySelectorAll("span");
      for (var i = 0; i < symptoms.length; i++) {
        if (symptoms[i].textContent.trim() === selectedSymptom) {
          alert("Symptom already exists!");
          return; // Exit function if symptom already exists
        }
      }
      // If symptom is not present, add it to the div
      var span = document.createElement("span");
      span.textContent = selectedSymptom;
      symptomsText.appendChild(span);
      symptomsText.appendChild(document.createElement("br"));
    }
  }
  
  
  function moveSelection(direction) {
    var symptomsText = document.getElementById("symptomsText");
    var spans = symptomsText.getElementsByTagName("span");
    var currentSelectionIndex = -1;
    // Find the index of the currently selected item
    for (var i = 0; i < spans.length; i++) {
      if (spans[i].classList.contains("highlight")) {
        currentSelectionIndex = i;
        break;
      }
    }
    // Calculate the new index based on the direction
    var newIndex = currentSelectionIndex + direction;
    // Ensure the index stays within bounds
    newIndex = Math.max(0, Math.min(newIndex, spans.length - 1));
    // Deselect all existing selections
    for (var i = 0; i < spans.length; i++) {
      spans[i].classList.remove("highlight");
    }
    // Select the new item
    spans[newIndex].classList.add("highlight");
  }
  
  function clearSelectedSymptom() {
    var symptomsText = document.getElementById("symptomsText");
    var highlightedText = symptomsText.querySelector(".highlight");
    if (highlightedText) {
      var nextElement = highlightedText.nextElementSibling;
      
      // Remove the highlighted text
      highlightedText.parentNode.removeChild(highlightedText);
      
      // Remove empty line after the removed text
      if (nextElement && nextElement.tagName.toLowerCase() === 'br') {
        nextElement.parentNode.removeChild(nextElement);
      }
      
      // Move subsequent text up
      if (nextElement && nextElement.textContent) {
        var textNode = document.createTextNode(nextElement.textContent);
        symptomsText.insertBefore(textNode, nextElement);
      }
    }
  }
  
  
  
  function clearAllSymptoms() {
    document.getElementById("symptomsText").innerHTML = "";
    document.getElementById("output").innerHTML = "";
  }
  
  // Prevent manual editing by disabling typing
  document.getElementById("symptomsText").addEventListener("keypress", function(event) {
    event.preventDefault();
  });
  
  // Allow mouse movement within the symptoms area
  document.getElementById("symptomsText").addEventListener("mousedown", function(event) {
    event.preventDefault();
  });
  
  function predict() {
      // Step i: Check number of symptoms selected
      var symptomsText = document.getElementById("symptomsText");
      var symptomsCount = symptomsText.querySelectorAll("span").length;
      if (symptomsCount < 3 || symptomsCount > 16) {
          alert("Please select between 3 and 16 symptoms.");
          return;
      }
  
      // Step ii: Replace spaces with underscores and save in an array
      var symptomsArray = [];
      var spans = symptomsText.querySelectorAll("span");
      spans.forEach(function(span) {
          var symptom = span.textContent.trim().replace(/\s+/g, '_'); // Replace spaces with underscores
          symptomsArray.push(symptom);
      });
  
      // Step iii: Send POST request to Flask server
      fetch('/predict', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ symptoms: symptomsArray })
      })
      .then(response => response.json())
      .then(data => {
          var outputDiv = document.getElementById("output");
          outputDiv.innerHTML = "<h3>Top three best matched diseases:</h3>";
          var ul = document.createElement("ul");
          data.predicted_diseases.forEach(function(disease) {
              var li = document.createElement("li");
              li.textContent = disease;
              ul.appendChild(li);
          });
          outputDiv.appendChild(ul);
      })
      .catch(error => console.error('Error:', error));
  }
  
  function logout() {
      fetch('/logout')
      .then(response => {
          if (response.redirected) {
              window.location.href = response.url; // Redirect to login page
          }
      })
      .catch(error => console.error('Error:', error));
  }
  
  function toggleDropdown() {
    document.getElementById("dropdownContent").classList.toggle("show");
  }
  
  // Close the dropdown menu if the user clicks outside of it
  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }