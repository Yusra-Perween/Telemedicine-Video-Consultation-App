from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
import os
import json

ai_bp = Blueprint('ai', __name__)

# ---------------------------------------------------------------------------
# Helper: call OpenAI chat completions
# ---------------------------------------------------------------------------
def _openai_chat(system_prompt: str, user_message: str) -> str:
    """Send a single-turn chat to OpenAI and return the reply text."""
    try:
        import openai
        openai.api_key = os.environ.get("OPENAI_API_KEY", "")
        if not openai.api_key:
            return "⚠️ OpenAI API key not configured. Please set OPENAI_API_KEY in your .env file."

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_message},
            ],
            temperature=0.4,
            max_tokens=600,
        )
        return response.choices[0].message.content.strip()
    except ImportError:
        return "⚠️ openai package not installed. Run: pip install openai"
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"


# ---------------------------------------------------------------------------
# 1. AI Symptom Checker
# ---------------------------------------------------------------------------
@ai_bp.route('/ai/symptom-checker', methods=['GET'])
def symptom_checker():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('ai_symptom_checker.html')


@ai_bp.route('/api/ai/symptom-check', methods=['POST'])
def api_symptom_check():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    symptoms = data.get('symptoms', '').strip()
    if not symptoms:
        return jsonify({'error': 'No symptoms provided'}), 400

    system_prompt = (
        "You are a helpful medical triage assistant. Based on the patient's symptoms, "
        "suggest (1) the most likely medical specialist they should consult, "
        "(2) 2-3 possible conditions (not a diagnosis), "
        "(3) immediate self-care tips, and "
        "(4) a warning if the symptoms suggest an emergency. "
        "Always remind the patient that this is not a medical diagnosis and they should see a doctor. "
        "Keep your response clear, friendly, and concise."
    )

    reply = _openai_chat(system_prompt, f"My symptoms are: {symptoms}")
    return jsonify({'result': reply})


# ---------------------------------------------------------------------------
# 2. AI Medical Report Summarizer
# ---------------------------------------------------------------------------
@ai_bp.route('/ai/report-summarizer', methods=['GET'])
def report_summarizer():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('ai_report_summarizer.html')


@ai_bp.route('/api/ai/summarize-report', methods=['POST'])
def api_summarize_report():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    report_text = data.get('report', '').strip()
    if not report_text:
        return jsonify({'error': 'No report text provided'}), 400

    system_prompt = (
        "You are a medical interpreter AI. A patient has shared their medical report. "
        "Summarize it in simple, plain English that a non-medical person can understand. "
        "Highlight: key findings, what they mean in plain terms, and any recommended next steps. "
        "Do NOT use medical jargon without explaining it. Keep it under 300 words."
    )

    reply = _openai_chat(system_prompt, f"Medical Report:\n{report_text}")
    return jsonify({'result': reply})


# ---------------------------------------------------------------------------
# 3. AI Doctor Notes Assistant
# ---------------------------------------------------------------------------
@ai_bp.route('/ai/notes-assistant', methods=['GET'])
def notes_assistant():
    if 'user_id' not in session or session.get('role') != 'doctor':
        return redirect(url_for('auth.login'))
    return render_template('ai_notes_assistant.html')


@ai_bp.route('/api/ai/expand-notes', methods=['POST'])
def api_expand_notes():
    if 'user_id' not in session or session.get('role') != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    brief_notes = data.get('notes', '').strip()
    if not brief_notes:
        return jsonify({'error': 'No notes provided'}), 400

    system_prompt = (
        "You are a professional medical documentation assistant. "
        "A doctor has provided brief consultation notes. "
        "Expand them into a well-structured, professional clinical note "
        "with sections: Chief Complaint, History of Present Illness, Assessment, and Plan. "
        "Use formal medical terminology where appropriate. Keep it accurate to the input."
    )

    reply = _openai_chat(system_prompt, f"Doctor's brief notes:\n{brief_notes}")
    return jsonify({'result': reply})
