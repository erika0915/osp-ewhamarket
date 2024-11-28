const productName = "{{ data.productName }}";
function showHeart() {
  $.ajax({
    type: 'GET',
    url: '/show_heart/{{ data.productName }}/',
    data: {},
    success: function (response) {
      let my_heart = response['my_heart'];
      if (my_heart['interested'] == 'Y')
      {
        $("#heart").css("color","red");
        $("#heart").attr("onclick","unlike()");
     }
      else
      {
        $("#heart").css("color","grey");
        $("#heart").attr("onclick","like()");
      }
      //alert("showheart!")
  }
  });
}

function like() {
  $.ajax({
  type: 'POST',
  url: '/like/{{data.productName}}/',
  data: {
    interested : "Y"
  },
  success: function (response) {
    alert(response['msg']);
    window.location.reload()
  }
  });
}

function unlike() {
  $.ajax({
    type: 'POST',
    url: '/unlike/{{data.productName}}/',
    data: {
      interested : "N"
    },
  success: function (response) {
    alert(response['msg']);
    window.location.reload()
  }
  });
}
$(document).ready(function () {
  showHeart();
});