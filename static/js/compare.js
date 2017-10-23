$(function(){
  // initial card add
  add_card();

  $('#plus-button').click(function(){
    //console.log('hey')
    add_card();
    // this is submit functionality, needs to be added here for the same reason above
  })

})

function get_card($selector) {
  return $selector.closest('.card');
}

function get_id($selector) {
  var this_id = $selector[0].id;
  return parseInt(this_id.substring(this_id.indexOf('-') + 1));
}

function add_card(){
  // does a bunch, clones the template guy, then makes it no longer invisible
  var $new_card = $('.card').first().clone();
  var id_num = get_id($('.card').last()) + 1;
  $new_card.attr("id", "card-" + id_num);
  $new_card.insertBefore($('#plus-button')).css('display','inline-block')

  // this is close functionality, has to be added here because each new card needs its own close mechanism
  $('.close').click(function(){
    var id_num = get_id(get_card($(this)));
    $("#card-" + id_num).remove();
  });
}
