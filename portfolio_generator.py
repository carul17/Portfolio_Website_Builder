import json
import os
from typing import Dict, Any
from pathlib import Path

class PortfolioGenerator:
    def __init__(self):
        """Initialize the portfolio generator."""
        self.output_dir = "portfolio_website"
        from openai import OpenAI
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def load_resume_data(self, json_path: str) -> Dict[str, Any]:
        """Load parsed resume data from JSON file."""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Error loading resume data: {str(e)}")
    
    def generate_personalized_description(self, resume_data: Dict[str, Any], description_type: str = "hero") -> str:
        """Generate personalized description using LLM based on resume data."""
        # Extract key information for context
        personal_info = resume_data.get('personal_info', {})
        work_experience = resume_data.get('work_experience', resume_data.get('experience', []))
        projects = resume_data.get('projects', [])
        skills = resume_data.get('skills', [])
        education = resume_data.get('education', [])
        
        # Create context summary
        context = f"""
Resume Data Summary:
- Name: {personal_info.get('name', 'Professional')}
- Title/Position: {personal_info.get('title', personal_info.get('position', 'Professional'))}
- Work Experience: {len(work_experience)} positions
- Projects: {len(projects)} projects
- Skills: {skills if isinstance(skills, list) else list(skills.keys()) if isinstance(skills, dict) else []}
- Education: {len(education)} entries

Work Experience Details:
{json.dumps(work_experience[:2], indent=2) if work_experience else 'None'}

Recent Projects:
{json.dumps(projects[:2], indent=2) if projects else 'None'}
"""

        if description_type == "hero":
            prompt = f"""Based on the following resume data, write a compelling 1-2 sentence hero description for a portfolio website. 

REQUIREMENTS:
- Write in first person (use "I" not their name)
- Keep it general and high-level, don't mention specific projects or tools
- Only mention the current company they work for if applicable
- Use a confident, professional tone
- Focus on their role/field and general expertise
- Keep it concise and impactful (1-2 sentences max)
- Avoid clichés but can use phrases like "passionate about" if natural
- Don't use buzzwords or corporate speak

{context}

Write only the description, no quotes or extra text:"""
        
        else:  # about section
            prompt = f"""Based on the following resume data, write a personalized "About Me" section for a portfolio website.

REQUIREMENTS:
- Write 2-3 sentences that are specific to this person's background
- Mention actual technologies, companies, or projects from their experience
- Avoid generic phrases like "passion for innovation", "dedicated professional", "unique perspectives"
- Be conversational but professional
- Focus on concrete experience and skills
- Don't use meaningless filler words
- Make it sound human, not like an AI wrote it

{context}

Write only the about me text, no quotes or extra text:"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a professional copywriter who writes authentic, specific content that avoids clichés and generic language."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Warning: Could not generate personalized description: {str(e)}")
            # Fallback descriptions
            if description_type == "hero":
                return "Building software solutions and bringing ideas to life through code."
            else:
                return "I work with modern technologies to create software solutions that solve real problems."
    
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
        
        # Extract key information with fallbacks - focus on personal_info first
        personal_info = resume_data.get('personal_info', {})
        contact_info = resume_data.get('contact_info', {})
        contact = resume_data.get('contact', {})
        
        # Function to search for a value, prioritizing personal_info
        def find_value(keys):
            # First check personal_info (including nested contact)
            if isinstance(personal_info, dict):
                for key in keys:
                    if key in personal_info and personal_info[key]:
                        return personal_info[key]
                # Also check nested contact within personal_info
                if 'contact' in personal_info and isinstance(personal_info['contact'], dict):
                    for key in keys:
                        if key in personal_info['contact'] and personal_info['contact'][key]:
                            return personal_info['contact'][key]
            
            # Then check other sections
            for section in [contact_info, contact, resume_data]:
                if isinstance(section, dict):
                    for key in keys:
                        if key in section and section[key]:
                            return section[key]
            return ''
        
        name = find_value(['name', 'full_name', 'first_name', 'last_name'])
        if not name and 'first_name' in resume_data and 'last_name' in resume_data:
            name = f"{resume_data['first_name']} {resume_data['last_name']}"
        if not name:
            name = 'Professional Portfolio'
            
        title = find_value(['title', 'position', 'job_title', 'role', 'current_position'])
        if not title:
            title = 'Professional'
            
        email = find_value(['email', 'email_address', 'mail', 'e_mail'])
        phone = find_value(['phone', 'phone_number', 'mobile', 'cell', 'telephone'])
        location = find_value(['location', 'address', 'city', 'residence', 'based_in'])
        
        # Get social links from multiple possible locations
        linkedin = find_value(['linkedin', 'linkedin_url', 'linkedin_profile'])
        github = find_value(['github', 'github_url', 'github_profile'])
        website = find_value(['website', 'portfolio', 'personal_website', 'portfolio_url'])
        
        # Debug print to see what we found
        print(f"Debug - Found contact info: email='{email}', phone='{phone}', location='{location}'")
        print(f"Debug - personal_info keys: {list(personal_info.keys()) if personal_info else 'None'}")
        print(f"Debug - personal_info content: {personal_info}")
        print(f"Debug - Full resume_data keys: {list(resume_data.keys())}")
        
        # Get sections
        skills = resume_data.get('skills', [])
        work_experience = resume_data.get('work_experience', resume_data.get('experience', []))
        projects = resume_data.get('projects', [])
        education = resume_data.get('education', [])
        
        # Generate personalized descriptions
        print("Generating personalized descriptions...")
        hero_description = self.generate_personalized_description(resume_data, "hero")
        about_description = self.generate_personalized_description(resume_data, "about")
        
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
        html_content = html_content.replace('{{hero_description}}', hero_description)
        html_content = html_content.replace('{{about_description}}', about_description)
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
        print(f"Debug - Generating contact details with: email='{email}', phone='{phone}', location='{location}'")
        
        details = []
        if email and email.strip():
            details.append(f'<div class="contact-item"><i class="fas fa-envelope"></i><a href="mailto:{email}">{email}</a></div>')
            print(f"Debug - Added email: {email}")
        if phone and phone.strip():
            details.append(f'<div class="contact-item"><i class="fas fa-phone"></i><a href="tel:{phone}">{phone}</a></div>')
            print(f"Debug - Added phone: {phone}")
        if location and location.strip():
            details.append(f'<div class="contact-item"><i class="fas fa-map-marker-alt"></i><span>{location}</span></div>')
            print(f"Debug - Added location: {location}")
        
        # If no contact details found, return placeholder
        if not details:
            print("Debug - No contact details found, returning placeholder")
            return '<div class="contact-item"><i class="fas fa-info-circle"></i><span>Contact information will be displayed here</span></div>'
        
        result = ''.join(details)
        print(f"Debug - Final contact details HTML: {result}")
        return result
    
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
    
    def _format_date_range(self, dates) -> str:
        """Format date range from various formats."""
        if isinstance(dates, dict):
            start = dates.get('start', '')
            end = dates.get('end', '')
            if start and end:
                return f"{start} - {end}"
            elif start:
                return start
            elif end:
                return end
        elif isinstance(dates, str):
            return dates
        return str(dates) if dates else ''
    
    def _generate_experience_html(self, work_experience: list) -> str:
        """Generate HTML for work experience section."""
        if not work_experience:
            return '<div class="timeline-item"><h3>Experience details will be added soon.</h3></div>'
        
        html = ''
        for exp in work_experience:
            company = exp.get('company', 'Company')
            position = exp.get('position', exp.get('title', 'Position'))
            duration = self._format_date_range(exp.get('duration', exp.get('dates', '')))
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
    
    def _format_description(self, description) -> str:
        """Format project description as bullet points similar to work experience."""
        if isinstance(description, list):
            # Format as bullet points with same styling as work experience
            bullet_points = []
            for item in description:
                if item and str(item).strip():
                    cleaned_item = str(item).strip('[]"\'')
                    bullet_points.append(cleaned_item)
            return '</li><li>'.join(bullet_points) if bullet_points else ''
        elif isinstance(description, str):
            # Remove brackets and quotes, clean up the text
            cleaned = description.strip('[]"\'')
            # Split by common delimiters and create bullet points
            if '.' in cleaned and len(cleaned.split('.')) > 2:
                sentences = [s.strip() for s in cleaned.split('.') if s.strip()]
                return '</li><li>'.join([f'{sentence}.' for sentence in sentences])
            else:
                return cleaned
        return str(description) if description else ''
    
    def _generate_projects_html(self, projects: list) -> str:
        """Generate HTML for projects section."""
        if not projects:
            return '<div class="project-card"><h3>Projects will be showcased here.</h3></div>'
        
        html = ''
        for project in projects:
            name = project.get('name', project.get('title', 'Project'))
            description = self._format_description(project.get('description', ''))
            technologies = project.get('technologies', project.get('tech_stack', []))
            link = project.get('link', project.get('url', ''))
            github = project.get('github', project.get('repository', ''))
            
            if isinstance(technologies, list):
                tech_tags = ''.join([f'<span class="tech-tag">{tech}</span>' for tech in technologies])
            else:
                tech_tags = f'<span class="tech-tag">{technologies}</span>' if technologies else ''
            
            # Format description as bullet points if it exists
            description_html = ''
            if description:
                description_html = f'<div class="project-description"><ul><li>{description}</li></ul></div>'
            
            html += f'''
                <div class="project-card">
                    <div class="project-content">
                        <h3>{name}</h3>
                        {description_html}
                        <div class="tech-stack">
                            {tech_tags}
                        </div>
                        <div class="project-links">
                            {f'<a href="{github}" target="_blank" class="project-btn"><i class="fab fa-github"></i>GitHub</a>' if github else ''}
                            {f'<a href="{link}" target="_blank" class="project-btn"><i class="fab fa-github"></i>GitHub</a>' if link else ''}
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
            year = self._format_date_range(edu.get('year', edu.get('graduation_year', edu.get('dates', ''))))
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
        import webbrowser
        import os
        
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
        
        # Get absolute path to the HTML file
        html_file_path = os.path.abspath(f"{self.output_dir}/index.html")
        
        # Open the website in the default browser
        print("Opening portfolio website in browser...")
        webbrowser.open(f"file://{html_file_path}")
        
        print(f"Portfolio opened at: file://{html_file_path}")


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
