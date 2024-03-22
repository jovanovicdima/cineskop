const allTags = new Set();
const selectedTags = new Set();
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
	printMovies();
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
	console.log(movieList)
	for(let i = 0; i < movieList.length; i++) {
		movieList[i].originaltitle = movieList[i].originaltitle.replaceAll(/[^a-zA-Z0-9]/g, '\\$&');
		movieList[i].genre = movieList[i].genre.split(", ")
		for(let j = 0; j < movieList[i].genre.length; j++) {
			movieList[i].genre[j] = movieList[i].genre[j].charAt(0).toUpperCase() + movieList[i].genre[j].slice(1);
			allTags.add(movieList[i].genre[j]);
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
		movies.appendChild(movie)
	}
}

getMovies();
