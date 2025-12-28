import string
from PyPDF2 import PdfReader
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

current_dir=os.path.dirname(os.path.abspath(__file__))

resume_file_path=os.path.join(current_dir,"resume.pdf")
job_description_file_path=os.path.join(current_dir,"job_description.txt")

class ATSScanner:
    def __init__(self):
        
        try:
            nltk.data.find('corpora/stopwords')
            nltk.data.find('tokenizers/punkt')
        except:
            print("Downloading nltk datapackages..")
            nltk.download('stopwords')
            nltk.download('punkt')
            nltk.download('punkt_tab')
        
        self.stemmer=PorterStemmer()
        boilerplate = {
            "job", "title", "candidate", "description", "responsibilities", 
            "requirements", "summary", "seeking", "ideal", "must", "key", 
            "preferred", "previous", "prior", "professional", "program", 
            "dedicated", "diverse", "assist", "support", "work", "role",
            "experience", "position", "qualifications", "skills"
        }
        self.stop_words=set(stopwords.words("english")).union(boilerplate)

    def clean_text(self, text):
        # Lowercase
        text = text.lower()
        
        words=word_tokenize(text)
        cleaned_word=set()

        for word in words:
            if not word.isalpha():
                continue
            if word in self.stop_words:
                continue

            root_words=self.stemmer.stem(word)
            cleaned_word.add(root_words)
        
        return cleaned_word
    
    def extract_text_from_resume(self,input_file):
        try:
            reader=PdfReader(input_file)
            text=""
            for page in reader.pages:
                text+=page.extract_text()
            return text
        except Exception as e:
            return f"Error:{e} has occurred"
        
    def calculate_cosine_similarity(self, resume_text, jd_text):
        """
        Converts text to Vectors and calculates the Cosine Similarity.
        This is much smarter than simple keyword matching.
        """
        # 1. Clean both texts first (using your existing cleaner)
        # We join the set back into a string because CountVectorizer expects strings
        resume_cleaned = " ".join(self.clean_text(resume_text))
        jd_cleaned = " ".join(self.clean_text(jd_text))
        
        text_list = [resume_cleaned, jd_cleaned]
        
        # 2. Vectorize (Turn words into math)
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(text_list)
        
        # 3. Calculate Similarity (0.0 to 1.0)
        match_percentage = cosine_similarity(count_matrix)[0][1] * 100
        
        return round(match_percentage, 2)

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
    
    print("--- ATS RESUME HACKER v3.0 ---")
    
    if resume_file_path.endswith(".pdf"):
        resume_input=scanner.extract_text_from_resume(input_file=resume_file_path)
    else:
        with open(resume_file_path,"rb") as filp:
            resume_input=filp.read()
    
    with open(job_description_file_path,"r",encoding="utf-8") as filp:
        jd_input=filp.read()

    # Run the Logic
    score, matches, missing = scanner.scan(resume_input, jd_input)
    cosine_score = scanner.calculate_cosine_similarity(resume_input, jd_input)

    # Output the Report
    print("\n" + "="*30)
    print(f"MATCH SCORE: {score:.1f}%")
    print(f"COSINE (AI) SCORE:   {cosine_score:.1f}%")
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
    
    if cosine_score < 50:
        print("Verdict: 🗑️  AUTO-REJECTED. You need to add the missing keywords.")
    elif score < 80:
        print("Verdict: ⚠️  MAYBE. Human might read it if lucky.")
    else:
        print("Verdict: 🚀  INTERVIEW LIKELY. Great job.")