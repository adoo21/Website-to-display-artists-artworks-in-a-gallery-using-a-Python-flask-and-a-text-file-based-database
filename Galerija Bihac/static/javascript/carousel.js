// Select carousel elements
const carouselTrack = document.querySelector('.carousel-track');
const slides = Array.from(carouselTrack.children);
const dots = document.querySelectorAll('.dot');
const slideWidth = slides[0].getBoundingClientRect().width;

let currentIndex = 0;

// Function to update the active dot
function updateDots(index) {
    dots.forEach((dot, i) => {
        dot.classList.toggle('active', i === index);
    });
}

// Function to move to the next slide
function moveToNextSlide() {
    currentIndex = (currentIndex + 1) % slides.length;
    const amountToMove = -slideWidth * currentIndex;
    carouselTrack.style.transform = `translateX(${amountToMove}px)`;
    updateDots(currentIndex);
}

// Set the carousel to scroll every 5 seconds
setInterval(moveToNextSlide, 5000);

// Add click functionality to dots
dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
        currentIndex = index;
        const amountToMove = -slideWidth * currentIndex;
        carouselTrack.style.transform = `translateX(${amountToMove}px)`;
        updateDots(currentIndex);
    });
});
