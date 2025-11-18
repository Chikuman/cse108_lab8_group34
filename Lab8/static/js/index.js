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

function updateGrade(enrollmentId) {
  const newGrade = prompt("Enter new grade (e.g. A, B+, 90):");
  if (newGrade === null) {
    return; // user cancelled
  }

  fetch("/update_grade", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      enrollment_id: enrollmentId,
      grade: newGrade,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "ok") {
        const cell = document.getElementById(`grade-${enrollmentId}`);
        if (cell) {
          cell.textContent = data.grade || "N/A";
        }
      } else {
        alert(data.error || "Error updating grade.");
      }
    })
    .catch((err) => {
      console.error("Error updating grade:", err);
      alert("Error updating grade.");
    });
}