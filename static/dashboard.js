const contactInfo = {
    webLink: "https://yourweb.com",
    phoneNumber: "+123456789",
    email: "contact@yourweb.com",
    linkedIn: "https://linkedin.com/in/yourprofile",
    instagram: "https://instagram.com/yourprofile"
};

function approveCVE(cveNumber, description, severity) {
    const publishedDate = new Date().toUTCString();
    const emailContent = `
        <h3>NEW CVE UPDATES</h3>
        <p><strong>Dear User,</strong></p>
        <p>This is an important notification regarding the following CVE:</p>
        
        <h4>Octopus Server Improper Access Control</h4>
        <p>
            <strong>CVE NUMBER:</strong> ${cveNumber}<br>
            <strong>SEVERITY:</strong> ${severity}<br>
            ${description}<br>
            <strong>Published Date:</strong> ${publishedDate}
        </p>

        <p>Please take the necessary actions to address these issues.</p>
        <p>Contact Information:</p>
        <ul>
            <li>Web: <a href="${contactInfo.webLink}" target="_blank">${contactInfo.webLink}</a></li>
            <li>Phone: ${contactInfo.phoneNumber}</li>
            <li>Email: <a href="mailto:${contactInfo.email}">${contactInfo.email}</a></li>
            <li>LinkedIn: <a href="${contactInfo.linkedIn}" target="_blank">${contactInfo.linkedIn}</a></li>
            <li>Instagram: <a href="${contactInfo.instagram}" target="_blank">${contactInfo.instagram}</a></li>
        </ul>
        <p>&copy; 2024 Necurity | All Rights Reserved</p>
        <p>Best Regards,<br>Your Security Team</p>
    `;

    document.getElementById('template-container').innerHTML = emailContent;
}

function showTemplate(templateToShow) {
    const templates = ['template1', 'template2', 'template3'];
    templates.forEach(template => {
        const element = document.getElementById(template);
        if (element) {
            element.style.display = template === templateToShow ? 'block' : 'none';
        } else {
            console.error(`Template element with id "${template}" not found.`);
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    // Ensure that event listeners are added only once
    const button1 = document.getElementById("button1");
    const button2 = document.getElementById("button2");
    const button3 = document.getElementById("button3");

    // Remove previous event listeners before adding new ones to avoid duplicates
    if (button1) {
        button1.removeEventListener("click", loadTemplate1);  // Remove previous listeners
        button1.addEventListener("click", loadTemplate1);
    }
    if (button2) {
        button2.removeEventListener("click", loadTemplate2);  // Remove previous listeners
        button2.addEventListener("click", loadTemplate2);
    }
    if (button3) {
        button3.removeEventListener("click", loadTemplate3);  // Remove previous listeners
        button3.addEventListener("click", loadTemplate3);
    }
});

// Function to fetch and load Template 1
function loadTemplate1() {
    fetch('/template1')
        .then(response => response.ok ? response.text() : Promise.reject("Network response was not ok"))
        .then(data => {
            const container = document.getElementById("template-container");
            container.innerHTML = ''; // Clear any previous content
            container.innerHTML = data; // Insert new template content
        })
        .catch(error => console.error("Fetch error for template1:", error));
}

// Function to fetch and load Template 2
function loadTemplate2() {
    fetch('/template2')
        .then(response => response.ok ? response.text() : Promise.reject("Network response was not ok"))
        .then(data => {
            const container = document.getElementById("template-container");
            container.innerHTML = ''; // Clear any previous content
            container.innerHTML = data; // Insert new template content
        })
        .catch(error => console.error("Fetch error for template2:", error));
}

// Function to fetch and load Template 3
function loadTemplate3() {
    fetch('/template3')
        .then(response => response.ok ? response.text() : Promise.reject("Network response was not ok"))
        .then(data => {
            const container = document.getElementById("template-container");
            container.innerHTML = ''; // Clear any previous content
            container.innerHTML = data; // Insert new template content
        })
        .catch(error => console.error("Fetch error for template3:", error));
}


function sendEmail(template) {
    const recipientEmail = document.getElementById('recipientEmail').value;
    if (!recipientEmail) {
        alert('Please enter a recipient email.');
        return;
    }
    
    fetch('/send_email', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            recipient: recipientEmail,
            template: template
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert(data.message);
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        alert('An error occurred: ' + error);
    });
}

// Function to handle sending a "Sent Email"
function sendSentEmail() {
    const recipientEmail = document.getElementById("recipient_email").value;
    const cveNumber = document.getElementById("modal-cve-number").value;
    const emailContent = document.getElementById("modal-email-preview").innerHTML;

    if (!recipientEmail || !emailContent) {
        alert("Please fill in the recipient email and select a template.");
        return;
    }

    fetch('/send_approval_email', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            recipient_email: recipientEmail,
            cve_number: cveNumber,
            email_content: emailContent
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Email sent successfully!");
        } else {
            alert("Failed to send email.");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An error occurred while sending the email.");
    });
}

function sendEmail() {
    const recipientEmail = document.getElementById('recipient_email').value;
    const selectedTemplate = document.querySelector('input[name="template"]:checked')?.value; // Get the selected template

    if (!selectedTemplate) {
        alert('Please select a template.');
        return;
    }

    let emailContent = '';

    if (selectedTemplate === 'template1') {
        emailContent = `
            <html>
                <head><title>Template 1</title></head>
                <body>
                    <h1>Welcome to Template 1</h1>
                    <p>This is the full HTML design for Template 1.</p>
                    <p><strong>Important:</strong> Don't forget to customize it!</p>
                </body>
            </html>
        `;
    } else if (selectedTemplate === 'template2') {
        emailContent = `
            <html>
                <head><title>Template 2</title></head>
                <body>
                    <h1>Welcome to Template 2</h1>
                    <p>This is the full HTML design for Template 2.</p>
                </body>
            </html>
        `;
    } else if (selectedTemplate === 'template3') {
        emailContent = `
            <html>
                <head><title>Template 3</title></head>
                <body>
                    <h1>Welcome to Template 3</h1>
                    <p>This is the full HTML design for Template 3.</p>
                </body>
            </html>
        `;
    }

    if (recipientEmail && emailContent) {
        fetch('/send_email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                recipient_email: recipientEmail,
                email_content: emailContent // Full HTML content of the selected template
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Email sent successfully!');
            } else {
                alert('Failed to send email.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while sending the email.');
        });
    } else {
        alert("Please enter a recipient email.");
    }
}


function rejectCVE(button) {
    const row = button.closest('tr');
    const cveNumber = row.cells[0].textContent.trim();
    const description = row.cells[1].textContent.trim();
    const severity = row.cells[4].textContent.trim();

    const rejectedTable = document.getElementById('rejected-list-table').getElementsByTagName('tbody')[0];
    const newRow = rejectedTable.insertRow();

    newRow.insertCell(0).textContent = cveNumber;
    newRow.insertCell(1).textContent = description;
    newRow.insertCell(2).textContent = severity;

    row.remove();
}

function sendEmailToGroup() {
    const group = document.querySelector('input[name="group"]:checked').value;  // Selected group (e.g., 'Group A')
    const template = document.querySelector('textarea#template').value;  // Selected template content

    fetch('/send-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ group: group, template: template })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            alert(data.message);
        } else {
            alert("Error: " + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
