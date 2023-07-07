/* Project specific Javascript goes here. */
function search_for_artist(term, artists) {
  // artists is an array of arrays [[fullname, answer]], term is a string
  // find all items in list that contain term
  // sort by occurrence of term in item
  // (items where term occurs earlier are first)
  const filtered = artists.filter(
    (s) => s[0].toLowerCase().search(term.toLowerCase()) > -1
  );
  return filtered.length > 0
    ? filtered.sort((s) => s[0].toLowerCase().search(term.toLowerCase()))
    : [];
}

function autocomplete(inp, arr) {
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function (e) {
    var a, b, i, val;
    val = this.value;

    /*close any already open lists of autocompleted values*/
    closeAllLists();
    if (!val) {
      return false;
    }
    currentFocus = -1;
    let matches = search_for_artist(val, arr);
    /*create a DIV element that will contain the items (values):*/
    a = document.createElement("DIV");
    a.setAttribute("id", this.id + "autocomplete-list");
    a.setAttribute("class", "autocomplete-items");
    /*append the DIV element as a child of the autocomplete container:*/
    this.parentNode.appendChild(a);
    // Display each match below the input field
    console.log(matches);
    matches.map((m) => {
      b = document.createElement("div");
      // highlight occurrences of val in match, but retain case of match
      let sub = new RegExp(val, "gi");
      res = m[0].replace(sub, (x) => `<strong>${x}</strong>`);
      b.innerHTML = res;
      b.innerHTML += `<input type='hidden' value='${JSON.stringify(m)}'>`;
      b.addEventListener("click", function (e) {
        // add match to the input when clicked
        selected = JSON.parse(this.getElementsByTagName("input")[0].value);
        inp.value = selected[0]; // artist full name
        answer_input = document.getElementById("id_artist_answer");
        answer_input.value = selected[1]; // artist answer
        closeAllLists();
      });
      a.appendChild(b);
    });
    // automatically select the first choice
    x = document.getElementById(this.id + "autocomplete-list");
    console.log(x);
    if (x) {
      ac_list = x.getElementsByTagName("div");
      currentFocus = 0;
      addActive(ac_list);
    }
  });

  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function (e) {
    let x = document.getElementById(this.id + "autocomplete-list");
    if (x) x = x.getElementsByTagName("div");
    if (e.code === "ArrowDown") {
      /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
      currentFocus++;
      /*and and make the current item more visible:*/
      addActive(x);
    } else if (e.code === "ArrowUp") {
      //up
      /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
      currentFocus--;
      /*and and make the current item more visible:*/
      addActive(x);
    } else if (e.code === "Enter") {
      /*If the ENTER key is pressed, prevent the form from being submitted,*/
      e.preventDefault();
      if (currentFocus > -1) {
        /*and simulate a click on the "active" item:*/
        if (x) x[currentFocus].click();
      }
    }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = x.length - 1;
    /*add class "autocomplete-active":*/
    if (x.length > 0) {
      x[currentFocus].classList.add("autocomplete-active");
    }
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*Close all lists when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
    closeAllLists(e.target);
  });
}

const ale = document.getElementById("artist_list");
if (ale) {
  const artist_list = JSON.parse(ale.textContent);
  artist_div = document.getElementById("div_id_artist_fullname");
  artist_div.classList.add("autocomplete");
  artist_input = document.getElementById("id_artist_fullname");
  autocomplete(artist_input, artist_list);
}

const APPROVAL_OPTIONS = {
  rejected: 0,
  unset: 1,
  approved: 2,
};

function updateCard(dp_id, approved) {
  let col = document.getElementById(`dp_col_${dp_id}`);
  switch (approved) {
    case APPROVAL_OPTIONS.rejected:
      col.innerHTML = `<p>Moved to rejected</p>`;
      break;
    case APPROVAL_OPTIONS.unset:
      col.innerHTML = `<p>Moved to unset</p>`;
      break;
    case APPROVAL_OPTIONS.approved:
      col.innerHTML = `<p>Moved to approved</p>`;
      break;
    default:
      break;
  }
}

function setApproved(dp_id, approved) {
  const csrftoken = document.querySelector(
    "input[name=csrfmiddlewaretoken]"
  ).value;
  const data = {
    detailpage: dp_id,
    approved: approved,
  };

  // define APPROVAL_ENDPOINT with inline script tag on page using url template tag
  fetch(APPROVAL_ENDPOINT, {
    method: "post",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
      Accept: "application/json",
      "X-Requested-With": "XMLHttpRequest",
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      console.log(response);
      return response.json();
    })
    .then((data) => {
      console.log(data);
      if (data.status === "success") {
        console.log("success");
        updateCard(dp_id, approved);
      } else {
        console.log(data.message);
      }
    })
    .catch((error) => {
      console.log(error);
    });
}

function showEnlarged(title, origUrl) {
  const modal = new bootstrap.Modal(document.getElementById("enlargedModal"));
  const enlargedImage = document.getElementById("enlargedImage");
  enlargedImage.setAttribute("src", origUrl);
  const enlargedTitle = document.getElementById("enlargedModalTitle");
  enlargedTitle.textContent = title;
  modal.show();
  console.log(origUrl);
}

function showApprovalForm(dp_id, dp_title, dp_artist_fullname, imageUrl) {
  const modal = new bootstrap.Modal(document.getElementById("approvalModal"));
  const dp_id_input = document.getElementById("id_detailpage")
  const dp_artist_fullname_input = document.getElementById("id_artist_fullname")
  modal.show();
}
