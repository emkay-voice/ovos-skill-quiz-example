"""A small quiz: the skill asks, you answer.

Say "quiz me". The skill asks three questions from
locale/<language>/questions.list, one per line as "question | answer |
another way to say the answer", listens for your answer after each one
(get_response), says whether it was right, gives your score and asks if
you want to play again (ask_yesno).

Try changing: the questions (any number of lines), how many are asked
(ROUNDS), or what it says in right.dialog, wrong.dialog and score.dialog.

"Stop" ends a quiz: OVOS asks every skill whether it has something to stop
(can_stop) and tells the one that has (stop_session).
"""
import random

from ovos_bus_client.session import SessionManager
from ovos_workshop.decorators import intent_handler
from ovos_workshop.skills import OVOSSkill

ROUNDS = 3


class QuizSkill(OVOSSkill):

    def initialize(self):
        self.playing = set()   # the sessions (devices, users) with a quiz going on

    def can_stop(self, message):
        """Asked when someone says "stop": is there a quiz to stop?"""
        return SessionManager.get(message).session_id in self.playing

    def stop_session(self, session):
        """Stop the quiz in this session; True: there was one."""
        if session.session_id in self.playing:
            self.playing.discard(session.session_id)
            return True
        return False

    def questions(self):
        """[(question, [answers])] from questions.list in the skill's language."""
        path = self.find_resource("questions.list", lang=self.lang)
        out = []
        for line in open(path, encoding="utf-8") if path else []:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 2 and not line.startswith("#"):
                out.append((parts[0], [a.lower() for a in parts[1:] if a]))
        return out

    @staticmethod
    def is_right(reply, answers):
        """The reply says one of the answers (as a word, not inside another word)."""
        words = " " + "".join(c if c.isalnum() else " " for c in (reply or "").lower()) + " "
        return any(f" {a} " in words for a in answers)

    @intent_handler("start.intent")
    def handle_start(self, message):
        """Someone wants to play: ask, listen, keep score."""
        session = SessionManager.get(message).session_id
        self.playing.add(session)
        try:
            self.quiz(session)
        finally:
            self.playing.discard(session)

    def quiz(self, session):
        """Rounds of questions until the answer to "again?" is not yes."""
        while True:
            asked = random.sample(self.questions(), min(ROUNDS, len(self.questions())))
            self.speak_dialog("intro", {"count": len(asked)}, wait=True)
            points = 0
            for question, answers in asked:
                reply = self.get_response(question, num_retries=0)
                if session not in self.playing:   # "stop"
                    return
                if reply is None:
                    self.speak_dialog("no_answer", {"answer": answers[0]}, wait=True)
                elif self.is_right(reply, answers):
                    points += 1
                    self.speak_dialog("right", wait=True)
                else:
                    self.speak_dialog("wrong", {"answer": answers[0]}, wait=True)
            self.speak_dialog("score", {"points": points, "total": len(asked)}, wait=True)
            if self.ask_yesno("again") != "yes" or session not in self.playing:
                self.speak_dialog("bye")
                return
