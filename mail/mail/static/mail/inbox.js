document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Enable composing of an email
  document.querySelector('#compose-form').addEventListener('submit', (event) => {
    event.preventDefault();
    send_email();
    return false;
  });


  let archiveButton = document.querySelector('#archiveB');
  let unarchiveButton = document.querySelector('#unarchiveB')
  archiveButton.addEventListener('click', ()=> load_mailbox('inbox'));
  unarchiveButton.addEventListener('click', ()=> load_mailbox('inbox'));

  // By default, load the inbox
  load_mailbox('inbox');
});


function compose_email() {


  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#archiveB').style.display = 'none';
  document.querySelector('#unarchiveB').style.display = 'none';
  document.querySelector('#reply').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}


function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#archiveB').style.display = 'none';
  document.querySelector('#unarchiveB').style.display = 'none';
  document.querySelector('#reply').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Load the mailbox
  console.log(`loading ${mailbox}`);

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails);

    // Display the mails
    emails.forEach((email) => {

      let emDiv = document.createElement('div');
      emDiv.classList.add('card');
      emDiv.classList.add('border-primary');
      let sender = document.createElement('div');
      sender.classList.add('font-weight-bold');
      let subtS = document.createElement('div');
      subtS.classList.add('row');
      let sub = document.createElement('div');
      sub.classList.add('col');
      let tS = document.createElement('div');
      tS.style.fontSize = "12px";
      tS.classList.add('col');
      tS.classList.add('text-right');
      sender.textContent = email.sender;
      sub.textContent = email.subject;
      tS.textContent = email.timestamp;
      subtS.appendChild(sub);
      subtS.appendChild(tS);
      emDiv.appendChild(sender);
      emDiv.appendChild(subtS);

      // Change background color of the div if the email is read
      if (email.read === true) {
        emDiv.style.backgroundColor = "gray";
      }

      // Take the user to the email, if clicked on the div that is just created
      emDiv.addEventListener('click', ()=> fetch_email(email.id));

      document.querySelector('#emails-view').appendChild(emDiv);

    });
  });

}


function send_email() {

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
      console.log(result);
  });

  load_mailbox('sent');

}


function fetch_email(id) {

  mail = document.querySelector('#email-view');
  mail.textContent = '';

  // Show email view and hide other views
  mail.style.display = 'block';
  document.querySelector('#archiveB').style.display = 'block';
  document.querySelector('#unarchiveB').style.display = 'block';
  document.querySelector('#reply').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Fetch the email
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);

    let sender = document.createElement('div');
    let recipients = document.createElement('div');
    let subject = document.createElement('div');
    let timestamp = document.createElement('div');
    let body = document.createElement('div');
    let header = document.createElement('div');

    sender.innerHTML = `<b>From:</b> ${email.sender}`;
    sender.classList.add('card-subtitle');
    recipients.innerHTML = `<b>To:</b> ${email.recipients}`;
    recipients.classList.add('card-subtitle');
    subject.innerHTML = `<b>Subject:</b> ${email.subject}`;
    subject.classList.add('card-title');
    timestamp.innerHTML = `<b>Timestamp:</b> ${email.timestamp}`;
    timestamp.style.fontSize = "12px";
    header.appendChild(sender);
    header.appendChild(recipients);
    header.appendChild(subject);
    header.appendChild(timestamp);
    header.classList.add('card-header');

    body.textContent = email.body;
    body.classList.add('card-body');

    mail.appendChild(header);
    mail.appendChild(body);

    // Mark as read
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    })

    // Enable Archive-Unarchive buttons accordingly
    if (document.querySelector('h2').textContent == email.sender) {
      document.querySelector('#archiveB').style.display = 'none';
      document.querySelector('#unarchiveB').style.display = 'none';
      document.querySelector('#reply').style.display = 'none';
      return;
    }

    let archiveButton = document.querySelector('#archiveB');
    let unarchiveButton = document.querySelector('#unarchiveB');
    if (!email.archived) {
      archiveButton.style.display = 'block';
      unarchiveButton.style.display = 'none';
    } else {
      archiveButton.style.display = 'none';
      unarchiveButton.style.display = 'block';
    }

    archiveButton.addEventListener('click', ()=> archive(email.id));
    unarchiveButton.addEventListener('click', ()=> unarchive(email.id));

    // Enable reply button
    document.querySelector('#reply').addEventListener('click', ()=> reply(email.id));

  });
}


function archive(id) {

  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: true
    })
  });
}

function unarchive(id) {

  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: false
    })
  })
}


function reply(id) {
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    recipients = email.sender;
    if (!email.subject.startsWith("Re:")) {
      subject = "Re: "+ email.subject;
    }
    body = `On ${email.timestamp} ${recipients} wrote: ` + email.body;

    compose_email();
    document.querySelector('#compose-recipients').value = recipients;
    document.querySelector('#compose-subject').value = subject;
    document.querySelector('#compose-body').value = body;
  })
}