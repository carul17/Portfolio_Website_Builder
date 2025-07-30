import json
import PyPDF2
from openai import OpenAI
import os
from typing import Dict, Any

class DynamicResumeParser:
    def __init__(self, api_key: str = None):
        """
        Initialize the dynamic resume parser with OpenAI API key.
        If no API key provided, will try to get from environment variable.
        """
        self.client = OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from PDF file."""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    def parse_resume_with_llm(self, resume_text: str) -> Dict[str, Any]:
        """
        Use LLM to parse resume text and create a structured JSON representation.
        The LLM will dynamically determine the appropriate structure based on the content.
        """
        prompt = f"""
You are an expert resume parser. Analyze the following resume text and extract ALL relevant information into a well-structured JSON format.

IMPORTANT INSTRUCTIONS:
1. Create a comprehensive JSON structure that captures ALL information present in the resume
2. Use appropriate nested objects and arrays where needed
3. Include sections like: personal_info, skills, work_experience, projects, education, certifications, etc.
4. For work experience and projects, include arrays of objects with relevant details
5. Extract dates, locations, descriptions, technologies used, achievements, etc.
6. If certain standard sections don't exist, don't include them
7. If there are unique sections specific to this resume, include them with appropriate names
8. Ensure all text is properly cleaned and formatted
9. Return ONLY valid JSON, no additional text or explanations

Resume text:
{resume_text}

JSON:"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a professional resume parser that outputs only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=4000
            )
            
            json_response = response.choices[0].message.content.strip()
            
            # Try to parse the JSON to ensure it's valid
            parsed_json = json.loads(json_response)
            return parsed_json
            
        except json.JSONDecodeError as e:
            raise Exception(f"LLM returned invalid JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"Error calling LLM API: {str(e)}")
    
    def parse_resume(self, pdf_path: str, output_path: str = None) -> Dict[str, Any]:
        """
        Main method to parse a resume PDF and return structured data.
        
        Args:
            pdf_path: Path to the PDF resume file
            output_path: Optional path to save the JSON output
            
        Returns:
            Dictionary containing structured resume data
        """
        print(f"Extracting text from {pdf_path}...")
        resume_text = self.extract_text_from_pdf(pdf_path)
        
        print("Parsing resume with LLM...")
        structured_data = self.parse_resume_with_llm(resume_text)
        
        if output_path:
            print(f"Saving structured data to {output_path}...")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(structured_data, f, indent=2, ensure_ascii=False)
        
        return structured_data
    
    def enhance_parsing(self, resume_text: str, specific_requirements: str = None) -> Dict[str, Any]:
        """
        Enhanced parsing with specific requirements or focus areas.
        
        Args:
            resume_text: The extracted resume text
            specific_requirements: Additional instructions for parsing
            
        Returns:
            Dictionary containing structured resume data
        """
        base_prompt = f"""
You are an expert resume parser. Analyze the following resume text and extract ALL relevant information into a well-structured JSON format.

IMPORTANT INSTRUCTIONS:
1. Create a comprehensive JSON structure that captures ALL information present in the resume
2. Use appropriate nested objects and arrays where needed
3. Include sections like: personal_info, skills, work_experience, projects, education, certifications, etc.
4. For work experience and projects, include arrays of objects with relevant details
5. Extract dates, locations, descriptions, technologies used, achievements, etc.
6. If certain standard sections don't exist, don't include them
7. If there are unique sections specific to this resume, include them with appropriate names
8. Ensure all text is properly cleaned and formatted
9. Return ONLY valid JSON, no additional text or explanations
"""
        
        if specific_requirements:
            base_prompt += f"\n\nADDITIONAL REQUIREMENTS:\n{specific_requirements}"
        
        base_prompt += f"\n\nResume text:\n{resume_text}\n\nJSON:"
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a professional resume parser that outputs only valid JSON."},
                    {"role": "user", "content": base_prompt}
                ],
                temperature=0.1,
                max_tokens=4000
            )
            
            json_response = response.choices[0].message.content.strip()
            parsed_json = json.loads(json_response)
            return parsed_json
            
        except json.JSONDecodeError as e:
            raise Exception(f"LLM returned invalid JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"Error calling LLM API: {str(e)}")


def main():
    """Example usage of the dynamic resume parser."""
    # Initialize parser (make sure OPENAI_API_KEY is set in environment)
    parser = DynamicResumeParser()
    
    # Example usage
    try:
        # Parse the resume
        result = parser.parse_resume(
            pdf_path="Callum_Arul_Resume.pdf",
            output_path="parsed_resume.json"
        )
        
        print("Resume parsed successfully!")
        print(f"Extracted {len(result)} main sections:")
        for key in result.keys():
            print(f"  - {key}")
            
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
