//  Making Toast to show error messages
  document.addEventListener("DOMContentLoaded", function(){
    const toastElList = [].slice.call(document.querySelectorAll('.toast'))
    const toastList = toastElList.map(function(toastEl) {
      return new bootstrap.Toast(toastEl, { delay: 5000 });
    });
    toastList.forEach(toast => toast.show());
  });

  // Adding Role In Admin 
  document.getElementById()



