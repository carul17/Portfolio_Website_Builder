import json
import os
from typing import Dict, Any
from pathlib import Path

class PortfolioGenerator:
    def __init__(self):
        """Initialize the portfolio generator."""
        self.output_dir = "portfolio_website"
    
    def load_resume_data(self, json_path: str) -> Dict[str, Any]:
        """Load parsed resume data from JSON file."""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Error loading resume data: {str(e)}")
    
    def create_directory_structure(self):
        """Create the directory structure for the portfolio website."""
        directories = [
            self.output_dir,
            f"{self.output_dir}/css",
            f"{self.output_dir}/js",
            f"{self.output_dir}/assets",
            "templates"  # Ensure templates directory exists
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def load_template(self, template_name: str) -> str:
        """Load template file content."""
        try:
            with open(f"templates/{template_name}", 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise Exception(f"Error loading template {template_name}: {str(e)}")
    
    def generate_html(self, resume_data: Dict[str, Any]) -> str:
        """Generate the main HTML file using template."""
        # Load HTML template
        html_template = self.load_template('index.html')
        
        # Extract key information with fallbacks
        personal_info = resume_data.get('personal_info', {})
        name = personal_info.get('name', 'Professional Portfolio')
        title = personal_info.get('title', personal_info.get('position', 'Professional'))
        email = personal_info.get('email', '')
        phone = personal_info.get('phone', '')
        location = personal_info.get('location', personal_info.get('address', ''))
        
        # Get social links
        linkedin = personal_info.get('linkedin', '')
        github = personal_info.get('github', '')
        website = personal_info.get('website', '')
        
        # Get sections
        skills = resume_data.get('skills', [])
        work_experience = resume_data.get('work_experience', resume_data.get('experience', []))
        projects = resume_data.get('projects', [])
        education = resume_data.get('education', [])
        
        # Generate component HTML
        social_links = self._generate_social_links(linkedin, github, website, email)
        about_details = self._generate_about_details(email, phone, location)
        experience_html = self._generate_experience_html(work_experience)
        projects_html = self._generate_projects_html(projects)
        skills_html = self._generate_skills_html(skills)
        education_section = self._generate_education_section(education)
        contact_details = self._generate_contact_details(email, phone, location)
        social_links_contact = self._generate_social_links_contact(linkedin, github, website)
        
        # Replace template placeholders
        html_content = html_template.replace('{{name}}', name)
        html_content = html_content.replace('{{nav_logo}}', name.split()[0] if name else 'Portfolio')
        html_content = html_content.replace('{{title}}', title)
        html_content = html_content.replace('{{title_lower}}', title.lower())
        html_content = html_content.replace('{{social_links}}', social_links)
        html_content = html_content.replace('{{about_details}}', about_details)
        html_content = html_content.replace('{{experience_html}}', experience_html)
        html_content = html_content.replace('{{projects_html}}', projects_html)
        html_content = html_content.replace('{{skills_html}}', skills_html)
        html_content = html_content.replace('{{education_section}}', education_section)
        html_content = html_content.replace('{{contact_details}}', contact_details)
        html_content = html_content.replace('{{social_links_contact}}', social_links_contact)
        
        return html_content
    
    def _generate_social_links(self, linkedin: str, github: str, website: str, email: str) -> str:
        """Generate social links HTML for hero section."""
        links = []
        if linkedin:
            links.append(f'<a href="{linkedin}" target="_blank"><i class="fab fa-linkedin"></i></a>')
        if github:
            links.append(f'<a href="{github}" target="_blank"><i class="fab fa-github"></i></a>')
        if website:
            links.append(f'<a href="{website}" target="_blank"><i class="fas fa-globe"></i></a>')
        if email:
            links.append(f'<a href="mailto:{email}"><i class="fas fa-envelope"></i></a>')
        return ''.join(links)
    
    def _generate_about_details(self, email: str, phone: str, location: str) -> str:
        """Generate about details HTML."""
        details = []
        if email:
            details.append(f'<div class="detail-item"><i class="fas fa-envelope"></i><span>{email}</span></div>')
        if phone:
            details.append(f'<div class="detail-item"><i class="fas fa-phone"></i><span>{phone}</span></div>')
        if location:
            details.append(f'<div class="detail-item"><i class="fas fa-map-marker-alt"></i><span>{location}</span></div>')
        return ''.join(details)
    
    def _generate_contact_details(self, email: str, phone: str, location: str) -> str:
        """Generate contact details HTML."""
        details = []
        if email:
            details.append(f'<div class="contact-item"><i class="fas fa-envelope"></i><a href="mailto:{email}">{email}</a></div>')
        if phone:
            details.append(f'<div class="contact-item"><i class="fas fa-phone"></i><a href="tel:{phone}">{phone}</a></div>')
        if location:
            details.append(f'<div class="contact-item"><i class="fas fa-map-marker-alt"></i><span>{location}</span></div>')
        return ''.join(details)
    
    def _generate_social_links_contact(self, linkedin: str, github: str, website: str) -> str:
        """Generate social links HTML for contact section."""
        links = []
        if linkedin:
            links.append(f'<a href="{linkedin}" target="_blank" class="social-btn"><i class="fab fa-linkedin"></i>LinkedIn</a>')
        if github:
            links.append(f'<a href="{github}" target="_blank" class="social-btn"><i class="fab fa-github"></i>GitHub</a>')
        if website:
            links.append(f'<a href="{website}" target="_blank" class="social-btn"><i class="fas fa-globe"></i>Website</a>')
        return ''.join(links)
    
    def _generate_experience_html(self, work_experience: list) -> str:
        """Generate HTML for work experience section."""
        if not work_experience:
            return '<div class="timeline-item"><h3>Experience details will be added soon.</h3></div>'
        
        html = ''
        for exp in work_experience:
            company = exp.get('company', 'Company')
            position = exp.get('position', exp.get('title', 'Position'))
            duration = exp.get('duration', exp.get('dates', ''))
            location = exp.get('location', '')
            description = exp.get('description', exp.get('responsibilities', ''))
            
            if isinstance(description, list):
                description = '</li><li>'.join(description)
                description = f'<ul><li>{description}</li></ul>'
            
            html += f'''
                <div class="timeline-item">
                    <div class="timeline-marker"></div>
                    <div class="timeline-content">
                        <h3>{position}</h3>
                        <h4>{company}</h4>
                        <div class="timeline-meta">
                            <span class="duration">{duration}</span>
                            {f'<span class="location">{location}</span>' if location else ''}
                        </div>
                        <div class="timeline-description">
                            {description}
                        </div>
                    </div>
                </div>
            '''
        return html
    
    def _generate_projects_html(self, projects: list) -> str:
        """Generate HTML for projects section."""
        if not projects:
            return '<div class="project-card"><h3>Projects will be showcased here.</h3></div>'
        
        html = ''
        for project in projects:
            name = project.get('name', project.get('title', 'Project'))
            description = project.get('description', '')
            technologies = project.get('technologies', project.get('tech_stack', []))
            link = project.get('link', project.get('url', ''))
            github = project.get('github', project.get('repository', ''))
            
            if isinstance(technologies, list):
                tech_tags = ''.join([f'<span class="tech-tag">{tech}</span>' for tech in technologies])
            else:
                tech_tags = f'<span class="tech-tag">{technologies}</span>' if technologies else ''
            
            html += f'''
                <div class="project-card">
                    <div class="project-content">
                        <h3>{name}</h3>
                        <p>{description}</p>
                        <div class="tech-stack">
                            {tech_tags}
                        </div>
                        <div class="project-links">
                            {f'<a href="{link}" target="_blank" class="project-btn"><i class="fas fa-external-link-alt"></i>Live Demo</a>' if link else ''}
                            {f'<a href="{github}" target="_blank" class="project-btn"><i class="fab fa-github"></i>Code</a>' if github else ''}
                        </div>
                    </div>
                </div>
            '''
        return html
    
    def _generate_skills_html(self, skills: list) -> str:
        """Generate HTML for skills section."""
        if not skills:
            return '<div class="skill-category"><h3>Skills will be displayed here.</h3></div>'
        
        # Handle different skill formats
        if isinstance(skills, dict):
            html = ''
            for category, skill_list in skills.items():
                if isinstance(skill_list, list):
                    skill_items = ''.join([f'<span class="skill-item">{skill}</span>' for skill in skill_list])
                else:
                    skill_items = f'<span class="skill-item">{skill_list}</span>'
                
                html += f'''
                    <div class="skill-category">
                        <h3>{category.replace('_', ' ').title()}</h3>
                        <div class="skill-items">
                            {skill_items}
                        </div>
                    </div>
                '''
            return html
        elif isinstance(skills, list):
            skill_items = ''.join([f'<span class="skill-item">{skill}</span>' for skill in skills])
            return f'''
                <div class="skill-category">
                    <h3>Technical Skills</h3>
                    <div class="skill-items">
                        {skill_items}
                    </div>
                </div>
            '''
        else:
            return f'<div class="skill-category"><div class="skill-items"><span class="skill-item">{skills}</span></div></div>'
    
    def _generate_education_section(self, education: list) -> str:
        """Generate HTML for education section."""
        if not education:
            return ''
        
        html = '''
    <section id="education" class="education">
        <div class="container">
            <h2 class="section-title">Education</h2>
            <div class="education-grid">
        '''
        
        for edu in education:
            degree = edu.get('degree', edu.get('qualification', 'Degree'))
            institution = edu.get('institution', edu.get('school', edu.get('university', 'Institution')))
            year = edu.get('year', edu.get('graduation_year', edu.get('dates', '')))
            gpa = edu.get('gpa', '')
            
            html += f'''
                <div class="education-card">
                    <h3>{degree}</h3>
                    <h4>{institution}</h4>
                    <div class="education-meta">
                        <span class="year">{year}</span>
                        {f'<span class="gpa">GPA: {gpa}</span>' if gpa else ''}
                    </div>
                </div>
            '''
        
        html += '''
            </div>
        </div>
    </section>
        '''
        return html
    
    def generate_css(self) -> str:
        """Generate the CSS file using template."""
        return self.load_template('style.css')
    
    def generate_js(self) -> str:
        """Generate the JavaScript file using template."""
        return self.load_template('script.js')
    
    def generate_portfolio(self, json_path: str):
        """Generate the complete portfolio website."""
        print("Loading resume data...")
        resume_data = self.load_resume_data(json_path)
        
        print("Creating directory structure...")
        self.create_directory_structure()
        
        print("Generating HTML...")
        html_content = self.generate_html(resume_data)
        with open(f"{self.output_dir}/index.html", 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("Generating CSS...")
        css_content = self.generate_css()
        with open(f"{self.output_dir}/css/style.css", 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        print("Generating JavaScript...")
        js_content = self.generate_js()
        with open(f"{self.output_dir}/js/script.js", 'w', encoding='utf-8') as f:
            f.write(js_content)
        
        print(f"Portfolio website generated successfully in '{self.output_dir}' directory!")
        print(f"Open '{self.output_dir}/index.html' in your browser to view the portfolio.")


def main():
    """Main function to generate portfolio from parsed resume."""
    import sys
    
    generator = PortfolioGenerator()
    
    # Check if resume JSON file is provided as argument
    json_file = "parsed_resume.json"
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    
    try:
        # Generate portfolio from parsed resume JSON
        generator.generate_portfolio(json_file)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print(f"Make sure you have a '{json_file}' file from the resume parser.")
        print("Usage: uv run portfolio_generator.py [resume_json_file]")


if __name__ == "__main__":
    main()
