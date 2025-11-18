function studentShowTab(tab) {
  document.getElementById('current-classes').style.display =
    tab === 'current' ? 'block' : 'none';

  document.getElementById('add-classes').style.display =
    tab === 'add' ? 'block' : 'none';
}
function toggleClass(classId) {
  classId = Number(classId);
    fetch("/toggle_class", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ class_id: classId })
    })
    .then(res => res.json())
    .then(data => {
      console.log(data);
      location.reload();
    })
    .catch(err => console.error("Error:", err));
}

function loadClassDetails(classId) {
  classId = Number(classId)
  fetch(`/class/${classId}/students`, {
    method: "GET",
    credentials: "include"
  })
  .then(res => res.json())
  .then(data => {
    let html = `
      <h3>Students in this Class</h3>
      <button onclick="backToTeacher()">Back</button>
      <table border="1" cellspacing="0" cellpadding="8">
        <thead>
          <tr>
            <th>Student</th>
            <th>Grade</th>
          </tr>
        </thead>
      <tbody>
    `;

    data.forEach(row => {
      html += `
        <tr>
          <td>${row.name}</td>
          <td>
            ${row.grade}
            <button onclick="editGrade(${row.enrollment_id}, ${row.grade})">Edit</button>
          </td>
        </tr>
      `;
    });

    html += `</tbody></table>`;

    document.getElementById("class-details").innerHTML = html;
    document.getElementById("class-details").style.display = "block";
    document.getElementById("teaching-classes").style.display = "none";
  })
  .catch(err => console.error("Error:", err));
}

function backToTeacher() {
  document.getElementById("class-details").style.display = "none";
  document.getElementById("teaching-classes").style.display = "block";
}

function editGrade(enrollmentId, currentGrade) {
    const newGrade = prompt("Enter new grade:", currentGrade);

    if (newGrade === null) return;

    fetch("/update-grade", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            enrollment_id: enrollmentId,
            grade: Number(newGrade)
        }),
        credentials: "include"
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            alert("Grade updated.");
            loadClassDetails(data.class_id);
        } else {
            alert("Error: " + data.message);
        }
    })
    .catch(err => console.error("Update error:", err));
}

document.addEventListener("DOMContentLoaded", () => {
    if (USER_ROLE === "student") {
        document.getElementById("student-section").style.display = "block";
        document.getElementById("teacher-section").style.display = "none";
    } else {
        document.getElementById("student-section").style.display = "none";
        document.getElementById("teacher-section").style.display = "block";
    }
});