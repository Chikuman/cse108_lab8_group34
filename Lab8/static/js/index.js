function showTab(tab) {
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

document.addEventListener("DOMContentLoaded", () => {
    if (USER_ROLE === "student") {
        document.getElementById("student-section").style.display = "block";
        document.getElementById("teacher-section").style.display = "none";
    } else {
        document.getElementById("student-section").style.display = "none";
        document.getElementById("teacher-section").style.display = "block";
    }
});