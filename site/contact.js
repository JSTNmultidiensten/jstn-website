(function () {
  var NUMMER = "31636179549";
  var MAIL = "info@jstnmultidiensten.nl";

  // Tabs
  document.querySelectorAll(".tab").forEach(function (tab) {
    tab.addEventListener("click", function () {
      document.querySelectorAll(".tab").forEach(function (t) { t.classList.remove("on"); t.setAttribute("aria-selected", "false"); });
      document.querySelectorAll(".pane").forEach(function (p) { p.classList.remove("on"); });
      tab.classList.add("on"); tab.setAttribute("aria-selected", "true");
      document.getElementById("pane-" + tab.dataset.tab).classList.add("on");
    });
  });

  // WhatsApp-formulier
  document.getElementById("waForm").addEventListener("submit", function (e) {
    e.preventDefault();
    var naam = document.getElementById("naam"), bericht = document.getElementById("bericht");
    [naam, bericht].forEach(function (el) { el.style.borderColor = ""; });
    if (!naam.value.trim() || !bericht.value.trim()) {
      [naam, bericht].forEach(function (el) { if (!el.value.trim()) el.style.borderColor = "#e5484d"; });
      return;
    }
    var plaats = document.getElementById("plaats").value.trim();
    var tekst = "Hallo JSTN Multidiensten!\n\n" +
      "Naam: " + naam.value.trim() + "\n" +
      "Ik ben: " + document.getElementById("type").value + "\n" +
      "Dienst: " + document.getElementById("dienst").value + "\n" +
      (plaats ? "Plaats: " + plaats + "\n" : "") +
      "\n" + bericht.value.trim();
    window.open("https://wa.me/" + NUMMER + "?text=" + encodeURIComponent(tekst), "_blank", "noopener");
  });

  // E-mailformulier via FormSubmit
  document.getElementById("mailForm").addEventListener("submit", function (e) {
    e.preventDefault();
    var form = e.target, melding = document.getElementById("mailMelding"), knop = document.getElementById("mailKnop");
    melding.className = "msg";
    var ok = true;
    ["m-naam", "m-email", "m-bericht"].forEach(function (id) {
      var el = document.getElementById(id);
      el.style.borderColor = "";
      if (!el.value.trim() || (el.type === "email" && !el.checkValidity())) { el.style.borderColor = "#e5484d"; ok = false; }
    });
    if (!ok) { melding.textContent = "Vul uw naam, een geldig e-mailadres en uw vraag in."; melding.className = "msg err"; return; }
    var data = {};
    new FormData(form).forEach(function (v, k) { data[k] = v; });
    data._subject = "Nieuwe aanvraag via website – " + data["Dienst"];
    data._template = "table";
    data._captcha = "false";
    knop.disabled = true; knop.textContent = "Bezig met versturen...";
    fetch("https://formsubmit.co/ajax/" + MAIL, {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify(data)
    }).then(function (res) {
      if (!res.ok) throw new Error();
      form.reset();
      melding.textContent = "Bedankt! Uw aanvraag is verstuurd. We reageren binnen 12 uur.";
      melding.className = "msg ok";
    }).catch(function () {
      melding.innerHTML = 'Versturen lukte niet. Mail ons direct via <a href="mailto:' + MAIL + '">' + MAIL + '</a> of bel +31 6 36179549.';
      melding.className = "msg err";
    }).then(function () {
      knop.disabled = false; knop.textContent = "Verstuur aanvraag";
    });
  });
})();
