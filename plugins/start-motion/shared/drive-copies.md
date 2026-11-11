# Where the design, the readout and the review page live

The solution design, the solution readout and the design and build review page are client records. They must outlive the person who made them, so none of them lives only in one person's Claude account. The master copy of each is an HTML file in the client's Google Drive folder. The Claude link (the artifact) is how people read it; anyone on the client can republish that link from the Drive file.

People change these documents through Claude, never by hand. So each run reads the master copy from Drive, works on it, and writes the new version back to Drive.

## Folders and names

In the client's Drive folder, next to the Discovery subfolder:

| Document | Subfolder | File names |
|---|---|---|
| Solution design | `Design` | `[Client] Solution Design v0.3.html`, the content file `[Client] Design content v0.3.json`, and `[Client] Solution Design v0.3.pdf` when it goes Final or someone asks for one |
| Solution readout | `Readout` | `[Client] Solution Readout v1.1.html`, `.pdf`, and the content file `[Client] Readout content v1.1.json` |
| Design and build review page | `Build` | `[Client] Design and Build Review [date].html` |

Make the subfolder the first time, with the Google Drive connector, and say so in the report.

## One running document, one file per version

There is only ever one design and one readout per client. Each saved version is its own file, because the Drive connector can create a file but cannot replace the contents of one.

- The current version sits at the top of the subfolder. Before saving a new one, move the previous version's files into an `Older versions` folder inside the same subfolder (change the file's parent; never trash it). Drive keeps the full history that way, and anyone opening the folder sees exactly one current file.
- Upload HTML with `contentMimeType` `text/html` and `disableConversionToGoogleType` set to true. Without that, Drive turns the page into a Google Doc and the diagrams are lost.
- Versions: `v0.1`, `v0.2` and so on while it is a draft; `v1.0` when it goes Final (the design at scope sign-off, the readout at client sign-off); `v1.1` and up for any change after that. The version and the date are in the page header and in the file name, and they match.
- The page ends with a short change log: one line per version, with the date, who asked for it, and what changed.

## The PDF

Drive cannot preview an HTML file; clicking it offers a download. So every version saved also gets a PDF of the same page, saved next to it, which Drive previews and which can be sent to a client. Print it with headless Chrome: `google-chrome --headless --no-pdf-header-footer --print-to-pdf=<file.pdf> file://<page.html>` (`chromium` works the same; add `--no-sandbox` in a container). Keep the page's colors by giving the page `print-color-adjust: exact` before printing. If there is no way to print one in the session, save the HTML alone and say in the report that the PDF is missing.

The solution design is the exception while it is a draft: its drafts are read through the Claude link, and its PDF is made when the design goes Final or when someone asks for one. The design's content file is saved with every version, next to the page, because the next run starts from it.

## The Claude link

Publish the page as an artifact from the same HTML: the first time a new artifact, every time after that a new version of the same one, so the link never changes. Put the link in the Drive file's description and in the Discovery documents note. If the person running the stage cannot publish to the existing link (someone else made it, or that person has left), publish a new artifact from the current Drive file, put the new link in both places, and say so. Never publish over someone else's artifact.

## Reading it

At the start of every run, read the current version from the Drive subfolder (download it with the Google Drive connector), not from an artifact, not from the Claude Project and never from memory. If the artifact and the Drive file disagree, the Drive file wins; say so in the report. If there is no Drive copy yet but an artifact exists (a design or readout from before this rule), take the artifact's page, save it to Drive as the next version, and carry on from there.

## The workflow document and What we heard

These two stay Claude links owned by the SC who runs discovery; they are not copied into Drive. Their links are in the Google Doc "Discovery documents: [Client]" in the client's Drive folder (Discovery subfolder), which also names the SC. When a stage needs one of them:

- Open it from the link in that note. If the note is missing, look in the client's Drive folder and the person's own artifacts for "[Client] Workflows" and "[Client] What We Heard".
- If the link opens, use it. If it will not open because it was not shared with this person, or it cannot be found at all, say which one, name the SC who owns it (from the note), and ask the person to have the SC share it with them, or share all of the client's workflow diagrams if the person has none. Give them the exact link to ask about when there is one. Then carry on with everything that does not need it, and pick it up once they say it is shared.
- Never rebuild a workflow or What we heard from memory, from the readout's copy of it or from transcripts in its place. The signed readout's PDF in Drive is the record of what the client signed, and a stage that only needs the signed workflows (build planning) may read them from that PDF and say so.

## When Drive cannot be reached

Where the session has no Google Drive connector (Claude Code or Codex without it), save the files to `docs/` in the client's repo when there is one, and say plainly in the report that the Drive copy was not saved and needs saving from a session that has Drive. Never leave the only copy in a Claude Project or a local folder without saying so.
