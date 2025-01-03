function handleStudentSubmission(event) {
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
      const modalHeader = document.querySelector('#new_student_modal .modal-header');
      const alertDiv = document.createElement('div');
      alertDiv.className = 'alert alert-warning alert-dismissible fade show';
      alertDiv.innerHTML = `
        Error adding student
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      `;
      modalHeader.insertAdjacentElement('afterend', alertDiv);
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

document.addEventListener('click', function(e) {
  if (e.target && e.target.classList.contains('btn-close')) {
    const alert = e.target.closest('.alert');
    if (alert) {
      alert.remove();
    }
  }
});

function deleteStudent(id_number) {
  if (confirm('Are you sure you want to delete this student?')) {
    fetch(`/delete-student/${id_number}`, {
      method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        location.reload();
      } else {
        alert('Error deleting student');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Error deleting student');
    });
  }
}

function handleEditSubmission(event, id_number) {
  event.preventDefault();
  
  const form = event.target;
  const formData = new FormData(form);
  
  fetch(`/edit-student/${id_number}`, {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      const modal = bootstrap.Modal.getInstance(document.getElementById(`edit_student_modal_${id_number}`));
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

document.getElementById('studentInput').addEventListener('input', function(e) {
  const searchText = e.target.value.toLowerCase();
  const rows = document.querySelectorAll('tbody tr');
  
  rows.forEach(row => {
      const text = row.textContent.toLowerCase();
      row.style.display = text.includes(searchText) ? '' : 'none';
  });
});

document.querySelector('form').addEventListener('submit', function(e) {
  e.preventDefault();
});