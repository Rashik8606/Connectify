function toggleSearch() {
    const searchBar = document.getElementById('search-bar');
    searchBar.classList.toggle('hidden');
}

document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.like-btn').forEach(button => {
    button.addEventListener('click', function (e) {
      e.preventDefault();

      const postId = this.getAttribute('data-post-id');
      const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

      fetch(`/like/${postId}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken,
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(response => response.json())
      .then(data => {
        const icon = this.querySelector('i');
        const countSpan = this.querySelector('.like-count');

        countSpan.textContent = data.like_count;

        if (data.liked) {
          icon.classList.add('liked');
        } else {
          icon.classList.remove('liked');
        }
      });
    });
  });
});


  function toggleCommentBox(postId) {
    const commentBox = document.getElementById(`comment-box-${postId}`);
    if (commentBox.style.display === "none") {
        commentBox.style.display = "block";
    } else {
        commentBox.style.display = "none";
    }
}

function toggleCommentSection(postId) {
  const section = document.getElementById(`comment-section-${postId}`);
  section.style.display = section.style.display === 'none' || section.style.display === '' ? 'block' : 'none';
}


function submitComment(event, postId) {
  event.preventDefault();

  const form = document.getElementById(`comment-form-${postId}`);
  const formData = new FormData(form);

  fetch(`/comment/${postId}/`, {
      method: 'POST',
      headers: {
          'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
      },
      body: formData,
  })
  .then(response => response.json())
  .then(data => {
      console.log("Response data:", data);
      if (data.success) {
          const commentsDiv = document.getElementById(`comment-list-${postId}`);
          const newComment = document.createElement('p');
          newComment.innerHTML = `<strong>${data.username}:</strong> ${data.text}`;
          commentsDiv.appendChild(newComment);
          form.reset();
      } else {
          alert(data.error || "Failed to submit comment.");
      }
  })
  .catch(error => {
      console.error("Error:", error);
      alert("Something went wrong while submitting the comment.");
  });
}
