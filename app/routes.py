import json
import os
from datetime import datetime

from flask import Flask, redirect, render_template, request, url_for

from .analyzer import analyze_chat
from .models import get_reports, save_report

CHAT_PRESETS = {
    "chat1": {
        "label": "Chat 1: INDIRECT THREAT (Hard Case)",
        "messages": [
            "Why are you not replying?",
            "I've been watching you lately",
            "You go to college at 9 right?",
            "Don't make me do something bad",
        ],
    },
    "chat2": {
        "label": "Chat 2: MANIPULATIVE + EMOTIONAL ABUSE",
        "messages": [
            "I trusted you",
            "But you are just like others",
            "You are worthless",
            "No one will ever respect you",
        ],
    },
    "chat3": {
        "label": "Chat 3: MIXED CHAT (NORMAL + ABUSE)",
        "messages": [
            "Hey",
            "Did you finish the project?",
            "Also you are so dumb sometimes",
            "Anyway, see you tomorrow",
        ],
    },
    "chat4": {
        "label": "Chat 4: ESCALATION TRIGGER CASE",
        "messages": [
            "Send me your photo",
            "Why are you acting smart?",
            "I will leak your details online",
            "You will regret this",
        ],
    },
}


def register_routes(app: Flask) -> None:
    @app.get("/")
    def home():
        return redirect(url_for("chat"))

    @app.get("/chat")
    def chat():
        chat_id = request.args.get("chat_id", "chat1")
        if chat_id not in CHAT_PRESETS:
            chat_id = "chat1"

        chat_options = list(CHAT_PRESETS.items())
        messages = CHAT_PRESETS[chat_id]["messages"]
        return render_template(
            "chat.html",
            messages=messages,
            chat_options=chat_options,
            selected_chat_id=chat_id,
        )

    @app.post("/analyze")
    def analyze():
        chat_messages = request.form.getlist("messages")
        if not chat_messages:
            chat_messages = CHAT_PRESETS["chat1"]["messages"]

        result = analyze_chat(chat_messages)
        chat_text = "\n".join(chat_messages)

        # Save evidence snapshot as a simple text file (simulation of real-world reporting).
        evidence_dir = os.path.join(os.path.dirname(__file__), "..", "evidence")
        os.makedirs(evidence_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        evidence_filename = f"chat_{timestamp}.txt"
        evidence_path = os.path.join(evidence_dir, evidence_filename)
        with open(evidence_path, "w", encoding="utf-8") as f:
            f.write(chat_text)
        save_report(
            app.config["DATABASE"],
            chat_text,
            result["severity"],
            result["confidence"],
            result["suggestion"],
            json.dumps(result["line_results"]),
            evidence_filename,
        )

        return render_template(
            "result.html",
            severity=result["severity"],
            confidence=result["confidence"],
            suggestion=result["suggestion"],
            risk_score=result.get("risk_score"),
            risk_label=result.get("risk_label"),
            detected_phrases=result.get("detected_phrases", []),
            evidence_filename=evidence_filename,
            chat_messages=chat_messages,
            line_results=result["line_results"],
        )

    @app.get("/escalate")
    def escalate():
        message = "Escalation submitted (simulation): authorities have been notified."
        return render_template(
            "result.html",
            severity="High",
            confidence=100,
            risk_score=100,
            risk_label="Highly Unsafe",
            detected_phrases=[],
            suggestion=message,
            chat_messages=[],
            line_results=[],
        )

    @app.get("/admin")
    def admin():
        severity = request.args.get("severity", "All")
        reports = get_reports(app.config["DATABASE"], severity_filter=severity)
        return render_template("admin.html", reports=reports, selected=severity)
