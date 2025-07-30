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
            f"{self.output_dir}/assets"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def generate_html(self, resume_data: Dict[str, Any]) -> str:
        """Generate the main HTML file."""
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
        
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - Portfolio</title>
    <link rel="stylesheet" href="css/style.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-logo">
                <a href="#home">{name.split()[0] if name else 'Portfolio'}</a>
            </div>
            <div class="nav-menu" id="nav-menu">
                <a href="#home" class="nav-link">Home</a>
                <a href="#about" class="nav-link">About</a>
                <a href="#experience" class="nav-link">Experience</a>
                <a href="#projects" class="nav-link">Projects</a>
                <a href="#skills" class="nav-link">Skills</a>
                <a href="#contact" class="nav-link">Contact</a>
            </div>
            <div class="hamburger" id="hamburger">
                <span class="bar"></span>
                <span class="bar"></span>
                <span class="bar"></span>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section id="home" class="hero">
        <div class="hero-container">
            <div class="hero-content">
                <h1 class="hero-title">
                    <span class="greeting">Hello, I'm</span>
                    <span class="name">{name}</span>
                </h1>
                <p class="hero-subtitle">{title}</p>
                <p class="hero-description">
                    Passionate professional dedicated to creating innovative solutions and driving meaningful impact.
                </p>
                <div class="hero-buttons">
                    <a href="#contact" class="btn btn-primary">Get In Touch</a>
                    <a href="#projects" class="btn btn-secondary">View My Work</a>
                </div>
                <div class="social-links">
                    {f'<a href="{linkedin}" target="_blank"><i class="fab fa-linkedin"></i></a>' if linkedin else ''}
                    {f'<a href="{github}" target="_blank"><i class="fab fa-github"></i></a>' if github else ''}
                    {f'<a href="{website}" target="_blank"><i class="fas fa-globe"></i></a>' if website else ''}
                    {f'<a href="mailto:{email}"><i class="fas fa-envelope"></i></a>' if email else ''}
                </div>
            </div>
        </div>
        <div class="scroll-indicator">
            <div class="scroll-arrow"></div>
        </div>
    </section>

    <!-- About Section -->
    <section id="about" class="about">
        <div class="container">
            <h2 class="section-title">About Me</h2>
            <div class="about-content">
                <div class="about-text">
                    <p>
                        I am a dedicated {title.lower()} with a passion for innovation and excellence. 
                        My experience spans across various technologies and domains, allowing me to bring 
                        unique perspectives to every project I work on.
                    </p>
                    <div class="about-details">
                        {f'<div class="detail-item"><i class="fas fa-envelope"></i><span>{email}</span></div>' if email else ''}
                        {f'<div class="detail-item"><i class="fas fa-phone"></i><span>{phone}</span></div>' if phone else ''}
                        {f'<div class="detail-item"><i class="fas fa-map-marker-alt"></i><span>{location}</span></div>' if location else ''}
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Experience Section -->
    <section id="experience" class="experience">
        <div class="container">
            <h2 class="section-title">Work Experience</h2>
            <div class="timeline">
                {self._generate_experience_html(work_experience)}
            </div>
        </div>
    </section>

    <!-- Projects Section -->
    <section id="projects" class="projects">
        <div class="container">
            <h2 class="section-title">Featured Projects</h2>
            <div class="projects-grid">
                {self._generate_projects_html(projects)}
            </div>
        </div>
    </section>

    <!-- Skills Section -->
    <section id="skills" class="skills">
        <div class="container">
            <h2 class="section-title">Skills & Technologies</h2>
            <div class="skills-container">
                {self._generate_skills_html(skills)}
            </div>
        </div>
    </section>

    <!-- Education Section -->
    {self._generate_education_section(education)}

    <!-- Contact Section -->
    <section id="contact" class="contact">
        <div class="container">
            <h2 class="section-title">Let's Connect</h2>
            <div class="contact-content">
                <div class="contact-info">
                    <h3>Get In Touch</h3>
                    <p>I'm always interested in new opportunities and collaborations.</p>
                    <div class="contact-details">
                        {f'<div class="contact-item"><i class="fas fa-envelope"></i><a href="mailto:{email}">{email}</a></div>' if email else ''}
                        {f'<div class="contact-item"><i class="fas fa-phone"></i><a href="tel:{phone}">{phone}</a></div>' if phone else ''}
                        {f'<div class="contact-item"><i class="fas fa-map-marker-alt"></i><span>{location}</span></div>' if location else ''}
                    </div>
                    <div class="social-links-contact">
                        {f'<a href="{linkedin}" target="_blank" class="social-btn"><i class="fab fa-linkedin"></i>LinkedIn</a>' if linkedin else ''}
                        {f'<a href="{github}" target="_blank" class="social-btn"><i class="fab fa-github"></i>GitHub</a>' if github else ''}
                        {f'<a href="{website}" target="_blank" class="social-btn"><i class="fas fa-globe"></i>Website</a>' if website else ''}
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <p>&copy; 2024 {name}. All rights reserved.</p>
        </div>
    </footer>

    <script src="js/script.js"></script>
</body>
</html>'''
        return html_content
    
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
        """Generate the CSS file."""
        return '''/* Reset and Base Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

body {
    font-family: 'Inter', sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #ffffff;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Navigation */
.navbar {
    position: fixed;
    top: 0;
    width: 100%;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    z-index: 1000;
    padding: 1rem 0;
    transition: all 0.3s ease;
}

.nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.nav-logo a {
    font-size: 1.5rem;
    font-weight: 700;
    color: #2563eb;
    text-decoration: none;
}

.nav-menu {
    display: flex;
    gap: 2rem;
}

.nav-link {
    color: #333;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.3s ease;
    position: relative;
}

.nav-link:hover {
    color: #2563eb;
}

.nav-link::after {
    content: '';
    position: absolute;
    width: 0;
    height: 2px;
    bottom: -5px;
    left: 0;
    background-color: #2563eb;
    transition: width 0.3s ease;
}

.nav-link:hover::after {
    width: 100%;
}

.hamburger {
    display: none;
    flex-direction: column;
    cursor: pointer;
}

.bar {
    width: 25px;
    height: 3px;
    background-color: #333;
    margin: 3px 0;
    transition: 0.3s;
}

/* Hero Section */
.hero {
    min-height: 100vh;
    display: flex;
    align-items: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><polygon fill="rgba(255,255,255,0.1)" points="0,1000 1000,0 1000,1000"/></svg>');
    background-size: cover;
}

.hero-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    position: relative;
    z-index: 2;
}

.hero-content {
    max-width: 600px;
}

.greeting {
    display: block;
    font-size: 1.2rem;
    margin-bottom: 0.5rem;
    opacity: 0.9;
}

.name {
    display: block;
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    background: linear-gradient(45deg, #fff, #e0e7ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-subtitle {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: #e0e7ff;
}

.hero-description {
    font-size: 1.1rem;
    margin-bottom: 2rem;
    opacity: 0.9;
    line-height: 1.7;
}

.hero-buttons {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
}

.btn {
    padding: 12px 30px;
    border-radius: 50px;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s ease;
    display: inline-block;
}

.btn-primary {
    background: #fff;
    color: #2563eb;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}

.btn-secondary {
    background: transparent;
    color: #fff;
    border: 2px solid #fff;
}

.btn-secondary:hover {
    background: #fff;
    color: #2563eb;
}

.social-links {
    display: flex;
    gap: 1rem;
}

.social-links a {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: rgba(255,255,255,0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-size: 1.2rem;
    transition: all 0.3s ease;
}

.social-links a:hover {
    background: #fff;
    color: #2563eb;
    transform: translateY(-3px);
}

.scroll-indicator {
    position: absolute;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
}

.scroll-arrow {
    width: 30px;
    height: 30px;
    border: 2px solid #fff;
    border-top: none;
    border-right: none;
    transform: rotate(-45deg);
    animation: bounce 2s infinite;
}

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% {
        transform: translateX(-50%) rotate(-45deg) translateY(0);
    }
    40% {
        transform: translateX(-50%) rotate(-45deg) translateY(-10px);
    }
    60% {
        transform: translateX(-50%) rotate(-45deg) translateY(-5px);
    }
}

/* Section Styles */
section {
    padding: 80px 0;
}

.section-title {
    font-size: 2.5rem;
    text-align: center;
    margin-bottom: 3rem;
    color: #1f2937;
    position: relative;
}

.section-title::after {
    content: '';
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    width: 60px;
    height: 4px;
    background: linear-gradient(45deg, #2563eb, #7c3aed);
    border-radius: 2px;
}

/* About Section */
.about {
    background: #f8fafc;
}

.about-content {
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
}

.about-text p {
    font-size: 1.1rem;
    margin-bottom: 2rem;
    color: #4b5563;
    line-height: 1.8;
}

.about-details {
    display: flex;
    justify-content: center;
    gap: 2rem;
    flex-wrap: wrap;
}

.detail-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #6b7280;
}

.detail-item i {
    color: #2563eb;
}

/* Experience Section */
.timeline {
    max-width: 800px;
    margin: 0 auto;
    position: relative;
}

.timeline::before {
    content: '';
    position: absolute;
    left: 50%;
    top: 0;
    bottom: 0;
    width: 2px;
    background: #e5e7eb;
    transform: translateX(-50%);
}

.timeline-item {
    position: relative;
    margin-bottom: 3rem;
    width: 50%;
}

.timeline-item:nth-child(odd) {
    left: 0;
    padding-right: 2rem;
}

.timeline-item:nth-child(even) {
    left: 50%;
    padding-left: 2rem;
}

.timeline-marker {
    position: absolute;
    width: 20px;
    height: 20px;
    background: #2563eb;
    border-radius: 50%;
    top: 0;
}

.timeline-item:nth-child(odd) .timeline-marker {
    right: -10px;
}

.timeline-item:nth-child(even) .timeline-marker {
    left: -10px;
}

.timeline-content {
    background: #fff;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
}

.timeline-content:hover {
    transform: translateY(-5px);
}

.timeline-content h3 {
    color: #1f2937;
    margin-bottom: 0.5rem;
    font-size: 1.3rem;
}

.timeline-content h4 {
    color: #2563eb;
    margin-bottom: 1rem;
    font-weight: 600;
}

.timeline-meta {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
    font-size: 0.9rem;
    color: #6b7280;
}

.timeline-description ul {
    list-style: none;
    padding-left: 0;
}

.timeline-description li {
    position: relative;
    padding-left: 1.5rem;
    margin-bottom: 0.5rem;
    color: #4b5563;
}

.timeline-description li::before {
    content: '▸';
    position: absolute;
    left: 0;
    color: #2563eb;
}

/* Projects Section */
.projects {
    background: #f8fafc;
}

.projects-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2rem;
    max-width: 1000px;
    margin: 0 auto;
}

.project-card {
    background: #fff;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}

.project-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.15);
}

.project-content {
    padding: 2rem;
}

.project-content h3 {
    color: #1f2937;
    margin-bottom: 1rem;
    font-size: 1.4rem;
}

.project-content p {
    color: #4b5563;
    margin-bottom: 1.5rem;
    line-height: 1.6;
}

.tech-stack {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
}

.tech-tag {
    background: #e0e7ff;
    color: #3730a3;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
}

.project-links {
    display: flex;
    gap: 1rem;
}

.project-btn {
    padding: 0.7rem 1.5rem;
    background: #2563eb;
    color: #fff;
    text-decoration: none;
    border-radius: 25px;
    font-weight: 500;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.project-btn:hover {
    background: #1d4ed8;
    transform: translateY(-2px);
}

/* Skills Section */
.skills-container {
    max-width: 1000px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}

.skill-category {
    background: #fff;
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    text-align: center;
}

.skill-category h3 {
    color: #1f2937;
    margin-bottom: 1.5rem;
    font-size: 1.3rem;
}

.skill-items {
    display: flex;
    flex-wrap: wrap;
    gap: 0.8rem;
    justify-content: center;
}

.skill-item {
    background: linear-gradient(45deg, #2563eb, #7c3aed);
    color: #fff;
    padding: 0.6rem 1.2rem;
    border-radius: 25px;
    font-weight: 500;
    transition: all 0.3s ease;
}

.skill-item:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 15px rgba(37, 99, 235, 0.4);
}

/* Education Section */
.education {
    background: #f8fafc;
}

.education-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    max-width: 800px;
    margin: 0 auto;
}

.education-card {
    background: #fff;
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    text-align: center;
    transition: transform 0.3s ease;
}

.education-card:hover {
    transform: translateY(-5px);
}

.education-card h3 {
    color: #1f2937;
    margin-bottom: 0.5rem;
    font-size: 1.3rem;
}

.education-card h4 {
    color: #2563eb;
    margin-bottom: 1rem;
    font-weight: 600;
}

.education-meta {
    display: flex;
    justify-content: center;
    gap: 1rem;
    color: #6b7280;
    font-size: 0.9rem;
}

/* Contact Section */
.contact {
    background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
    color: #fff;
}

.contact-content {
    max-width: 600px;
    margin: 0 auto;
    text-align: center;
}

.contact-content h3 {
    font-size: 2rem;
    margin-bottom: 1rem;
}

.contact-content p {
    font-size: 1.1rem;
    margin-bottom: 2rem;
    opacity: 0.9;
}

.contact-details {
    margin-bottom: 2rem;
}

.contact-item {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 1rem;
    font-size: 1.1rem;
}

.contact-item i {
    color: #60a5fa;
}

.contact-item a {
    color: #fff;
    text-decoration: none;
}

.contact-item a:hover {
    color: #60a5fa;
}

.social-links-contact {
    display: flex;
    justify-content: center;
    gap: 1rem;
    flex-wrap: wrap;
}

.social-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.8rem 1.5rem;
    background: rgba(255,255,255,0.1);
    color: #fff;
    text-decoration: none;
    border-radius: 25px;
    transition: all 0.3s ease;
    font-weight: 500;
}

.social-btn:hover {
    background: #60a5fa;
    transform: translateY(-3px);
}

/* Footer */
.footer {
    background: #111827;
    color: #9ca3af;
    text-align: center;
    padding: 2rem 0;
}

/* Responsive Design */
@media (max-width: 768px) {
    .hamburger {
        display: flex;
    }
    
    .nav-menu {
        position: fixed;
        left: -100%;
        top: 70px;
        flex-direction: column;
        background-color: #fff;
        width: 100%;
        text-align: center;
        transition: 0.3s;
        box-shadow: 0 10px 27px rgba(0,0,0,0.05);
        padding: 2rem 0;
    }
    
    .nav-menu.active {
        left: 0;
    }
    
    .name {
        font-size: 2.5rem !important;
    }
    
    .hero-buttons {
        flex-direction: column;
        align-items: center;
    }
    
    .timeline::before {
        left: 20px;
    }
    
    .timeline-item {
        width: 100%;
        left: 0 !important;
        padding-left: 3rem !important;
        padding-right: 0 !important;
    }
    
    .timeline-marker {
        left: 10px !important;
    }
    
    .about-details {
        flex-direction: column;
        align-items: center;
    }
    
    .projects-grid {
        grid-template-columns: 1fr;
    }
    
    .skills-container {
        grid-template-columns: 1fr;
    }
    
    .education-grid {
        grid-template-columns: 1fr;
    }
    
    .social-links-contact {
        flex-direction: column;
        align-items: center;
    }
}

@media (max-width: 480px) {
    .container {
        padding: 0 15px;
    }
    
    .name {
        font-size: 2rem !important;
    }
    
    .section-title {
        font-size: 2rem;
    }
    
    .timeline-content {
        padding: 1.5rem;
    }
    
    .project-content {
        padding: 1.5rem;
    }
    
    .skill-category {
        padding: 1.5rem;
    }
}'''
    
    def generate_js(self) -> str:
        """Generate the JavaScript file."""
        return '''// Mobile Navigation Toggle
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('nav-menu');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
});

// Close mobile menu when clicking on a link
document.querySelectorAll('.nav-link').forEach(n => n.addEventListener('click', () => {
    hamburger.classList.remove('active');
    navMenu.classList.remove('active');
}));

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Navbar background on scroll
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 100) {
        navbar.style.background = 'rgba(255, 255, 255, 0.98)';
        navbar.style.boxShadow = '0 2px 20px rgba(0,0,0,0.1)';
    } else {
        navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        navbar.style.boxShadow = 'none';
    }
});

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe elements for animation
document.addEventListener('DOMContentLoaded', () => {
    // Add animation classes to elements
    const animatedElements = document.querySelectorAll('.timeline-item, .project-card, .skill-category, .education-card');
    
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});

// Typing animation for hero title
document.addEventListener('DOMContentLoaded', () => {
    const nameElement = document.querySelector('.name');
    if (nameElement) {
        const text = nameElement.textContent;
        nameElement.textContent = '';
        nameElement.style.borderRight = '3px solid #fff';
        
        let i = 0;
        const typeWriter = () => {
            if (i < text.length) {
                nameElement.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            } else {
                setTimeout(() => {
                    nameElement.style.borderRight = 'none';
                }, 1000);
            }
        };
        
        setTimeout(typeWriter, 1000);
    }
});

// Skill items hover effect
document.querySelectorAll('.skill-item').forEach(skill => {
    skill.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-5px) scale(1.05)';
    });
    
    skill.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
    });
});

// Project cards tilt effect
document.querySelectorAll('.project-card').forEach(card => {
    card.addEventListener('mousemove', function(e) {
        const rect = this.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        const rotateX = (y - centerY) / 10;
        const rotateY = (centerX - x) / 10;
        
        this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px)`;
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
    });
});

// Add loading animation
window.addEventListener('load', () => {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});

// Scroll progress indicator
const createScrollProgress = () => {
    const progressBar = document.createElement('div');
    progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 0%;
        height: 3px;
        background: linear-gradient(45deg, #2563eb, #7c3aed);
        z-index: 9999;
        transition: width 0.1s ease;
    `;
    document.body.appendChild(progressBar);
    
    window.addEventListener('scroll', () => {
        const scrolled = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
        progressBar.style.width = scrolled + '%';
    });
};

createScrollProgress();'''
    
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
    generator = PortfolioGenerator()
    
    try:
        # Generate portfolio from parsed resume JSON
        generator.generate_portfolio("parsed_resume.json")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Make sure you have a 'parsed_resume.json' file from the resume parser.")


if __name__ == "__main__":
    main()
