function handleStudentSubmission(event) {
  event.preventDefault();
  
  const form = event.target;
  const formData = new FormData(form);
  
  fetch(window.location.href, {
    method: 'POST',
    body: formData
  })
  .then(response => response.text())
  .then(html => {
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = html;
    const flashMessages = tempDiv.getElementsByClassName('alert');
    
    if (flashMessages.length > 0) {
      form.reset();
      
      const modalFlashContainer = document.querySelector('#new_student_modal .modal-header');
      const currentFlashMessages = Array.from(flashMessages).map(flash => flash.outerHTML).join('');
      
      const existingFlashes = modalFlashContainer.querySelectorAll('.alert');
      existingFlashes.forEach(flash => flash.remove());
      
      modalFlashContainer.insertAdjacentHTML('afterend', currentFlashMessages);
    } else {
      const modal = bootstrap.Modal.getInstance(document.getElementById('new_student_modal'));
      modal.hide();
      location.reload();
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