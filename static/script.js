// for showing and hiding doctor fields in registration form
function showDoctorFields() {
  const role = document.querySelector('select[name="role"]').value;
  const doctorFields = document.getElementById("doctor-fields");
  doctorFields.style.display = role === "doctor" ? "block" : "none";
}

document.addEventListener("DOMContentLoaded", function () {
  showDoctorFields();
});

document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      //for redirecting to stripe
      this.submit();
    });
  }
});
