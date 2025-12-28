import string
from PyPDF2 import PdfReader
import os


current_dir=os.path.dirname(os.path.abspath(__file__))

resume_file_path=os.path.join(current_dir,"resume.pdf")
job_description_file_path=os.path.join(current_dir,"job_description.txt")

class ATSScanner:
    def __init__(self):
        # A manual list of "Stop Words" (Words to ignore)
        # In a real app, you'd use NLTK or Spacy libraries for this.
        self.STOP_WORDS = {
            "and", "the", "is", "in", "at", "of", "or", "a", "an", "to", "for",
            "with", "on", "as", "by", "we", "are", "you", "your", "it", "be",
            "that", "which", "from", "this", "will", "can", "have", "has",
            "but", "not", "if", "job", "description", "resume", "work", "experience"
        }

    def clean_text(self, text):
        """
        1. Lowercases everything.
        2. Removes punctuation (.,!?:).
        3. Removes stop words.
        4. Returns a SET of unique keywords.
        """
        # Lowercase
        text = text.lower()
        
        # Remove punctuation using a translation table
        # This replaces every punctuation mark with None (deletes it)
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Split into a list of words
        words = text.split()
        
        # Filter out stop words and create a SET (Unique words only)
        # This is the secret sauce. Sets are instant to lookup.
        keywords = {word for word in words if word not in self.STOP_WORDS}
        
        return keywords
    
    def extract_text_from_resume(self,input_file):
        try:
            reader=PdfReader(input_file)
            text=""
            for page in reader.pages:
                text+=page.extract_text()
            return text
        except Exception as e:
            return f"Error:{e} has occurred"


    def scan(self, resume_text, job_desc_text):
        resume_set = self.clean_text(resume_text)
        jd_set = self.clean_text(job_desc_text)
        
        # 1. Calculate the Match
        # Intersection (&) finds words in BOTH sets
        matches = resume_set.intersection(jd_set)
        
        # 2. Calculate Missing Keywords
        # Difference (-) finds words in JD but NOT in Resume
        missing = jd_set.difference(resume_set)
        
        # 3. Calculate Score
        # (Matches / Total Unique JD Words) * 100
        if len(jd_set) == 0:
            return 0, set(), set()
            
        score = (len(matches) / len(jd_set)) * 100
        
        return score, matches, missing

# --- RUNNER CODE ---
if __name__ == "__main__":
    scanner = ATSScanner()
    
    print("--- ATS RESUME HACKER v1.0 ---")
    
    if resume_file_path.endswith(".pdf"):
        resume_input=scanner.extract_text_from_resume(input_file=resume_file_path)
    else:
        with open(resume_file_path,"rb") as filp:
            resume_input=filp.read()
    
    with open(job_description_file_path,"r",encoding="utf-8") as filp:
        jd_input=filp.read()

    # Run the Logic
    score, matches, missing = scanner.scan(resume_input, jd_input)
    
    # Output the Report
    print("\n" + "="*30)
    print(f"MATCH SCORE: {score:.1f}%")
    print("="*30)
    
    print(f"\n✅ MATCHED KEYWORDS ({len(matches)}):")
    print(", ".join(sorted(list(matches))))
    
    print(f"\n⚠️ MISSING CRITICAL KEYWORDS ({len(missing)}):")
    # We highlight these in RED using ANSI codes (Terminal hack)
    RED = "\033[91m"
    RESET = "\033[0m"
    
    for word in sorted(list(missing)):
        print(f"{RED}- {word}{RESET}")
        
    print("\n" + "="*30)
    
    if score < 50:
        print("Verdict: 🗑️  AUTO-REJECTED. You need to add the missing keywords.")
    elif score < 80:
        print("Verdict: ⚠️  MAYBE. Human might read it if lucky.")
    else:
        print("Verdict: 🚀  INTERVIEW LIKELY. Great job.")