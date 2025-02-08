const rooms = {
    1: { forward: 3, back: 13, left: null, right: 2, image: "/static/images/gallery/room1.jpg" },
    2: { forward: 3, back: 13, left: 1, right: null, image: "/static/images/gallery/room2.jpg" },
    3: { forward: 4, back: null, left: 2, right: 1, image: "/static/images/gallery/room3.jpg" },
    4: { forward: 5, back: 9, left: null, right: null, image: "/static/images/gallery/room4.jpg" },
    5: { forward: 6, back: 9, left: null, right: null, image: "/static/images/gallery/room5.jpg" },
    6: { forward: 8, back: 9, left: null, right: 7, image: "/static/images/gallery/room6.jpg" },
    7: { forward: 8, back: 9, left: 6, right: null, image: "/static/images/gallery/room7.jpg" },
    8: { forward: null, back: null, left: 7, right: 6, image: "/static/images/gallery/room8.jpg" },
    9: { forward: null, back: null, left: null, right: null, image: "/static/images/gallery/room9.jpg" },
    10: { forward: null, back: null, left: null, right: null, image: "/static/images/gallery/room10.jpg" },
    11: { forward: null, back: 13, left: null, right: 12, image: "/static/images/gallery/room11.jpg" },
    12: { forward: null, back: 13, left: 11, right: null, image: "/static/images/gallery/room12.jpg" },
    13: { forward: null, back: null, left: null, right: null, image: "/static/images/gallery/room13.jpg" },
};

const background = document.getElementById("background");
const mapRooms = document.querySelectorAll(".map-room");
const navButtons = {
    up: document.getElementById("up"),
    down: document.getElementById("down"),
    left: document.getElementById("left"),
    right: document.getElementById("right"),
};

let currentRoom = 3;

function updateView() {
    const room = rooms[currentRoom];
    // Log the room and image path for debugging
    console.log(`Current room: ${currentRoom}, Background image: ${room.image}`);
    background.style.backgroundImage = `url('${room.image}')`;
    background.style.backgroundSize = "cover";
    background.style.backgroundPosition = "center";
    mapRooms.forEach((r) => r.classList.remove("current-room"));
    document.querySelector(`.map-room[data-room="${currentRoom}"]`).classList.add("current-room");
    Object.keys(navButtons).forEach((dir) => {
        navButtons[dir].classList.toggle("hidden", !room[dir]);
    });
}

Object.keys(navButtons).forEach((dir) => {
    navButtons[dir].addEventListener("click", () => {
        if (rooms[currentRoom][dir]) {
            currentRoom = rooms[currentRoom][dir];
            updateView();
        }
    });
});

// Initial View
updateView();
