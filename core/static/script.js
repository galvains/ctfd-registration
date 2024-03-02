function addParticipant() {
    if (document.getElementsByClassName('participant').length >= 4) {
        alert('Вы уже добавили максимум участников!')
        return;
    }

    const participantsSection = document.getElementById('participantsSection');
    const participantDiv = document.createElement('div');
    participantDiv.className = 'participant';

    const participantFields = new Map();
    participantFields.set('_full_name', 'ФИО участника:');
    participantFields.set('_email', 'Email участника:');

    participantDiv.appendChild(document.createElement('br'));
    participantFields.forEach((value, field) => {
        const label = document.createElement('label');
        label.htmlFor = `participant{field}`;
        label.textContent = `${value}`;

        const input = document.createElement('input');

        if (field == '_full_name'){
            input.type = 'text';
        }
        else {
            input.type = 'email';
        }

        input.id = `participant${field}`;
        input.name = `participant${field}[]`;
        input.required = true;

        participantDiv.appendChild(label);
        participantDiv.appendChild(document.createElement('br'));
        participantDiv.appendChild(input);
    });

    const removeLink = document.createElement('span');
    removeLink.className = 'remove-participant';
    removeLink.textContent = 'Удалить участника';
    removeLink.onclick = function() { removeParticipant(this); };

    participantDiv.appendChild(document.createElement('br'));
    participantDiv.appendChild(removeLink);
    participantsSection.appendChild(participantDiv);
}

function removeParticipant(element) {
    const participantDiv = element.parentNode;
    const participantsSection = document.getElementById('participantsSection');
    participantsSection.removeChild(participantDiv);
}
