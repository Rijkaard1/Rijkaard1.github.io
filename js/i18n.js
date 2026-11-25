/* English / Deutsch switch.
   The pages are written in English. This script swaps every known English text for its German version
   (and back), and remembers the choice. Add a line to DE to translate another text.
   Names, code words and the course PDFs themselves stay in English. */
(function () {
  const DE = {
    /* ---------- shared: sidebar, footer ---------- */
    "CS Student · Cybersecurity Junior": "Informatik-Studium · Junior in Cybersicherheit",
    "~/home": "~/start",
    "~/about": "~/über-mich",
    "~/skills": "~/kenntnisse",
    "~/mathematics": "~/mathematik",
    "~/projects": "~/projekte",
    "~/contact": "~/kontakt",
    "Toggle menu": "Menü umschalten",
    "Light theme": "Helles Design",
    "Dark theme": "Dunkles Design",
    "Switch to light theme": "Zum hellen Design wechseln",
    "Switch to dark theme": "Zum dunklen Design wechseln",
    "Language": "Sprache",
    "Erich Law Eh: an armored knight seen from behind on a mountain summit, watching a burning castle at sunset in the rain":
      "Erich Law Eh: ein gepanzerter Ritter von hinten auf einem Berggipfel, der im Regen bei Sonnenuntergang eine brennende Burg betrachtet",
    "Rijkaard's Cyberworld: an armored knight watching a burning castle at sunset":
      "Rijkaard's Cyberworld: ein gepanzerter Ritter betrachtet bei Sonnenuntergang eine brennende Burg",

    /* ---------- Home ---------- */
    "> hello, world": "> hallo, welt",
    "I'm": "Ich bin",
    "I build things with code.": "Ich baue Dinge mit Code.",
    "Burmese (Myanmar) Computer Science student at Kasem Bundit University, working toward a BSc. I program in several languages, I'm a junior in cybersecurity, and I use AI effectively in my work.":
      "Ich komme aus Myanmar (burmesisch) und studiere Informatik an der Kasem Bundit University, auf dem Weg zum BSc. Ich programmiere in mehreren Sprachen, bin Junior in Cybersicherheit und setze KI wirkungsvoll bei meiner Arbeit ein.",
    "View Projects": "Projekte ansehen",
    "About Me": "Über mich",
    "Download CV": "Lebenslauf herunterladen",
    "At a glance": "Auf einen Blick",
    "coding languages": "Programmiersprachen",
    "spoken languages": "gesprochene Sprachen",
    "maths courses (PDF)": "Mathe-Kurse (PDF)",
    "projects": "Projekte",
    "Explore": "Entdecken",
    "Highlights": "Highlights",
    "Featured project": "Ausgewähltes Projekt",
    ": a programming quiz adventure game made with Unity and C#, built with my university team.":
      ": ein Programmier-Quiz-Abenteuerspiel, entwickelt mit Unity und C# gemeinsam mit meinem Uni-Team.",
    "Screenshot of The Last Cipher of Eden, the language choice screen":
      "Screenshot von The Last Cipher of Eden: der Bildschirm zur Sprachauswahl",
    "See my projects →": "Meine Projekte ansehen →",
    "Mathematics notes": "Mathematik-Skripte",
    "Nine free PDF courses I wrote, from pre-algebra up to double integrals and complex analysis.":
      "Neun kostenlose PDF-Kurse, die ich geschrieben habe: von der Prä-Algebra bis zu Doppelintegralen und komplexer Analysis.",
    "Open the courses →": "Kurse öffnen →",
    "Skills": "Kenntnisse",
    "Cybersecurity": "Cybersicherheit",
    "Python, Java, C++, C#, JavaScript, TypeScript, HTML and CSS, plus basic SQL. Junior in cybersecurity and effective with AI.":
      "Python, Java, C++, C#, JavaScript, TypeScript, HTML und CSS sowie Grundkenntnisse in SQL. Junior in Cybersicherheit und effektiver Einsatz von KI.",
    "See all skills →": "Alle Kenntnisse ansehen →",

    /* ---------- About ---------- */
    "About": "Über mich",
    "Background, education and nationality.": "Hintergrund, Ausbildung und Nationalität.",
    "Nationality": "Nationalität",
    "Burmese (Myanmar)": "Burmesisch (Myanmar)",
    "Education": "Ausbildung",
    "Up to Grade 6": "Bis zur 6. Klasse",
    "Basic Education High School, Myanmar.": "Basic Education High School, Myanmar.",
    "Left school after Grade 6 and passed the GED in 2024.": "Schule nach der 6. Klasse verlassen; 2024 den GED bestanden.",
    "Present": "Heute",
    "BSc in Computer Science": "BSc Informatik",
    "Kasem Bundit University (currently studying).": "Kasem Bundit University (aktuelles Studium).",
    "Mathematics & Science": "Mathematik & Naturwissenschaften",
    "Calculus II": "Analysis II",
    "Statistics": "Statistik",
    "Data Analytics": "Datenanalyse",
    "Complex Analysis": "Komplexe Analysis",
    "Mechanics (Physics)": "Mechanik (Physik)",
    "Trigonometry": "Trigonometrie",
    "Geometry": "Geometrie",

    /* ---------- Skills ---------- */
    "Programming knowledge, languages I speak, and more.": "Programmierkenntnisse, Sprachen, die ich spreche, und mehr.",
    "Programming Languages": "Programmiersprachen",
    "Intermediate": "Mittelstufe",
    "Beginner": "Anfänger",
    "Basic": "Grundkenntnisse",
    "Spoken Languages": "Gesprochene Sprachen",
    "Burmese": "Burmesisch",
    "Native": "Muttersprache",
    "English": "Englisch",
    "Fluent": "Fließend",
    "Chinese": "Chinesisch",
    "Conversational": "Gesprächssicher",
    "German": "Deutsch",
    "Junior": "Junior",
    "AI": "KI",
    "AI-assisted development": "KI-gestützte Entwicklung",
    "Effective": "Effektiv",

    /* ---------- Mathematics ---------- */
    "Mathematics": "Mathematik",
    "Choose a branch to see its courses.": "Wähle einen Bereich, um die Kurse zu sehen.",
    "Real Analysis": "Reelle Analysis",
    "From pre-algebra to advanced integration: algebra, geometry, trigonometry, probability and statistics, calculus and double integrals, ordered from the basics upward.":
      "Von der Prä-Algebra bis zur fortgeschrittenen Integration: Algebra, Geometrie, Trigonometrie, Wahrscheinlichkeit und Statistik, Analysis und Doppelintegrale, von den Grundlagen aufwärts geordnet.",
    "8 courses": "8 Kurse",
    "1 course": "1 Kurs",
    "View courses →": "Kurse ansehen →",
    "The world of imaginary numbers. It covers Euler’s formula, the complex plane, contour integrals and Cauchy’s theorem.":
      "Die Welt der imaginären Zahlen. Sie umfasst die Eulersche Formel, die komplexe Ebene, Kurvenintegrale und den Satz von Cauchy.",

    /* ---------- Real Analysis ---------- */
    "← Mathematics": "← Mathematik",
    "Ordered from the basics to the most advanced: pre-algebra, algebra, geometry, trigonometry, probability and statistics, calculus and integration. Click a course to open its PDF.":
      "Von den Grundlagen bis zum Anspruchsvollsten geordnet: Prä-Algebra, Algebra, Geometrie, Trigonometrie, Wahrscheinlichkeit und Statistik, Analysis und Integration. Klicke auf einen Kurs, um das PDF zu öffnen. Die PDFs sind auf Englisch.",
    "Search courses": "Kurse durchsuchen",
    "Search courses or topics, e.g. fractions, integrals, unit circle": "Kurse oder Themen suchen, z. B. Brüche, Integrale, Einheitskreis",
    "Filter by level": "Nach Stufe filtern",
    "Solutions PDF available": "Lösungs-PDF vorhanden",
    "No courses match your search.": "Keine Kurse passen zu deiner Suche.",
    "Clear search and filters": "Suche und Filter zurücksetzen",
    "Open PDF →": "PDF öffnen →",
    "Solutions PDF →": "Lösungs-PDF →",
    "Answer key included": "Lösungsschlüssel enthalten",

    "Level 1 · PDF · 89 pages · by Rijkaard": "Stufe 1 · PDF · 89 Seiten · von Rijkaard",
    "Level 2 · PDF · 95 pages · by Rijkaard": "Stufe 2 · PDF · 95 Seiten · von Rijkaard",
    "Level 3 · PDF · 79 pages · by Rijkaard": "Stufe 3 · PDF · 79 Seiten · von Rijkaard",
    "Level 4 · PDF · 89 pages · by Rijkaard": "Stufe 4 · PDF · 89 Seiten · von Rijkaard",
    "Level 5 · PDF · 95 pages · by Rijkaard": "Stufe 5 · PDF · 95 Seiten · von Rijkaard",
    "Level 6 · PDF · 32 pages": "Stufe 6 · PDF · 32 Seiten",
    "Level 7 · PDF · 42 pages": "Stufe 7 · PDF · 42 Seiten",
    "Level 8 · PDF · 37 pages": "Stufe 8 · PDF · 37 Seiten",

    "The starting point: from whole numbers and fractions to shapes, data and the first equations. It covers number sense, decimals and percents, integers, ratios and proportions, simple equations, measurement, and graphs and probability, and ends with a final test.":
      "Der Startpunkt: von natürlichen Zahlen und Brüchen zu Formen, Daten und den ersten Gleichungen. Behandelt Zahlenverständnis, Dezimalzahlen und Prozente, ganze Zahlen, Verhältnisse und Proportionen, einfache Gleichungen, Messen sowie Diagramme und Wahrscheinlichkeit und endet mit einem Abschlusstest.",
    "A full course that takes you from the first numbers to the threshold of trigonometry. It builds the algebra everything else depends on, with worked examples and exercises in every chapter.":
      "Ein vollständiger Kurs von den ersten Zahlen bis zur Schwelle der Trigonometrie. Er baut die Algebra auf, von der alles Weitere abhängt, mit durchgerechneten Beispielen und Übungen in jedem Kapitel.",
    "A full course from points and angles to solids and transformations. It covers shapes, triangles, the Pythagorean theorem, perimeter and area, circles, volume and surface area, and coordinate geometry.":
      "Ein vollständiger Kurs von Punkten und Winkeln bis zu Körpern und Transformationen. Behandelt Figuren, Dreiecke, den Satz des Pythagoras, Umfang und Flächeninhalt, Kreise, Volumen und Oberfläche sowie Koordinatengeometrie.",
    "From triangles and waves to the doorstep of calculus. It covers right-triangle trigonometry, the unit circle and radians, graphs, identities and equations, then polynomial and rational functions, vectors, polar coordinates and complex numbers.":
      "Von Dreiecken und Wellen bis an die Schwelle der Analysis. Behandelt Trigonometrie im rechtwinkligen Dreieck, Einheitskreis und Bogenmaß, Graphen, Identitäten und Gleichungen, dann Polynom- und rationale Funktionen, Vektoren, Polarkoordinaten und komplexe Zahlen.",
    "From counting data to making smart guesses. It covers describing data, averages and spread, probability rules, counting and combinations, conditional probability, random variables, the binomial and normal distributions, and sampling and inference.":
      "Vom Zählen von Daten bis zum klugen Schätzen. Behandelt das Beschreiben von Daten, Mittelwerte und Streuung, Wahrscheinlichkeitsregeln, Zählen und Kombinatorik, bedingte Wahrscheinlichkeit, Zufallsvariablen, Binomial- und Normalverteilung sowie Stichproben und Schlussfolgerungen.",
    "A complete study guide to the core of calculus: limits, derivatives and an introduction to integration. It includes worked examples, practice problems for every chapter, a full answer key and a formula sheet.":
      "Ein vollständiger Lernleitfaden zum Kern der Analysis: Grenzwerte, Ableitungen und eine Einführung in die Integration. Mit durchgerechneten Beispielen, Übungsaufgaben zu jedem Kapitel, einem vollständigen Lösungsschlüssel und einer Formelsammlung.",
    "The next step after basic integration: the main techniques, improper integrals, numerical methods and applications. It ends with a strategy chapter, a mixed review, an answer key and a formula sheet.":
      "Der nächste Schritt nach der Grundintegration: die wichtigsten Techniken, uneigentliche Integrale, numerische Verfahren und Anwendungen. Es endet mit einem Strategiekapitel, einer gemischten Wiederholung, einem Lösungsschlüssel und einer Formelsammlung.",
    "An introduction to integrating over regions in the plane. It covers partial derivatives, Fubini’s theorem, polar coordinates, applications such as area, volume and mass, change of variables, and a first look at triple integrals.":
      "Eine Einführung in die Integration über Gebiete in der Ebene. Behandelt partielle Ableitungen, den Satz von Fubini, Polarkoordinaten, Anwendungen wie Fläche, Volumen und Masse, Variablentransformation sowie einen ersten Blick auf Dreifachintegrale.",

    "Whole numbers": "Natürliche Zahlen",
    "Fractions": "Brüche",
    "Decimals and percents": "Dezimalzahlen und Prozente",
    "Integers": "Ganze Zahlen",
    "Ratios and proportions": "Verhältnisse und Proportionen",
    "First equations": "Erste Gleichungen",
    "Shapes and area": "Formen und Fläche",
    "Data and probability": "Daten und Wahrscheinlichkeit",
    "Arithmetic": "Arithmetik",
    "Equations": "Gleichungen",
    "Graphs and lines": "Graphen und Geraden",
    "Polynomials": "Polynome",
    "Quadratics": "Quadratische Gleichungen",
    "Functions": "Funktionen",
    "Logarithms": "Logarithmen",
    "Pre-trigonometry": "Vor-Trigonometrie",
    "Angles": "Winkel",
    "Triangles": "Dreiecke",
    "Area": "Fläche",
    "Circles": "Kreise",
    "Solids": "Körper",
    "Transformations": "Transformationen",
    "Unit circle": "Einheitskreis",
    "Radians": "Bogenmaß",
    "Identities": "Identitäten",
    "Trig graphs": "Trigonometrische Graphen",
    "Vectors": "Vektoren",
    "Polar coordinates": "Polarkoordinaten",
    "Data and graphs": "Daten und Diagramme",
    "Mean and spread": "Mittelwert und Streuung",
    "Probability": "Wahrscheinlichkeit",
    "Counting": "Abzählen",
    "Conditional probability": "Bedingte Wahrscheinlichkeit",
    "Random variables": "Zufallsvariablen",
    "Normal distribution": "Normalverteilung",
    "Inference": "Schließende Statistik",
    "Limits": "Grenzwerte",
    "Derivatives": "Ableitungen",
    "Chain rule": "Kettenregel",
    "Riemann sums": "Riemann-Summen",
    "Substitution": "Substitution",
    "Integration by parts": "Partielle Integration",
    "Trig substitution": "Trigonometrische Substitution",
    "Partial fractions": "Partialbruchzerlegung",
    "Improper integrals": "Uneigentliche Integrale",
    "Simpson’s rule": "Simpson-Regel",
    "Arc length": "Bogenlänge",
    "Partial derivatives": "Partielle Ableitungen",
    "Jacobian": "Jacobi-Determinante",
    "Triple integrals": "Dreifachintegrale",

    /* ---------- Complex Analysis ---------- */
    "Imaginary numbers, Euler’s formula and contour integrals. Click the course to open its PDF.":
      "Imaginäre Zahlen, Eulersche Formel und Kurvenintegrale. Klicke auf den Kurs, um das PDF zu öffnen. Das PDF ist auf Englisch.",
    "PDF · 33 pages · by Rijkaard": "PDF · 33 Seiten · von Rijkaard",
    "An introduction to complex analysis in four chapters, with worked examples, history notes and links to physics. It runs from imaginary numbers and Euler’s formula to contour integrals, the Cauchy–Riemann equations and Cauchy’s theorem.":
      "Eine Einführung in die komplexe Analysis in vier Kapiteln mit durchgerechneten Beispielen, historischen Hinweisen und Bezügen zur Physik. Sie reicht von imaginären Zahlen und der Eulerschen Formel bis zu Kurvenintegralen, den Cauchy-Riemann-Gleichungen und dem Satz von Cauchy.",
    "Complex numbers": "Komplexe Zahlen",
    "Euler’s formula": "Eulersche Formel",
    "Contour integrals": "Kurvenintegrale",
    "Cauchy’s theorem": "Satz von Cauchy",

    /* ---------- Projects ---------- */
    "Projects": "Projekte",
    "Things I've built so far.": "Was ich bisher gebaut habe.",
    "The Last Cipher of Eden logo": "Logo von The Last Cipher of Eden",
    "DTI413 Innovation Project · Kasem Bundit University · Team project":
      "DTI413 Innovationsprojekt · Kasem Bundit University · Teamprojekt",
    "A programming-language adventure quiz game for Windows. The player helps the Coder rescue the Girl of Eden by answering programming questions in one of nine languages, then fixes the Overlord's broken program to open her cell.":
      "Ein Programmiersprachen-Abenteuer-Quizspiel für Windows. Spielende helfen dem Coder, das Mädchen von Eden zu retten, indem sie Programmierfragen in einer von neun Sprachen beantworten. Danach reparieren sie das kaputte Programm des Overlords, um ihre Zelle zu öffnen.",
    "9 languages: Python, Java, C#, JavaScript, TypeScript, C++, Rust, SQL, PHP":
      "9 Sprachen: Python, Java, C#, JavaScript, TypeScript, C++, Rust, SQL, PHP",
    "Team": "Team",
    "Built together by:": "Gemeinsam entwickelt von:",
    "View repository →": "Repository ansehen →",
    "Personal project · Command-line tool · Windows": "Eigenes Projekt · Kommandozeilen-Tool · Windows",
    "Last updated:": "Zuletzt aktualisiert:",
    "A Python security checker for Windows that runs from a simple menu. It shows which network you are on, whether your Wi-Fi is safe, your public IP details, the IP addresses your laptop is talking to (and warns about new ones), apps opened in the last 24 hours, downloads from the last month rated SAFE / CAUTION / WARNING, startup programs, and open ports. It can also find a file by name and type, and save every scan to a log.":
      "Ein Python-Sicherheitsprüfer für Windows, der über ein einfaches Menü läuft. Er zeigt, in welchem Netzwerk du bist, ob dein WLAN sicher ist, deine öffentlichen IP-Daten, die IP-Adressen, mit denen dein Laptop kommuniziert (und warnt vor neuen), in den letzten 24 Stunden geöffnete Apps, Downloads des letzten Monats mit der Bewertung SAFE / CAUTION / WARNING, Autostart-Programme und offene Ports. Außerdem kann er Dateien nach Name und Typ finden und jeden Scan in einem Protokoll speichern.",
    "Networking": "Netzwerke",
    "Standard library only": "Nur Standardbibliothek",
    "View source →": "Quellcode ansehen →",
    "Changelog →": "Änderungsprotokoll →",
    "View all repositories →": "Alle Repositories ansehen →",
    "Enlarged screenshot": "Vergrößerter Screenshot",
    "Close": "Schließen",
    "Enlarge: The Coder tells the story": "Vergrößern: Der Coder erzählt die Geschichte",
    "The Coder tells the story": "Der Coder erzählt die Geschichte",
    "Enlarge: Choose your language": "Vergrößern: Sprache wählen",
    "Choose your language screen with nine languages": "Bildschirm zur Sprachauswahl mit neun Sprachen",
    "Enlarge: A wrong answer and the Byte Spider": "Vergrößern: Eine falsche Antwort und die Byte-Spinne",
    "A wrong answer and the Byte Spider's reaction": "Eine falsche Antwort und die Reaktion der Byte-Spinne",
    "Enlarge: Map after the Beginner level": "Vergrößern: Karte nach dem Anfänger-Level",
    "Map after the Beginner level": "Karte nach dem Anfänger-Level",
    "Enlarge: The Overlord story scene": "Vergrößern: Die Story-Szene mit dem Overlord",
    "The Overlord story scene": "Die Story-Szene mit dem Overlord",
    "Enlarge: The final challenge begins": "Vergrößern: Die letzte Herausforderung beginnt",
    "The final challenge begins": "Die letzte Herausforderung beginnt",
    "Enlarge: The Overlord is defeated": "Vergrößern: Der Overlord ist besiegt",
    "The Overlord is defeated": "Der Overlord ist besiegt",
    "Enlarge: She is free": "Vergrößern: Sie ist frei",
    "Victory: the Girl of Eden is free": "Sieg: Das Mädchen von Eden ist frei",
    "Enlarge: Simple Security System menu and risk score": "Vergrößern: Menü und Risikowert des Simple Security System",
    "Simple Security System in PowerShell: the main menu with 12 options and the risk score of 33 out of 100 (moderate) with what raised it and tips":
      "Simple Security System in PowerShell: das Hauptmenü mit 12 Optionen und der Risikowert 33 von 100 (mäßig), mit den Gründen dafür und Tipps",

    /* ---------- Contact ---------- */
    "Contact": "Kontakt",
    "Want to talk, ask a question or see my code? Email me or find me on GitHub.":
      "Du möchtest reden, eine Frage stellen oder meinen Code sehen? Schreib mir eine E-Mail oder finde mich auf GitHub.",
    "Email": "E-Mail",
    "The best way to reach me for questions, projects or study help.":
      "Der beste Weg, mich für Fragen, Projekte oder Lernhilfe zu erreichen.",
    "CV": "Lebenslauf",
    "My one-page CV with education, skills and projects (PDF).":
      "Mein einseitiger Lebenslauf mit Ausbildung, Kenntnissen und Projekten (PDF, auf Englisch).",
    "Download CV ↓": "Lebenslauf herunterladen ↓",
    "Browse my repositories and recent work.": "Stöbere in meinen Repositories und aktuellen Arbeiten.",

    /* ---------- page titles and search/preview texts ---------- */
    "About | Rijkaard's Cyberworld": "Über mich | Rijkaard's Cyberworld",
    "Skills | Rijkaard's Cyberworld": "Kenntnisse | Rijkaard's Cyberworld",
    "Mathematics | Rijkaard's Cyberworld": "Mathematik | Rijkaard's Cyberworld",
    "Real Analysis | Rijkaard's Cyberworld": "Reelle Analysis | Rijkaard's Cyberworld",
    "Complex Analysis | Rijkaard's Cyberworld": "Komplexe Analysis | Rijkaard's Cyberworld",
    "Projects | Rijkaard's Cyberworld": "Projekte | Rijkaard's Cyberworld",
    "Contact | Rijkaard's Cyberworld": "Kontakt | Rijkaard's Cyberworld",
    "Portfolio of Erich Law Eh: Computer Science student and junior cybersecurity enthusiast. Projects, programming skills and mathematics notes.":
      "Portfolio von Erich Law Eh: Informatik-Studium und Junior in Cybersicherheit. Projekte, Programmierkenntnisse und Mathematik-Skripte.",
    "Education, nationality and background of Erich Law Eh.": "Ausbildung, Nationalität und Hintergrund von Erich Law Eh.",
    "Programming languages, spoken languages and skills of Erich Law Eh.": "Programmiersprachen, gesprochene Sprachen und Kenntnisse von Erich Law Eh.",
    "Mathematics courses and study files of Erich Law Eh.": "Mathematik-Kurse und Lernunterlagen von Erich Law Eh.",
    "Real Analysis courses and study guides by Erich Law Eh.": "Kurse und Lernleitfäden zur Reellen Analysis von Erich Law Eh.",
    "Complex Analysis course by Erich Law Eh.": "Kurs zur Komplexen Analysis von Erich Law Eh.",
    "Projects built by Erich Law Eh.": "Projekte von Erich Law Eh.",
    "Find Erich Law Eh on GitHub.": "Erich Law Eh auf GitHub finden."
  };

  /* texts that need a different German word depending on where they appear (matched by data-i18n="key") */
  const KEYS = {
    "band.all": "Alle Stufen",
    "band.basic": "Grundlagen",
    "band.intermediate": "Mittelstufe",
    "band.advanced": "Fortgeschritten"
  };

  const norm = (s) => s.replace(/\s+/g, " ").trim();
  let lang = "en";
  try {
    const saved = localStorage.getItem("lang");
    if (saved === "de" || saved === "en") lang = saved;
  } catch (e) { /* not saved */ }

  const textNodes = [];  // { node, en, de, lead, trail }
  const attrs = [];      // { el, name, en, de }
  const keyed = [];      // { el, en, de }
  const metas = [];      // { el, en, de }
  let titleEn = document.title;

  function collect() {
    document.querySelectorAll("[data-i18n]").forEach((el) => {
      const de = KEYS[el.dataset.i18n];
      if (de) keyed.push({ el, en: el.textContent, de });
    });
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode(n) {
        const p = n.parentElement;
        if (!p || p.closest("script,style,noscript,[data-no-i18n],[data-i18n]")) return NodeFilter.FILTER_REJECT;
        const t = norm(n.data);
        return t && DE[t] ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
      },
    });
    while (walker.nextNode()) {
      const node = walker.currentNode;
      const t = norm(node.data);
      textNodes.push({
        node, en: node.data, de: DE[t],
        lead: node.data.match(/^\s*/)[0], trail: node.data.match(/\s*$/)[0],
      });
    }
    ["alt", "aria-label", "placeholder", "title"].forEach((name) => {
      document.querySelectorAll("[" + name + "]").forEach((el) => {
        if (el.closest("[data-no-i18n]")) return;
        const v = el.getAttribute(name);
        if (v && DE[norm(v)]) attrs.push({ el, name, en: v, de: DE[norm(v)] });
      });
    });
    document.querySelectorAll(
      'meta[name="description"], meta[property="og:title"], meta[property="og:description"], meta[property="og:image:alt"]'
    ).forEach((el) => {
      const v = el.getAttribute("content");
      if (v && DE[norm(v)]) metas.push({ el, en: v, de: DE[norm(v)] });
    });
  }

  function apply(next) {
    lang = next;
    const de = lang === "de";
    textNodes.forEach((t) => { t.node.data = de ? t.lead + t.de + t.trail : t.en; });
    attrs.forEach((a) => a.el.setAttribute(a.name, de ? a.de : a.en));
    keyed.forEach((k) => { k.el.textContent = de ? k.de : k.en; });
    metas.forEach((m) => m.el.setAttribute("content", de ? m.de : m.en));
    document.title = de && DE[norm(titleEn)] ? DE[norm(titleEn)] : titleEn;
    document.documentElement.setAttribute("lang", lang);
    document.querySelectorAll(".lang-btn").forEach((b) => {
      const on = b.dataset.lang === lang;
      b.classList.toggle("active", on);
      b.setAttribute("aria-pressed", on ? "true" : "false");
    });
    document.dispatchEvent(new CustomEvent("langchange", { detail: lang }));
  }

  function set(next) {
    if (next !== "de" && next !== "en") return;
    try { localStorage.setItem("lang", next); } catch (e) { /* not saved */ }
    apply(next);
  }

  collect();
  document.querySelectorAll(".lang-btn").forEach((b) => b.addEventListener("click", () => set(b.dataset.lang)));
  apply(lang);

  // t("English text") gives the German text when German is on (for texts made by other scripts)
  window.i18n = {
    lang: () => lang,
    set,
    t: (en) => (lang === "de" && DE[en] ? DE[en] : en),
  };
})();
