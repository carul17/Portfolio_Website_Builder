# Resume Parser

A Python tool that extracts structured information from PDF resumes and stores it in JSON format for easy consumption by LLMs.

## Features

- Extracts contact information (name, email, phone, location, LinkedIn, GitHub)
- Parses skills organized by categories
- Extracts work experience with descriptions
- Parses projects with URLs and descriptions
- Extracts education details
- Parses certifications with descriptions
- Extracts extracurricular activities
- Outputs structured JSON data

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python resume_parser.py path/to/resume.pdf -o output.json
```

### Arguments

- `pdf_path`: Path to the PDF resume file (required)
- `-o, --output`: Output JSON file path (default: resume_data.json)

## Example

```bash
python resume_parser.py Callum_Arul_Resume.pdf -o callum_resume.json
```

## Output Format

The tool generates a JSON file with the following structure:

```json
{
  "contact_info": {
    "name": "Full Name",
    "location": "City, State",
    "phone": "+1 123 456 7890",
    "email": "email@example.com",
    "linkedin": "linkedin.com/in/profile",
    "github": "github.com/username"
  },
  "skills": {
    "Languages": ["Python", "Java", "C++"],
    "Frameworks": ["PyTorch", "TensorFlow"],
    "CloudOps": ["AWS", "GCP"]
  },
  "work_experience": [
    {
      "title": "Job Title",
      "company": "Company Name",
      "location": "Location",
      "duration": "Jan 2024 - Present",
      "description": ["Bullet point 1", "Bullet point 2"]
    }
  ],
  "projects": [
    {
      "name": "Project Name",
      "url": "github.com/project",
      "duration": "Jan 2024 - Feb 2024",
      "description": ["Project description bullets"]
    }
  ],
  "education": [
    {
      "institution": "University Name",
      "location": "City, State",
      "degree": "Bachelor of Science",
      "duration": "Sep 2018 - Dec 2023"
    }
  ],
  "certifications": [
    {
      "name": "Certification Name",
      "issuer": "Issuing Organization",
      "duration": "Jan 2024 - Feb 2024",
      "description": ["Certification details"]
    }
  ],
  "extracurriculars": [
    "Activity descriptions"
  ]
}
```

## LLM Integration

The structured JSON output is designed to be easily consumed by LLMs for tasks like:

- Resume analysis and scoring
- Job matching
- Skill gap analysis
- Interview question generation
- Resume summarization

The hierarchical structure allows LLMs to easily understand and process different sections of the resume.
