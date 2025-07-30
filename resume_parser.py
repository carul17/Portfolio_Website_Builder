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
        
        # Find skills section - look for SKILLS header
        skills_match = re.search(r'SKILLS\s*\n(.*?)(?=\nWORK EXPERIENCE|\nEXPERIENCE|\nEDUCATION|\nPROJECTS|\Z)', text, re.DOTALL | re.IGNORECASE)
        if not skills_match:
            return skills
        
        skills_text = skills_match.group(1)
        lines = skills_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('•'):
                continue
            
            # Look for lines that start with bullet points or have category: format
            if ':' in line:
                parts = line.split(':', 1)
                category = parts[0].strip()
                # Remove any leading bullet or special characters
                category = re.sub(r'^[•\s]+', '', category)
                
                if len(parts) > 1 and parts[1].strip():
                    # Skills listed on same line after colon
                    skill_items = [item.strip() for item in parts[1].split(',') if item.strip()]
                    skills[category] = skill_items
        
        return skills
    
    def parse_work_experience(self, text: str) -> List[WorkExperience]:
        """Extract work experience"""
        experiences = []
        
        # Find work experience section
        work_match = re.search(r'WORK EXPERIENCE\s*\n(.*?)(?=\nPROJECTS|\nEDUCATION|\nSKILLS|\Z)', text, re.DOTALL | re.IGNORECASE)
        if not work_match:
            return experiences
        
        work_text = work_match.group(1)
        lines = work_text.split('\n')
        
        current_job = None
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            
            # Look for job title lines (followed by date on same line or next line)
            date_pattern = r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*?(\d{4}|Present)'
            
            if re.search(date_pattern, line):
                # This line contains a date - it's likely a job header
                if current_job:
                    experiences.append(current_job)
                
                # Split title and date
                date_match = re.search(date_pattern, line)
                duration = date_match.group(0) if date_match else ""
                title = re.sub(date_pattern, '', line).strip()
                
                # Look for company info in next line
                company = ""
                location = ""
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if next_line and not next_line.startswith('•'):
                        # Parse company and location from next line
                        company_parts = next_line.split()
                        if 'Remote' in next_line or 'Full-time' in next_line or 'Part-time' in next_line or 'Consultant' in next_line:
                            # Extract company before work type
                            work_type_match = re.search(r'(Remote|Full-time|Part-time|Contract|Consultant/Freelance)', next_line)
                            if work_type_match:
                                company = next_line[:work_type_match.start()].strip()
                                location = work_type_match.group(0)
                        else:
                            company = next_line
                        i += 1  # Skip the company line
                
                current_job = WorkExperience(
                    title=title,
                    company=company,
                    location=location,
                    duration=duration,
                    description=[]
                )
            
            elif line.startswith('•') and current_job:
                # This is a bullet point for the current job
                bullet_text = line[1:].strip()  # Remove bullet
                current_job.description.append(bullet_text)
            
            i += 1
        
        # Add the last job
        if current_job:
            experiences.append(current_job)
        
        return experiences
    
    def parse_projects(self, text: str) -> List[Project]:
        """Extract projects section"""
        projects = []
        
        # Find projects section
        projects_match = re.search(r'PROJECTS\s*\n(.*?)(?=\nEDUCATION|\nCERTIFICATIONS|\nEXTRACURRICULARS|\Z)', text, re.DOTALL | re.IGNORECASE)
        if not projects_match:
            return projects
        
        projects_text = projects_match.group(1)
        lines = projects_text.split('\n')
        
        current_project = None
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            
            # Look for project headers with | separator and dates
            if '|' in line and re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*?\d{4}', line):
                if current_project:
                    projects.append(current_project)
                
                # Parse project header: "Name | URL Date"
                parts = line.split('|')
                name = parts[0].strip()
                
                # Extract URL and date from second part
                url = ""
                duration = ""
                if len(parts) > 1:
                    second_part = parts[1].strip()
                    # Look for date pattern
                    date_match = re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*?\d{4}', second_part)
                    if date_match:
                        duration = date_match.group(0)
                        # URL is what's left after removing the date
                        url = second_part.replace(duration, '').strip()
                    else:
                        url = second_part
                
                current_project = Project(
                    name=name,
                    url=url,
                    duration=duration,
                    description=[]
                )
            
            elif line.startswith('•') and current_project:
                # This is a bullet point for the current project
                bullet_text = line[1:].strip()  # Remove bullet
                current_project.description.append(bullet_text)
            
            i += 1
        
        # Add the last project
        if current_project:
            projects.append(current_project)
        
        return projects
    
    def parse_education(self, text: str) -> List[Education]:
        """Extract education section"""
        education = []
        
        # Find education section
        edu_match = re.search(r'EDUCATION\s*\n(.*?)(?=\nCERTIFICATIONS|\nEXTRACURRICULARS|\Z)', text, re.DOTALL | re.IGNORECASE)
        if not edu_match:
            return education
        
        edu_text = edu_match.group(1)
        lines = edu_text.split('\n')
        
        current_edu = None
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            
            # Look for institution headers with | separator and dates
            if '|' in line and re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*?\d{4}', line):
                if current_edu:
                    education.append(current_edu)
                
                # Parse education header: "Institution | Location Date"
                parts = line.split('|')
                institution = parts[0].strip()
                
                # Extract location and date from second part
                location = ""
                duration = ""
                if len(parts) > 1:
                    second_part = parts[1].strip()
                    # Look for date pattern
                    date_match = re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*?\d{4}', second_part)
                    if date_match:
                        duration = date_match.group(0)
                        # Location is what's left after removing the date
                        location = second_part.replace(duration, '').strip().rstrip(',')
                    else:
                        location = second_part
                
                # Look for degree in next line
                degree = ""
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if next_line and not ('|' in next_line or re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)', next_line)):
                        degree = next_line
                        i += 1  # Skip the degree line
                
                current_edu = Education(
                    institution=institution,
                    location=location,
                    degree=degree,
                    duration=duration
                )
            
            i += 1
        
        # Add the last education entry
        if current_edu:
            education.append(current_edu)
        
        return education
    
    def parse_certifications(self, text: str) -> List[Certification]:
        """Extract certifications section"""
        certifications = []
        
        # Find certifications section
        cert_match = re.search(r'CERTIFICATIONS\s*\n(.*?)(?=\nEXTRACURRICULARS|\Z)', text, re.DOTALL | re.IGNORECASE)
        if not cert_match:
            return certifications
        
        cert_text = cert_match.group(1)
        lines = cert_text.split('\n')
        
        current_cert = None
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            
            # Look for certification headers with | separator and dates
            if '|' in line and re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*?\d{4}', line):
                if current_cert:
                    certifications.append(current_cert)
                
                # Parse certification header: "Name | Issuer Date"
                parts = line.split('|')
                name = parts[0].strip()
                
                # Extract issuer and date from second part
                issuer = ""
                duration = ""
                if len(parts) > 1:
                    second_part = parts[1].strip()
                    # Look for date pattern
                    date_match = re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*?\d{4}', second_part)
                    if date_match:
                        duration = date_match.group(0)
                        # Issuer is what's left after removing the date
                        issuer = second_part.replace(duration, '').strip()
                    else:
                        issuer = second_part
                
                current_cert = Certification(
                    name=name,
                    issuer=issuer,
                    duration=duration,
                    description=[]
                )
            
            elif line.startswith('•') and current_cert:
                # This is a bullet point for the current certification
                bullet_text = line[1:].strip()  # Remove bullet
                current_cert.description.append(bullet_text)
            
            i += 1
        
        # Add the last certification
        if current_cert:
            certifications.append(current_cert)
        
        return certifications
    
    def parse_extracurriculars(self, text: str) -> List[str]:
        """Extract extracurricular activities"""
        extracurriculars = []
        
        # Find extracurriculars section
        extra_match = re.search(r'EXTRACURRICULARS\s*\n(.*?)(?=\Z)', text, re.DOTALL | re.IGNORECASE)
        if not extra_match:
            return extracurriculars
        
        extra_text = extra_match.group(1)
        lines = extra_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('•'):
                # Extract bullet point text
                bullet_text = line[1:].strip()
                extracurriculars.append(bullet_text)
        
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
