// Get references to the card and form container elements
const addProjectCard = document.getElementById('addProjectCard');
const projectFormContainer = document.getElementById('projectFormContainer');

// Add a click event listener to the card
addProjectCard.addEventListener('click', () => {
    // Toggle the display of the form container
    if (projectFormContainer.style.display === 'none' || projectFormContainer.style.display === '') {
        projectFormContainer.style.display = 'block';
    } else {
        projectFormContainer.style.display = 'none';
    }
});
