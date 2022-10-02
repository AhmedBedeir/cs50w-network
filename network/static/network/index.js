document.addEventListener('DOMContentLoaded', () => {
  const getLoves = document.querySelectorAll('.love').forEach((item) => {
    item.addEventListener('click', function () {
      updateLoves(this.parentElement.id);
    });
  });
  // console.log(getLoves)
});

function updateLoves(postId) {
  console.log(postId);
  console.log(typeof postId);
  fetch(`love/${postId}`)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      let numberLikes = document.getElementById(`countLikes-${postId}`);
      let valNumLikes = +numberLikes.innerHTML;
      if (data.type === 'added') {
        valNumLikes++;
        numberLikes.innerHTML = valNumLikes;
        numberLikes.parentElement.classList.remove('btn-outline-danger');
        numberLikes.parentElement.classList.add('btn-danger');
      }
      if (data.type === 'deleted' && valNumLikes > 0) {
        valNumLikes--;
        numberLikes.innerHTML = valNumLikes;
        numberLikes.parentElement.classList.add('btn-outline-danger');
        numberLikes.parentElement.classList.remove('btn-danger');
      }
      console.log(numberLikes.parentElement.parentElement);
    });
}

document.querySelectorAll('.edit').forEach((item) => {
  item.addEventListener('click', () => {
    document.querySelector('.btnPost').style.display = 'none';
    const update = `<button class="btn updatePost btn-primary"/>Save</button>`;
    const formPost = document.querySelector('.form-post');
    formPost.innerHTML += update;
    const areaPost = document.getElementById('getPost');
    areaPost.focus();
    areaPost.value = document.getElementById(
      `content-${item.parentElement.id}`
    ).innerHTML;
    document.querySelectorAll('.updatePost').forEach((elem) => {
      elem.addEventListener('click', (e) => {
        console.log('Hello...');
        e.preventDefault();
        const newContent = document.getElementById('getPost').value;
        fetch(`edit/${item.parentElement.id}`, {
          method: 'PUT',
          body: JSON.stringify({
            content: newContent,
          }),
          // csrfmiddlewaretoken: '{{ csrf_token }}',
        })
          .then((response) => response.json())
          .then((data) => {
            let message = '';
            if (data.message === 'updated') {
              document.getElementById(
                `content-${item.parentElement.id}`
              ).innerHTML = newContent;
              message = 'Updated Successfully ^_^';
              document.querySelectorAll('.updatePost').forEach(elem => {
                elem.style.display = 'none';
              })
              document.querySelector('.btnPost').style.display = 'block';
              areaPost.value = '';
            } else {
              message = 'Write Something..!';
              areaPost.focus();
              areaPost.value = document.getElementById(
                `content-${item.parentElement.id}`
              ).innerHTML;
            }
            document.querySelector('.alert').innerHTML = `<h1>${message}</h1>`;
            setTimeout(() => {
              document.querySelector('.alert').innerHTML = '';
            }, 4000);
          });
      });
    });
  });
});
