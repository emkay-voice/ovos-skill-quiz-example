# A quiz skill

The skill asks, you answer: say **"quiz me"**, and it asks three
questions, listens for your answer after each one, tells you whether you were
right, gives your score and asks whether you want to play again – in all
twelve of [Emkay](https://emkay.ai)'s languages.

**👉 The friendly guide: <https://dev.emkay.ai>**

## What it shows

- **Asking back:** `self.get_response(question)` speaks the question and waits
  for the next thing you say; `self.ask_yesno("again")` does the same and
  turns the answer into `"yes"`, `"no"` or `None`.
- **Your own data per language:** the questions are in
  `locale/<language>/questions.list`, one per line:
  `question | answer | another way to say it`. `self.find_resource()` finds
  the file for the language Emkay speaks.
- **Stopping:** say "stop" during a quiz and it ends. `can_stop()` tells OVOS
  there is something to stop, `stop_session()` stops it – in the session
  (device) where the quiz is going on, not on every device at once.
- **Dialogs with values:** `{count}`, `{answer}`, `{points}` and `{total}` in
  the `.dialog` files are filled in by `speak_dialog(name, {...})`.

## Why not "start the quiz"?

OVOS' media player (OCP) claims every sentence that begins with *play …* or
*start …* (in Danish also *spil …*), and it is asked before ordinary skills –
"start the quiz" would look for a quiz to play as music. So the sentences in
`start.intent` begin with other words. The golden utterances in
`test/end2end/` are how you find out: a test that says `got ocp:play` means a
sentence was taken by the media player.

## Try changing

- the questions – add your own, any number of lines;
- `ROUNDS` in `__init__.py` – how many it asks;
- what it says when you are right (`right.dialog`) – one line is picked at random.

## A working skill, and a template

This is a complete OpenVoiceOS skill – install it and it works – and an
example to start your own from: *Use this template* on GitHub, or
*Emkay: New skill* in VS Code ([Emkay Dev](https://dev.emkay.ai)), which
gives it your own names. Made for [Emkay](https://emkay.ai), it runs on any
OpenVoiceOS.

## Try it

- **Emkay Dev (VS Code):** *Emkay: Run the skill in Emkay* (Ctrl+Alt+E) opens
  Emkay next to your code and loads the skill; type under Emkay to talk to it.
  Every save loads it again. *Emkay: Test the skill* sends the golden
  utterances and shows ✓ / ✗ in the Testing view. Emkay's menu →
  *Guardian* → *What's happening?* shows which skill took a sentence, and why.
- **ovos-tui-client (Codespaces, Dev Container):** run `ovos-tui` in the
  terminal, type to talk, `Ctrl+P` → *Test* runs the same golden utterances
  against a full OpenVoiceOS.
- **pytest:** `pytest -q` – no OpenVoiceOS needed.

When you make a repository from this template ("Use this template"), a
small workflow renames the skill after your repository and then removes
itself.

## Show it, on your own Emkay, and into the store

To show it in [See my skill](https://dev.emkay.ai/#gallery) on dev.emkay.ai –
ready or not – add the topic `emkay-skill` to the repository (the ⚙ next to
*About*). Remove the topic, or make the repository private, to take it away.

*Emkay: Send to my Emkay* shows a QR code that installs this skill from
GitHub on the Emkay you scan it with. To get it into the
[Emkay store](https://store.emkay.ai): topics `ovos` and `openvoiceos` on the
repository, a release on GitHub (`publish.yml` puts it on PyPI), and the
store's nightly test does the rest – <https://dev.emkay.ai/#store>.

More on writing skills:
[the OpenVoiceOS technical manual](https://openvoiceos.github.io/ovos-technical-manual/).
