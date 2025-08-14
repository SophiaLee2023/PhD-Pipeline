# === SETUP ===
import openai
import pandas as pd
from tqdm import tqdm
import time
import os
import json
import csv

# === SETUP ===
openai.api_key = "teddy9 sent me his API key here like a fool :)"
input_csv_path = "input.csv"
output_csv_path = "./data/r1_universities.csv"
batch_size = 1
temperature = 1

# === LOAD DATA ===
df = pd.read_csv(input_csv_path, encoding="utf-8-sig")
if os.path.exists(output_csv_path):
    result_df = pd.read_csv(output_csv_path, encoding="utf-8-sig")
    last_processed_index = result_df.index[-1]
else:
    result_df = pd.DataFrame()
    last_processed_index = -1

# === JSON PARSER ===
def extract_structured_data(text):
    try:
        # Remove code block markdown if present
        if text.startswith("```json"):
            text = text.strip("```json").strip("` \n")
        elif text.startswith("```"):
            text = text.strip("```").strip("` \n")
        
        data = json.loads(text)
        return pd.DataFrame([data])
    except Exception as e:
        print(f"[!] JSON parsing failed: {e}")
        return pd.DataFrame([{"raw_response": text, "error": str(e)}])
    
client = openai.OpenAI(api_key=openai.api_key)
# === SYSTEM PROMPT ===
system_prompt = """
Follow instructions precisely as if you were a professional data analytics expert with proficiency in data entry and collection.
You will be provided with the name of an R1 university. Your task is to search for and retrieve links to the personel website of specific departments at that university. 
The departments to search for are the following, as defined by NSF:
Agricultural sciences
Natural resources and conservation
Biochemistry and biophysics
Biology and biomedical sciences, general
Bioinformatics, biostatistics, and computational biology
Cellular and developmental biology, and anatomy
Ecology, evolutionary biology, and epidemiology
Genetics and genomics
Microbiology and immunology
Molecular biology
Neurobiology and neurosciences
Pharmacology and toxicology
Physiology, pathology, and cancer biology
Computer science
Aerospace, aeronautical, and astronautical engineering
Bioengineering and biomedical engineering
Chemical and petroleum engineering
Civil, environmental, and transportation engineering
Electrical and computer engineering
Industrial engineering and operations research
Materials and mining engineering
Mechanical engineering
Geological sciences
Ocean, marine, and atmospheric sciences
Nursing science
Pharmaceutical sciences
Public health
Applied mathematics
Mathematics
Statistics
Astronomy and astrophysics
Chemistry
Physics
Clinical psychology
Counseling and applied psychology
Research and experimental psychology
Anthropology
Economics
Political science and government
Public policy analysis
Sociology, demography, and population studies
Business
Education leadership and administration
Education research
Teacher education and teaching fields
Education, other
Letters
Foreign languages and literature
History
Philosophy and religious studies
Music and performing arts
Communication
Public administration and social services

Note: If you cannot find a specific department at a specific university, please return NA for that department.
At the end, return only a valid JSON object containing the following fields (with lists for each element if applicable):
```json
{{
  "university": ["Example University"],
  "Agricultural sciences": ["NA"],
  "Natural resources and conservation": ["NA"],
  "Biochemistry and biophysics": ["NA"],
  "Biology and biomedical sciences, general": ["NA"],
  "Bioinformatics, biostatistics, and computational biology": ["NA"],
  "Cellular and developmental biology, and anatomy": ["NA"],
  "Ecology, evolutionary biology, and epidemiology": ["NA"],
  "Genetics and genomics": ["NA"],
  "Microbiology and immunology": ["NA"],
  "Molecular biology": ["NA"],
  "Neurobiology and neurosciences": ["NA"],
  "Pharmacology and toxicology": ["NA"],
  "Physiology, pathology, and cancer biology": ["NA"],
  "Computer science": ["NA"],
  "Aerospace, aeronautical, and astronautical engineering": ["NA"],
  "Bioengineering and biomedical engineering": ["NA"],
  "Chemical and petroleum engineering": ["NA"],
  "Civil, environmental, and transportation engineering": ["NA"],
  "Electrical and computer engineering": ["NA"],
  "Industrial engineering and operations research": ["NA"],
  "Materials and mining engineering": ["NA"],
  "Mechanical engineering": ["NA"],
  "Geological sciences": ["NA"],
  "Ocean, marine, and atmospheric sciences": ["NA"],
  "Nursing science": ["NA"],
  "Pharmaceutical sciences": ["NA"],
  "Public health": ["NA"],
  "Applied mathematics": ["NA"],
  "Mathematics": ["NA"],
  "Statistics": ["NA"],
  "Astronomy and astrophysics": ["NA"],
  "Chemistry": ["NA"],
  "Physics": ["NA"],
  "Clinical psychology": ["NA"],
  "Counseling and applied psychology": ["NA"],
  "Research and experimental psychology": ["NA"],
  "Anthropology": ["NA"],
  "Economics": ["NA"],
  "Political science and government": ["NA"],
  "Public policy analysis": ["NA"],
  "Sociology, demography, and population studies": ["NA"],
  "Business": ["NA"],
  "Education leadership and administration": ["NA"],
  "Education research": ["NA"],
  "Teacher education and teaching fields": ["NA"],
  "Education, other": ["NA"],
  "Letters": ["NA"],
  "Foreign languages and literature": ["NA"],
  "History": ["NA"],
  "Philosophy and religious studies": ["NA"],
  "Music and performing arts": ["NA"],
  "Communication": ["NA"],
  "Public administration and social services": ["NA"]
}}
"Respond with only the JSON object. Do not include explanations, prefaces, or markdown formatting."

"""

# === MAIN LOOP ===
for i in tqdm(range(last_processed_index + 1, len(df), batch_size), desc="Processing"):
    batch = df.iloc[i:i + batch_size]

    for idx, row in batch.iterrows():
        paragraph = row['Text']
        user_prompt = f"""Paragraph: {paragraph}"""

        try:
            response = client.chat.completions.create(
                model="gpt-5-2025-08-07",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
            )

            reply = response.choices[0].message.content
            print(f"\n--- Raw GPT Response ---\n{reply}\n------------------------\n")
            row_data = extract_structured_data(reply)
            result_df = pd.concat([result_df, row_data], ignore_index=True)

        except Exception as e:
            print(f"Error on row {idx}: {e}")
            continue

    # Save progress
    result_df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")