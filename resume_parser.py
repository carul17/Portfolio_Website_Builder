import PyPDF2
import json
import re
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import argparse

@dataclass
class ContactInfo:
    name: str = ""
    location: str = ""
    phone: str = ""
    email: str = ""
    linkedin: str = ""
    github: str = ""

@dataclass
class WorkExperience:
    title: str
    company: str
    location: str
    duration: str
    description: List[str]

@dataclass
class Project:
    name: str
    url: str
    duration: str
    description: List[str]

@dataclass
class Education:
    institution: str
    location: str
    degree: str
    duration: str

@dataclass
class Certification:
    name: str
    issuer: str
    duration: str
    description: List[str]

@dataclass
class ResumeData:
    contact_info: ContactInfo
    skills: Dict[str, List[str]]
    work_experience: List[WorkExperience]
    projects: List[Project]
    education: List[Education]
    certifications: List[Certification]
    extracurriculars: List[str]

class ResumeParser:
    def __init__(self):
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'\+?1?\s*\(?(\d{3})\)?[-.\s]*(\d{3})[-.\s]*(\d{4})'
        self.url_pattern = r'https?://[^\s]+|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?'
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    def parse_contact_info(self, text: str) -> ContactInfo:
        """Extract contact information from resume text"""
        lines = text.split('\n')
        contact = ContactInfo()
        
        # Extract name (usually first non-empty line)
        for line in lines:
            line = line.strip()
            if line and not any(char.isdigit() for char in line) and len(line.split()) <= 3:
                contact.name = line
                break
        
        # Extract email
        email_match = re.search(self.email_pattern, text)
        if email_match:
            contact.email = email_match.group()
        
        # Extract phone
        phone_match = re.search(self.phone_pattern, text)
        if phone_match:
            contact.phone = phone_match.group()
        
        # Extract location (look for patterns like "City, State" or "City, Province")
        location_pattern = r'([A-Za-z\s]+,\s*[A-Z]{2,3}(?:\s*,\s*[A-Za-z\s]+)?)'
        location_match = re.search(location_pattern, text)
        if location_match:
            contact.location = location_match.group().strip()
        
        # Extract LinkedIn and GitHub
        urls = re.findall(self.url_pattern, text, re.IGNORECASE)
        for url in urls:
            if 'linkedin' in url.lower():
                contact.linkedin = url
            elif 'github' in url.lower():
                contact.github = url
        
        return contact
    
    def parse_skills(self, text: str) -> Dict[str, List[str]]:
        """Extract skills section"""
        skills = {}
        
        # Find skills section
        skills_match = re.search(r'SKILLS\s*\n(.*?)(?=\n[A-Z\s]+\n|\Z)', text, re.DOTALL | re.IGNORECASE)
        if not skills_match:
            return skills
        
        skills_text = skills_match.group(1)
        lines = skills_text.split('\n')
        
        current_category = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line is a category (ends with colon)
            if ':' in line and not line.startswith('•'):
                parts = line.split(':', 1)
                current_category = parts[0].strip()
                if len(parts) > 1 and parts[1].strip():
                    # Skills listed on same line
                    skill_items = [item.strip() for item in parts[1].split(',')]
                    skills[current_category] = skill_items
            elif current_category and line:
                # Skills on separate lines
                if current_category not in skills:
                    skills[current_category] = []
                skill_items = [item.strip() for item in line.split(',')]
                skills[current_category].extend(skill_items)
        
        return skills
    
    def parse_work_experience(self, text: str) -> List[WorkExperience]:
        """Extract work experience"""
        experiences = []
        
        # Find work experience section
        work_match = re.search(r'WORK EXPERIENCE\s*\n(.*?)(?=\n[A-Z\s]+\n|\Z)', text, re.DOTALL | re.IGNORECASE)
        if not work_match:
            return experiences
        
        work_text = work_match.group(1)
        
        # Split by job entries (look for patterns like "Title Date" or "Title Company Date")
        job_pattern = r'([A-Za-z\s\-&]+?)\s+((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*?(?:Present|\d{4}))\s*\n([A-Za-z\s,]+?)(?:\s+(Remote|Full-time|Part-time|Contract|Consultant/Freelance).*?)?\s*\n'
        
        jobs = re.finditer(job_pattern, work_text, re.MULTILINE)
        
        for job in jobs:
            title = job.group(1).strip()
            duration = job.group(2).strip()
            company_location = job.group(3).strip()
            
            # Parse company and location
            company_parts = company_location.split()
            if len(company_parts) >= 2:
                company = company_parts[0]
                location = ' '.join(company_parts[1:])
            else:
                company = company_location
                location = ""
            
            # Find description bullets for this job
            job_end = job.end()
            next_job = re.search(job_pattern, work_text[job_end:])
            if next_job:
                desc_text = work_text[job_end:job_end + next_job.start()]
            else:
                desc_text = work_text[job_end:]
            
            # Extract bullet points
            bullets = re.findall(r'•\s*(.+)', desc_text)
            
            experiences.append(WorkExperience(
                title=title,
                company=company,
                location=location,
                duration=duration,
                description=bullets
            ))
        
        return experiences
    
    def parse_projects(self, text: str) -> List[Project]:
        """Extract projects section"""
        projects = []
        
        # Find projects section
        projects_match = re.search(r'PROJECTS\s*\n(.*?)(?=\n[A-Z\s]+\n|\Z)', text, re.DOTALL | re.IGNORECASE)
        if not projects_match:
            return projects
        
        projects_text = projects_match.group(1)
        
        # Split by project entries
        project_pattern = r'([A-Za-z\s\-&]+?)\s*\|\s*([^\s]+)\s+((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*?(?:\d{4}))\s*\n'
        
        project_matches = list(re.finditer(project_pattern, projects_text, re.MULTILINE))
        
        for i, project in enumerate(project_matches):
            name = project.group(1).strip()
            url = project.group(2).strip()
            duration = project.group(3).strip()
            
            # Find description for this project
            project_end = project.end()
            if i + 1 < len(project_matches):
                next_project_start = project_matches[i + 1].start()
                desc_text = projects_text[project_end:next_project_start]
            else:
                desc_text = projects_text[project_end:]
            
            # Extract bullet points
            bullets = re.findall(r'•\s*(.+)', desc_text)
            
            projects.append(Project(
                name=name,
                url=url,
                duration=duration,
                description=bullets
            ))
        
        return projects
    
    def parse_education(self, text: str) -> List[Education]:
        """Extract education section"""
        education = []
        
        # Find education section
        edu_match = re.search(r'EDUCATION\s*\n(.*?)(?=\n[A-Z\s]+\n|\Z)', text, re.DOTALL | re.IGNORECASE)
        if not edu_match:
            return education
        
        edu_text = edu_match.group(1)
        
        # Parse education entries
        edu_pattern = r'([A-Za-z\s]+?)\s*\|\s*([A-Za-z\s,]+?)\s+((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*?(?:\d{4}))\s*\n([A-Za-z\s,.]+)'
        
        edu_matches = re.finditer(edu_pattern, edu_text, re.MULTILINE)
        
        for edu in edu_matches:
            institution = edu.group(1).strip()
            location = edu.group(2).strip()
            duration = edu.group(3).strip()
            degree = edu.group(4).strip()
            
            education.append(Education(
                institution=institution,
                location=location,
                degree=degree,
                duration=duration
            ))
        
        return education
    
    def parse_certifications(self, text: str) -> List[Certification]:
        """Extract certifications section"""
        certifications = []
        
        # Find certifications section
        cert_match = re.search(r'CERTIFICATIONS\s*\n(.*?)(?=\n[A-Z\s]+\n|\Z)', text, re.DOTALL | re.IGNORECASE)
        if not cert_match:
            return certifications
        
        cert_text = cert_match.group(1)
        
        # Parse certification entries
        cert_pattern = r'([A-Za-z\s\-()]+?)\s*\|\s*([A-Za-z\s()]+?)\s+((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*?(?:\d{4}))\s*\n'
        
        cert_matches = list(re.finditer(cert_pattern, cert_text, re.MULTILINE))
        
        for i, cert in enumerate(cert_matches):
            name = cert.group(1).strip()
            issuer = cert.group(2).strip()
            duration = cert.group(3).strip()
            
            # Find description for this certification
            cert_end = cert.end()
            if i + 1 < len(cert_matches):
                next_cert_start = cert_matches[i + 1].start()
                desc_text = cert_text[cert_end:next_cert_start]
            else:
                desc_text = cert_text[cert_end:]
            
            # Extract bullet points
            bullets = re.findall(r'•\s*(.+)', desc_text)
            
            certifications.append(Certification(
                name=name,
                issuer=issuer,
                duration=duration,
                description=bullets
            ))
        
        return certifications
    
    def parse_extracurriculars(self, text: str) -> List[str]:
        """Extract extracurricular activities"""
        extracurriculars = []
        
        # Find extracurriculars section
        extra_match = re.search(r'EXTRACURRICULARS\s*\n(.*?)(?=\Z)', text, re.DOTALL | re.IGNORECASE)
        if not extra_match:
            return extracurriculars
        
        extra_text = extra_match.group(1)
        
        # Extract bullet points
        bullets = re.findall(r'•\s*(.+)', extra_text)
        extracurriculars.extend(bullets)
        
        return extracurriculars
    
    def parse_resume(self, pdf_path: str) -> ResumeData:
        """Parse entire resume from PDF"""
        text = self.extract_text_from_pdf(pdf_path)
        
        return ResumeData(
            contact_info=self.parse_contact_info(text),
            skills=self.parse_skills(text),
            work_experience=self.parse_work_experience(text),
            projects=self.parse_projects(text),
            education=self.parse_education(text),
            certifications=self.parse_certifications(text),
            extracurriculars=self.parse_extracurriculars(text)
        )
    
    def save_to_json(self, resume_data: ResumeData, output_path: str):
        """Save parsed resume data to JSON file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(resume_data), f, indent=2, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser(description='Parse resume PDF and extract structured data')
    parser.add_argument('pdf_path', help='Path to the PDF resume file')
    parser.add_argument('-o', '--output', default='resume_data.json', help='Output JSON file path')
    
    args = parser.parse_args()
    
    resume_parser = ResumeParser()
    
    try:
        print(f"Parsing resume from: {args.pdf_path}")
        resume_data = resume_parser.parse_resume(args.pdf_path)
        
        print(f"Saving structured data to: {args.output}")
        resume_parser.save_to_json(resume_data, args.output)
        
        print("Resume parsing completed successfully!")
        print(f"Extracted data for: {resume_data.contact_info.name}")
        
    except Exception as e:
        print(f"Error parsing resume: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
