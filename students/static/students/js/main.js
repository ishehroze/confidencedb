(function () {
  $(document).ready(function () {
    $('#roll-field').val("");
    $('#roll-search').click(function () {
      var url = "/students/" + $('#roll-field').val();
      window.location.href = url;
    });
  });
})();
