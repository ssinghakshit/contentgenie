function generateBlog() {
    // Code to generate the email text using backend content
  
    // Update the content of the generated-email div
    var generatedBlogDiv = document.getElementById("generated-blog");
    generatedBlogDiv.innerHTML = generatedBlogText;
  
    // Scroll to the output section
    document.getElementById("output-section").scrollIntoView();
  }
  