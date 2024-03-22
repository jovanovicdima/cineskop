const parser = new URL(document.URL)
const id = parser.searchParams.get("id");
const dates = new Set();
let movie;

async function getMovie() {
		const items = await fetch(`http://localhost:3000/movie/${id}`);
	movie = (await items.json())[0];
  console.log(movie);
	movie.genre = movie.genre.split(", ");
	for(let i = 0; i < movie.genre.length; i++) {
		movie.genre[i] = movie.genre[i].charAt(0).toUpperCase() + movie.genre[i].slice(1);
	}

	movie.projections = await fetch(`http://localhost:3000/projection/${id}`).then(x => x.json());
	for(let i = 0; i < movie.projections.length; i++) {
		movie.projections[i].time = new Date(movie.projections[i].time);
	}

	console.log(movie.originaltitle);

}

function showMovie() {
	const titleTag = document.getElementById("title");
	const title = document.createElement("h1");
	title.innerHTML = movie.title;
	titleTag.appendChild(title);
	const originalTitle = document.createElement("p");
	originalTitle.innerHTML = movie.originaltitle;
	titleTag.appendChild(originalTitle);

	const image = document.getElementById("image");
	const path = movie.originaltitle.replaceAll(/[^a-zA-Z0-9]/g, '\\$&');
	console.log(path);
	image.style.background = `url(images/${path}.jpeg)`;
	image.style.backgroundSize = "100% 100%";

	const runtime = document.getElementById("runtime");
	runtime.innerHTML = movie.runningtime + " min";

	const director = document.getElementById("director");
	director.innerHTML = movie.director;

	const origin = document.getElementById("origin");
	origin.innerHTML = movie.countryoforigin;

	const cast = document.getElementById("cast");
  if(movie.cast != "") {
    cast.innerHTML = movie.cast;
  } else {
    cast.parentNode.innerHTML = "";
  }

	const genres = document.getElementById("genres");
	for(let genre of movie.genre) {
		const div = document.createElement("div");
		div.classList.add("smallButton");
		div.classList.add("defaultButton");
		div.innerHTML = genre;
		genres.appendChild(div);
	}

	const synopsis = document.getElementById("synopsis");
	synopsis.innerHTML = movie.synopsis;
	
	const trailer = document.getElementById("trailer");
	if(movie.trailerlink != "") {
		const iframe = document.createElement("iframe");
		iframe.src = movie.trailerlink;
		iframe.allowFullscreen = true;
		trailer.appendChild(iframe);
	}
	else {
		trailer.style.display = "none";
	}

	const times = document.getElementById("dates");
	for(let time of movie.projections) {
		dates.add(time.time.toLocaleDateString("sr").replaceAll(" ", ""));
	}
	for(let item of dates) {
		const date = document.createElement("div");
		date.onclick = onClick;
		date.classList.add("button");
		date.classList.add("defaultButton");
		date.classList.add("date");
		date.innerHTML = item.replaceAll(" ", "");
		times.appendChild(date);
	}

	const firstDate = dates.values().next().value;
	showProjections(firstDate);

}

function showProjections(targetDate) {
	const projections = document.getElementById("projections");
	projections.innerHTML = "";

	for(let button of document.getElementsByClassName("date")) {
		if(button.innerHTML == targetDate) {
			button.classList.remove("defaultButton");
			button.classList.add("accentButton");
		}
		else {
			button.classList.remove("accentButton");
			button.classList.add("defaultButton");
		}
	}
	
	for(let item of movie.projections) {
		if(item.time.toLocaleDateString("sr").replaceAll(" ", "") == targetDate) {
			const projection = document.createElement("a");
			projection.href = item.link;
			projection.classList.add("projection");
			projection.classList.add("defaultButton");

			const time = document.createElement("p");
			time.innerHTML = item.time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
			projection.appendChild(time);

			const cinema = document.createElement("div");
			cinema.classList.add("cinema");
			const movieName = document.createElement("p");
			movieName.classList.add("movieName"); // TODO: - NEED TO CHANGE
			movieName.innerHTML = item.name;
			cinema.appendChild(movieName);
			const movieAuditorium = document.createElement("p");
			movieAuditorium.classList.add("movieAuditorium");
			movieAuditorium.innerText = `${item.auditorium} (${item.projectiontype})`;
			cinema.appendChild(movieAuditorium);
			projection.appendChild(cinema);

			const price = document.createElement("p");
			price.innerText = item.price + " RSD";
			projection.appendChild(price);

			projections.appendChild(projection);
		}
	}

}

function onClick() {
	showProjections(this.innerText);
}

try {
	await getMovie();
	showMovie();
}
catch(e) {
	console.log(e);
}
