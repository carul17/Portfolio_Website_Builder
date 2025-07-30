# AI-Powered Resume Parser & Portfolio Generator

A comprehensive Python toolkit that extracts structured information from PDF resumes using AI and generates beautiful, professional portfolio websites automatically.

## 🚀 Features

### Resume Parser (`dynamic_resume_parser.py`)
- **AI-Powered Extraction**: Uses OpenAI GPT-4o-mini to intelligently parse resume content
- **Bold Text Preservation**: Maintains formatting from PDFs (bold text becomes `**text**`)
- **Flexible Structure**: Dynamically adapts to different resume formats and sections
- **Hyperlink Detection**: Preserves URLs and contact links from PDFs
- **Multiple Detection Methods**: Uses font flags, font names, and weights to detect formatting
- **Custom Sections**: Automatically includes empty hero and about sections for customization

### Portfolio Generator (`portfolio_generator.py`)
- **Professional Design**: Modern, responsive dark theme with blue accent colors
- **AI-Generated Content**: Creates personalized hero and about descriptions
- **Profile Picture Support**: Adds LinkedIn-style circular profile pictures
- **Resume Integration**: Automatically includes downloadable resume PDF
- **Smooth Animations**: Professional hover effects and transitions
- **Mobile Responsive**: Optimized for all device sizes
- **SEO Friendly**: Clean HTML structure with proper meta tags

## 📋 Requirements

- Python 3.8+
- OpenAI API key
- Required packages: `openai`, `PyMuPDF` (fitz), `pathlib`

## 🛠️ Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## 📖 Usage

### Step 1: Parse Resume
```bash
uv run dynamic_resume_parser.py resume.pdf [output.json]
```

### Step 2: Generate Portfolio
```bash
uv run portfolio_generator.py [parsed_resume.json] [resume.pdf] [profile_picture.jpg]
```

### Complete Example
```bash
# Parse the resume
uv run dynamic_resume_parser.py Callum_Arul_Resume_August.pdf parsed_resume.json

# Generate portfolio with profile picture
uv run portfolio_generator.py parsed_resume.json Callum_Arul_Resume_August.pdf profile.jpg
```

## 📁 Project Structure

```
├── dynamic_resume_parser.py    # AI-powered PDF parser
├── portfolio_generator.py      # Portfolio website generator
├── templates/
│   ├── index.html              # HTML template
│   ├── style.css               # Professional dark theme CSS
│   └── script.js               # Interactive JavaScript
├── portfolio_website/          # Generated website output
│   ├── index.html
│   ├── css/style.css
│   ├── js/script.js
│   └── assets/
│       ├── resume.pdf
│       └── profile.jpg
└── requirements.txt
```

## 🎨 Portfolio Features

- **Hero Section**: Name, title, personalized description, profile picture
- **About Section**: AI-generated personal introduction
- **Experience Timeline**: Interactive work history with hover effects
- **Projects Showcase**: Featured projects with technology tags
- **Skills Grid**: Organized technical skills by category
- **Education**: Academic background and achievements
- **Contact**: Multiple contact methods and social links
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile

## 🔧 Customization

### Custom Descriptions
Edit the generated `parsed_resume.json` file to add custom hero and about descriptions:
```json
{
  "hero_description": "Your custom hero description here",
  "about_me": "Your custom about section here",
  ...
}
```

### Theme Colors
The portfolio uses a professional blue theme. Colors can be customized in `templates/style.css`:
- Primary: `#3b82f6`
- Secondary: `#2563eb`
- Dark: `#1d4ed8`

## 📊 Output Format

The parser generates structured JSON with sections like:
- `personal_info`: Contact details and basic information
- `work_experience`: Job history with descriptions
- `projects`: Portfolio projects with links and technologies
- `skills`: Technical skills organized by category
- `education`: Academic background
- `hero_description`: Custom hero section text
- `about_me`: Custom about section text

## 🤖 AI Integration

- **Smart Parsing**: Adapts to different resume formats automatically
- **Content Generation**: Creates engaging, personalized descriptions
- **Format Preservation**: Maintains important formatting like bold text
- **Context Awareness**: Generates content based on actual resume content

## 🌐 Live Demo

The generated portfolio includes:
- Smooth scrolling navigation
- Interactive animations
- Professional typography
- Optimized performance
- Cross-browser compatibility

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
