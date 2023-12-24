// SIDEBAR
function toggleActiveLink(element) {
  const links = document.querySelectorAll('.js-sidebar-link');
  console.log(links);
  // remove active class from all links
  links.forEach(link => link.classList.remove('active'));
  console.log(links);
  // add active class to the clicked link
  element.classList.add('active');
}

// MAIN
function removeMessage() {
  const flashMessages = document.querySelector('.flash-messages');
  flashMessages.remove();
}

// MANAGE DATA
function openModal(rowData) {
  const row = JSON.parse(rowData);
  const modal = document.querySelector('.js-modal');
  console.log(row);
  modal.style.display = 'block';
}

function closeModal() {
  const modal = document.querySelector('.js-modal');
  // change display to none
  modal.style.display = 'none';
}