// Get references to the card and form container elements
const addProjectCard = document.getElementById('addProjectCard');
const projectFormContainer = document.getElementById('projectFormContainer');
const addcertficates = document.getElementById('addcertficates');
const certificatesFormContainer = document.getElementById('certificatesFormContainer');
const addlanguages = document.getElementById('addlanguages');
const languagesFormContainer = document.getElementById('languagesFormContainer');
// Add a click event listener to the card
addProjectCard.addEventListener('click', () => {
    // Toggle the display of the form container
    if (projectFormContainer.style.display === 'none' || projectFormContainer.style.display === '') {
        projectFormContainer.style.display = 'block';
    } else {
        projectFormContainer.style.display = 'none';
    }
});

// toggle certificates
addcertficates.addEventListener('click',() => {
    if (certificatesFormContainer.style.display === 'none' || certificatesFormContainer.style.display === ''){
        certificatesFormContainer.style.display = 'block';
    } else{
        certificatesFormContainer.style.display = 'none'
    }
});

// languages known
addlanguages.addEventListener('click',() => {
    if (languagesFormContainer.style.display === 'none' || languagesFormContainer.style.display === ''){
        languagesFormContainer.style.display = 'block';
    } else{
        languagesFormContainer.style.display = 'none'
    }
});
