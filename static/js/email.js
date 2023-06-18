function generateEmail() {
    // Code to generate the email text using backend content
  
    // Update the content of the generated-email div
    var generatedEmailDiv = document.getElementById("generated-email");
    generatedEmailDiv.innerHTML = generatedEmailText;
  
    // Scroll to the output section
    document.getElementById("output-section").scrollIntoView();
  }
function copyToClipboard() {
    var copyText = document.getElementById("generated-email");
    copyText.select();
    document.execCommand("copy");
  }