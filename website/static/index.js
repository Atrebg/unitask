//take the noteid we passed it send a post request to the delete-note endpoint
//quando riceve una risposta ricarica la pagina window.location.href

function deleteOffer(offerId) {
  fetch("/delete-offer", {
    method: "POST",
    body: JSON.stringify({ offerId: offerId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}