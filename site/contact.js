(function () {
  // JSTN contactpagina (v2). WhatsApp-formulier: bericht klaarzetten in WhatsApp; de klik loopt via de gedeelde
  // klik-afhandeling (NAV_JS): computer -> WhatsApp in nieuw tabblad + /bedankt/whatsapp/, telefoon -> door bij terugkeer.
  // E-mailformulier: Netlify Forms ('contact'), pas door naar /bedankt/formulier/ na een geslaagde verzending.
  var NUMMER = "31636179549", MAIL = "info@jstnmultidiensten.nl";
  function leeg(ids) { var ok = true; ids.forEach(function (id) { var el = document.getElementById(id); el.style.borderColor = "";
    if (!el.value.trim() || (el.type === "email" && !el.checkValidity())) { el.style.borderColor = "#e5484d"; ok = false; } }); return ok; }

  var wa = document.getElementById("waForm");
  if (wa) wa.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!leeg(["naam", "bericht"])) return;
    var plaats = document.getElementById("plaats").value.trim();
    var tekst = "Hallo JSTN Multidiensten!\n\nNaam: " + document.getElementById("naam").value.trim() + "\n" +
      "Ik ben: " + document.getElementById("type").value + "\n" + "Dienst: " + document.getElementById("dienst").value + "\n" +
      (plaats ? "Plaats: " + plaats + "\n" : "") + "\n" + document.getElementById("bericht").value.trim();
    var a = document.createElement("a");
    a.href = "https://wa.me/" + NUMMER + "?text=" + encodeURIComponent(tekst);
    document.body.appendChild(a); a.click(); a.remove();
  });

  var mf = document.getElementById("mailForm");
  if (mf) mf.addEventListener("submit", function (e) {
    e.preventDefault();
    var melding = document.getElementById("mailMelding"), knop = document.getElementById("mailKnop");
    melding.className = "msg";
    if (!leeg(["m-naam", "m-email", "m-bericht"])) { melding.textContent = "Vul uw naam, een geldig e-mailadres en uw vraag in."; melding.className = "msg err"; return; }
    if (mf.website.value) return;
    if (/^(localhost|127\.0\.0\.1)$/.test(location.hostname)) { melding.textContent = "Test: formulier werkt (lokaal wordt niets verstuurd)."; melding.className = "msg ok"; return; }
    knop.disabled = true; knop.textContent = "Bezig met versturen...";
    fetch("/", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: new URLSearchParams(new FormData(mf)).toString() })
      .then(function (r) { if (!r.ok) throw new Error(); window.location.href = "/bedankt/formulier/"; })
      .catch(function () {
        melding.innerHTML = 'Versturen lukte niet. Mail ons direct via <a href="mailto:' + MAIL + '">' + MAIL + '</a> of bel +31 6 36179549.';
        melding.className = "msg err"; knop.disabled = false; knop.textContent = "Verstuur aanvraag";
      });
  });
})();
