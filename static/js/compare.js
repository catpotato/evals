$(function(){

  $('#plus-button').click(function(){
    $('.card').first().clone().insertBefore(this)
    
    $('.close').click(function(){
      console.log('clicky')
      $(this).parent().parent().remove()
    })

  })




})
