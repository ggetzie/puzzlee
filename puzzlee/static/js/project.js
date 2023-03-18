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

function setDPFlag(endpoint, dp_id, value) {
  const row = document.getElementById(`dp_row_${dp_id}`);
  row.classList.toggle("is_candidate");
  const approved_cb = document.getElementById(`reviewed_dp_${dp_id}`);
  approved_cb.setAttribute("checked", true);
  approved_cb.setAttribute("disabled", true);
}
