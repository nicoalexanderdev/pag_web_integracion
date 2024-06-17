document.addEventListener('DOMContentLoaded', function() {
  const togglePassword = document.querySelector('#togglePassword');
  const password = document.querySelector('#id_password');
  const togglePasswordIcon = document.querySelector('#togglePasswordIcon');

  togglePassword.addEventListener('click', function() {
      // Toggle the type attribute using getAttribute() and setAttribute()
      const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
      password.setAttribute('type', type);

      // Toggle the icon class
      if (type === 'text') {
          togglePasswordIcon.classList.remove('bi-eye-slash');
          togglePasswordIcon.classList.add('bi-eye');
      } else {
          togglePasswordIcon.classList.remove('bi-eye');
          togglePasswordIcon.classList.add('bi-eye-slash');
      }
  });
});