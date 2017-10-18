$(function(){

  // initial card add
  $('.card').clone().insertBefore('#plus-button').css('display','inline-block');

  //
  $('#plus-button').click(function(){
    // does a bunch, clones the template guy, then makes it noe longer invisible
    $('.card').first().clone().insertBefore(this).css('display','inline-block')

    // this is close functionality, has to be added here because each new card needs its own close mechanism
    $('.close').click(function(){
      $(this).parent().parent().remove()
    })

  })

})
