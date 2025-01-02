function handleCourseSubmission(event) {
  event.preventDefault();

  const form = event.target;
  const formData = new FormData(form);

  fetch(window.location.href, {
    method: 'POST',
    body: formData
  })
    .then(response => {
      if (response.ok) {
        location.reload();
      } else {
        const modalHeader = document.querySelector('#new_course_modal .modal-header');
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-warning alert-dismissible fade show';
        alertDiv.innerHTML = `
        Error adding course
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      `;
        modalHeader.insertAdjacentElement('afterend', alertDiv);
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

document.addEventListener('click', function (e) {
  if (e.target && e.target.classList.contains('btn-close')) {
    const alert = e.target.closest('.alert');
    if (alert) {
      alert.remove();
    }
  }
});

function deleteCourse(course_code) {
  if (confirm('Are you sure you want to delete this course?')) {
    fetch(`courses/delete-course/${course_code}`, {
      method: 'DELETE',
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          location.reload();
        } else {
          alert('Error deleting course');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        alert('Error deleting course');
      });
  }
}

function handleEditSubmission(event, course_code) {
  event.preventDefault();

  const form = event.target;
  const formData = new FormData(form);

  fetch(`/edit-course/${course_code}`, {
    method: 'POST',
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        const modal = bootstrap.Modal.getInstance(document.getElementById(`edit_course_modal_${course_code}`));
        modal.hide();
        location.reload();
      } else {
        const modalHeader = form.querySelector('.modal-header');
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-warning alert-dismissible fade show';
        alertDiv.innerHTML = `
          ${data.error}
          <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        modalHeader.insertAdjacentElement('afterend', alertDiv);
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

document.getElementById('courseInput').addEventListener('input', function (e) {
  const searchText = e.target.value.toLowerCase();
  const rows = document.querySelectorAll('tbody tr');

  rows.forEach(row => {
    const text = row.textContent.toLowerCase();
    row.style.display = text.includes(searchText) ? '' : 'none';
  });
});

document.querySelector('form').addEventListener('submit', function (e) {
  e.preventDefault();
});