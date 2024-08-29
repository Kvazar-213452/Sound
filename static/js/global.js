function clos(name) {
  $('#' + name).hide(); 
}

function openModal(name) {
  $('#' + name).show(); 
}

function togglePopup() {
  const popupContainer = document.getElementById('popup-container');
  const isOpen = popupContainer.style.display === 'block';

  if (isOpen) {
    popupContainer.style.top = '-320px'; 
    setTimeout(() => {
      popupContainer.style.display = 'none';
    }, 1000); 
  } else {
    popupContainer.style.display = 'block';
    setTimeout(() => {
      popupContainer.style.top = '20px'; 
    }, 100);

    setTimeout(() => {
      togglePopup();
    }, 5000);
  }
}


function list(name) {
  window.parent.postMessage(name, '*');
} 
