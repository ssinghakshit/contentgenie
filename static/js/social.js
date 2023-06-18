function generateSocial() {
    // Code to generate the email text using backend content
  
    // Update the content of the generated-email div
    var generatedSocialDiv = document.getElementById("generated-Social");
    generatedSocialDiv.innerHTML = generatedSocialText;
  
    // Scroll to the output section
    document.getElementById("output-section").scrollIntoView();
  }
  