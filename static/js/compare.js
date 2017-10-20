$(function(){

  // initial card add
  add_card();

  $('#plus-button').click(function(){
    //console.log('hey')
    add_card()




    // this is submit functionality, needs to be added here for the same reason above



  })

})

function add_card(){

  // does a bunch, clones the template guy, then makes it noe longer invisible
  $('.card').first().clone().insertBefore($('#plus-button')).css('display','inline-block')

  // this is close functionality, has to be added here because each new card needs its own close mechanism
  $('.close').click(function(){
    $(this).parent().parent().remove()
  })

  $('.submit').last().click(function(){
    console.log('ive been clicked')
    form = $(this).parent()
    //console.log($(this).parent().children('input[name="department"]').val())

    $.getJSON($SCRIPT_ROOT + '/_send_query', {
      department: form.children('input[name="department"]').val(),
      course: form.children('input[name="course"]').val(),
      professor: form.children('input[name="professor"]').val()
    }, function(data) {
      console.log(data.course);
    })

  })


}
