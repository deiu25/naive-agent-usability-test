// Formularul "Expediere noua".
const modal = document.getElementById('formExpediere');

function deschideFormular() {
    modal.classList.add('deschis');
}

// X doar ascunde formularul; campurile raman completate pana la salvare.
modal.querySelector('.inchide').addEventListener('click', function () {
    modal.classList.remove('deschis');
});

document.getElementById('butonExpediereNoua').addEventListener('click', deschideFormular);

document.getElementById('expediere').addEventListener('submit', async function (e) {
    e.preventDefault();
    const date = Object.fromEntries(new FormData(this));
    const r = await fetch('/expedieri', { method: 'POST', body: JSON.stringify(date),
        headers: { 'Content-Type': 'application/json' } });
    if (r.ok) {
        this.reset();
        modal.classList.remove('deschis');
    }
});

// Avizul (PDF) se deschide intr-un tab nou al browserului.
document.getElementById('genereazaAviz').addEventListener('click', function () {
    const id = document.getElementById('expediere').dataset.id;
    window.open('/avize/genereaza?expediere=' + id, '_blank');
});
