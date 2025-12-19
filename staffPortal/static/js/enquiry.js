    function toggleFields() {
        const education = document.getElementById("edu_status").value;
        const schoolField = document.getElementById("school-field");
        const courseField = document.getElementById("course_details");
        const collegeField = document.getElementById("college_university");
        const branchField = document.getElementById("branch");
        const passingYearField = document.getElementById("passing_year");
        const percentageField = document.getElementById("percentage_cgpa");
        if (education === "10th" || education === "12th" || education === "11th") {
            schoolField.style.display = "block";
            courseField.style.display = "block";
            collegeField.style.display = "none";
            branchField.style.display = "none";
            passingYearField.style.display = "none";
            percentageField.style.display = "none";
        
        }
        else if (education === "Graduate" || education === "Diploma" || education === "B-Tech" || education === "M-Tech" || education === "BCA" || education=="MCA")
        {
            // For higher education (college/university level)
            schoolField.style.display = "none";
            courseField.style.display = "none";
            collegeField.style.display = "block";
            branchField.style.display = "block";
            passingYearField.style.display = "block";
            percentageField.style.display = "block";
        } 
         else {
            schoolField.style.display = "none";
            courseField.style.display = "none";
            collegeField.style.display = "none";
            branchField.style.display = "none";
            passingYearField.style.display = "none";
            percentageField.style.display = "none";
        }
    }

    

function show_exp(is_exp) {
    var expDiv = document.getElementById('exp_div');
    if (is_exp) {
        expDiv.classList.add("show");
    } else {
        expDiv.classList.remove("show");
    }
}  