$(document).ready(function() {
  function query(page) {
    document.queryForm.pageNo.value = page+"";
    document.queryForm.submit();
  }
});
