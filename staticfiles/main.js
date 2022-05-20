// Close alerts
setTimeout(() => {
    $('.alert').alert('close');
}, 5000);


// Stars for rating
function starsReview(stars, input) {
  let input_initial_value = input.value;
  stars.forEach((star, index) => {
    if (index >= parseInt(input_initial_value)) {
      star.innerText = '★';
    } else {
      star.innerText = '☆';
    }
  })
}

if (document.querySelectorAll(".star").length > 0) {
  const stars = document.querySelectorAll(".star");
  const input = document.querySelector("#id_rating");
  starsReview(stars, input);
  stars.forEach((star, index) => {
    
  })
}