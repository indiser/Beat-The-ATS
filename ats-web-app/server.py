from flask import Flask, render_template, request
from ats_scanner import ATSScanner # Importing your logic
import os

app = Flask(__name__)
scanner = ATSScanner() # Initialize once to load NLTK/Models

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # 1. Get Data from Form
        job_description = request.form.get("job_description")
        uploaded_file = request.files.get("resume_file")
        
        if not job_description or not uploaded_file:
            return render_template("index.html", error="Please provide both a Job Description and a Resume.")

        # 2. Process the PDF (In memory, no saving to disk needed)
        # specific logic to save temp file if pypdf requires a path, 
        # or we can tweak scanner to accept a stream. 
        # For simplicity, we save temp file.
        temp_path = "temp_resume.pdf"
        uploaded_file.save(temp_path)
        
        try:
            resume_text = scanner.extract_text_from_resume(temp_path)
            
            # 3. Run Analysis
            keyword_match, matches, missing = scanner.scan(resume_text, job_description)
            cosine_match = scanner.calculate_cosine_similarity(resume_text, job_description)
            
            # 4. Determine Verdict
            if cosine_match >= 80:
                verdict = "🚀 Interview Likely"
                color = "success" # Green
            elif cosine_match >= 50:
                verdict = "⚠️ Application at Risk"
                color = "warning" # Yellow
            else:
                verdict = "🗑️ High Probability of Rejection"
                color = "danger"  # Red

            # 5. Render Results
            return render_template("index.html", 
                                   results=True,
                                   keyword_score=round(keyword_match, 1),
                                   ai_score=round(cosine_match, 1),
                                   missing_keywords=sorted(list(missing)),
                                   verdict=verdict,
                                   verdict_color=color)

        except Exception as e:
            return render_template("index.html", error=f"Error processing file: {e}")
        finally:
            # Cleanup temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)

    return render_template("index.html", results=False)

if __name__ == "__main__":
    app.run(debug=True)