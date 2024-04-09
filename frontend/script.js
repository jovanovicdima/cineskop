const allTags = new Set();
const selectedTags = new Set();
let startDate = endDate = NaN;
let startTime = endTime = "";
let movieList;

function selectTag() {
	if(selectedTags.has(this.innerText)) {
		this.classList.remove("accentButton");
		this.classList.add("defaultButton");
		selectedTags.delete(this.innerText);
	}
	else {
		this.classList.add("accentButton");
		this.classList.remove("defaultButton");
		selectedTags.add(this.innerText);
	}
}

function setGenres() {
	const genres = document.getElementById("genres");
	const phoneGenres = document.getElementById("phoneGenres");
	genres.innerHTML = "";
	phoneGenres.innerHTML = "";
	allTags.forEach(element => {
		const tag = document.createElement("div");
		tag.classList.add("defaultButton");
		tag.classList.add("genre");
		tag.innerText = element;
		tag.onclick = selectTag;
		let copy = tag.cloneNode(true);
		copy.classList.add("button");
		copy.onclick = selectTag;
		genres.appendChild(copy);
		tag.classList.add("smallButton");
		phoneGenres.appendChild(tag);
	});
}

async function getMovies() {
	const items = await fetch("http://localhost:3000");
	movieList = await items.json();
	for(let i = 0; i < movieList.length; i++) {
		movieList[i].originaltitle = movieList[i].originaltitle.replaceAll(/[^a-zA-Z0-9]/g, '\\$&');
		movieList[i].genre = movieList[i].genre.split(", ")
		for(let j = 0; j < movieList[i].genre.length; j++) {
			movieList[i].genre[j] = movieList[i].genre[j].charAt(0).toUpperCase() + movieList[i].genre[j].slice(1);
			allTags.add(movieList[i].genre[j]);
		}
    for(let j = 0; j < movieList[i].projectiontimes.length; j++) {
      movieList[i].projectiontimes[j] = new Date(movieList[i].projectiontimes[j]);
    }
  }
	movieList.sort((a, b) => {return a.id - b.id});
	
	setGenres()
	printMovies();
}

function printMovies() {
	const movies = document.getElementById("movies");
	movies.innerHTML = "";

	for(let i = 0; i < movieList.length; i++) {
		let hasTag = false;	
		if(selectedTags.size != 0) {
			movieList[i].genre.forEach(element => {
				if(selectedTags.has(element)) {
					hasTag = true;
				}
			});
			if(hasTag == false) continue;
		}
    
    if(!isNaN(startDate)) {
      let hasDate = false;
      for(let date of movieList[i].projectiontimes) {
        if(startDate <= date) hasDate = true;
      }
      if(hasDate == false) continue;
    }

    if(!isNaN(endDate)) {
      let hasDate = false;
      for(let date of movieList[i].projectiontimes) {
        if(endDate >= date) hasDate = true;
      }
      if(hasDate == false) continue;
    }

    if(startTime.length != 0) {
      let hasTime = false;
      for(let time of movieList[i].projectiontimes) {
        time = time.toLocaleTimeString('sr-RS');
        if(startTime <= time) hasTime = true;
      }
      if(hasTime == false) continue;
    }

    if(endTime.length != 0) {
      let hasTime = false;
      for(let time of movieList[i].projectiontimes) {
        time = time.toLocaleTimeString('sr-RS');
        if(endTime >= time) hasTime = true;
      }
      if(hasTime == false) continue;
    }

		const movie = document.createElement("a");
		movie.href = `./movie.html?id=${movieList[i].id}`;

		const image = document.createElement("div");
		
		image.style.background = `url(images/${movieList[i].originaltitle}.jpeg)`
		image.style.backgroundSize = "100% 100%";
		image.classList.add("image");
		movie.appendChild(image);

		const movieName = document.createElement("p");
		movieName.classList.add("name");
		movieName.innerText = movieList[i].title;
		movie.appendChild(movieName);
	
		const	tags = document.createElement("div");
		tags.classList.add("tags");

		for(let j = 0; j < movieList[i].genre.length; j++) {
			const genre = document.createElement("div");
			genre.classList.add("smallButton");
			genre.classList.add("defaultButton");
			genre.innerText = movieList[i].genre[j];
			allTags.add(movieList[i].genre[j]);
			tags.appendChild(genre);
		}
		movie.appendChild(tags);
		movies.appendChild(movie);
	}

  const filterButton = document.getElementById("filterButton").firstElementChild;
  if(selectedTags.size == 0 && isNaN(startDate) && isNaN(endDate) && startTime.length == 0 && endTime.length == 0) {
    filterButton.classList.add("defaultButton");
    filterButton.classList.remove("accentButton");
  }
  else {
    filterButton.classList.add("accentButton");
    filterButton.classList.remove("defaultButton");
  }
}

getMovies();

function toggleFilter() {
  const dim = document.getElementById("dim");
  const filter = document.getElementById("filter");

  dim.classList.toggle("hidden");
  filter.classList.toggle("hidden");

  if(filter.className.includes("hidden")) {
    startDate = new Date(Date.parse(document.getElementById("startDate").value + "T00:00"));
    endDate = new Date(Date.parse(document.getElementById("endDate").value + "T00:00"));
    endDate.setDate(endDate.getDate() + 1);

    startTime = document.getElementById("startTime").value;
    if(startTime != "") {
      startTime += ":00";
    }

    endTime = document.getElementById("endTime").value;
    if(endTime != "") {
      endTime += ":00";
    }

	  printMovies();
  }
}

function resetFilters(filter) {
  switch(filter) {
    case "genre":
      selectedTags.clear();
      const tags = document.getElementsByClassName("genre");
      for(let tag of tags) {
        tag.classList.remove("accentButton");
        tag.classList.add("defaultButton");
      }
      break;
    case "date":
      const dates = document.querySelectorAll("input[type='date']");
      for(let date of dates) {
        date.value = "";
        date.max = "";
        date.min = "";
      }
      startDate = NaN;
      endDate = NaN;
      break;
    case "time":
      const times = document.querySelectorAll("input[type='time']");
      for(let time of times) {
        time.value = "";
        time.max = "";
        time.min = "";
      }
      startTime = "";
      endTime = "";
      break;
  }
}

function onChange(value) {
  switch(value) {
    case "startDate":
      document.getElementById("endDate").min = document.getElementById("startDate").value;
      break;
    case "endDate":
      document.getElementById("startDate").max = document.getElementById("endDate").value;
      break;
    case "startTime":
      document.getElementById("startTime").max = document.getElementById("endTime").value;
      break;
    case "endTime":
      document.getElementById("endTime").min = document.getElementById("startTime").value;
      break;
  }
}
