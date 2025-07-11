"""
PDF Generator Module
Creates clean, structured PDF transcripts from educational scripts.
"""

import os
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime
import html
import re

# Try to import WeasyPrint, fall back to reportlab if not available
try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("WeasyPrint not available, falling back to reportlab")

# Fallback to reportlab
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFGenerator:
    """Generates structured PDF transcripts from educational scripts."""
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize the PDF generator.
        
        Args:
            output_dir: Directory to save PDF files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Check available PDF libraries
        self.use_weasyprint = WEASYPRINT_AVAILABLE
        self.use_reportlab = REPORTLAB_AVAILABLE
        
        if not (self.use_weasyprint or self.use_reportlab):
            raise ImportError("Neither WeasyPrint nor ReportLab is available. Please install one of them.")
        
        logger.info(f"PDF Generator initialized with {'WeasyPrint' if self.use_weasyprint else 'ReportLab'}")
    
    async def create_pdf(self, script_data: Dict[str, Any], output_path: Optional[str] = None) -> str:
        """
        Create a PDF transcript from script data.
        
        Args:
            script_data: Educational script data
            output_path: Custom output path (generates if None)
            
        Returns:
            Path to the generated PDF file
        """
        try:
            logger.info("Creating PDF transcript...")
            
            # Generate output path if not provided
            if not output_path:
                title = script_data.get('title', 'Educational_Transcript')
                safe_title = re.sub(r'[^\w\s-]', '', title).strip()
                safe_title = re.sub(r'[-\s]+', '_', safe_title)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = self.output_dir / f"{safe_title}_{timestamp}.pdf"
            
            # Create PDF using available library
            if self.use_weasyprint:
                pdf_path = await self._create_pdf_weasyprint(script_data, str(output_path))
            elif self.use_reportlab:
                pdf_path = await self._create_pdf_reportlab(script_data, str(output_path))
            else:
                raise RuntimeError("No PDF library available")
            
            logger.info(f"PDF created successfully: {pdf_path}")
            return pdf_path
            
        except Exception as e:
            logger.error(f"Error creating PDF: {e}")
            raise
    
    async def _create_pdf_weasyprint(self, script_data: Dict[str, Any], output_path: str) -> str:
        """Create PDF using WeasyPrint."""
        try:
            # Generate HTML content
            html_content = self._generate_html(script_data)
            
            # Generate CSS styles
            css_content = self._generate_css()
            
            # Create PDF
            html_doc = HTML(string=html_content)
            css_doc = CSS(string=css_content)
            
            html_doc.write_pdf(output_path, stylesheets=[css_doc])
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error with WeasyPrint: {e}")
            raise
    
    async def _create_pdf_reportlab(self, script_data: Dict[str, Any], output_path: str) -> str:
        """Create PDF using ReportLab."""
        try:
            # Create document
            doc = SimpleDocTemplate(output_path, pagesize=letter)
            story = []
            
            # Get styles
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                textColor=HexColor('#1f4e79'),
                alignment=1  # Center alignment
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=18,
                spaceAfter=12,
                spaceBefore=20,
                textColor=HexColor('#2e75b6')
            )
            
            body_style = ParagraphStyle(
                'CustomBody',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=12,
                leading=14
            )
            
            # Title
            title = script_data.get('title', 'Educational Transcript')
            story.append(Paragraph(title, title_style))
            story.append(Spacer(1, 20))
            
            # Metadata
            metadata = f"""
            <b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>
            <b>Subject:</b> {script_data.get('subject_area', 'General').title()}<br/>
            <b>Difficulty:</b> {script_data.get('difficulty_level', 'Intermediate').title()}<br/>
            <b>Duration:</b> {script_data.get('total_duration', 0):.1f} seconds
            """
            story.append(Paragraph(metadata, body_style))
            story.append(Spacer(1, 20))
            
            # Introduction
            if script_data.get('introduction'):
                story.append(Paragraph("Introduction", heading_style))
                story.append(Paragraph(script_data['introduction'], body_style))
                story.append(Spacer(1, 12))
            
            # Sections
            for i, section in enumerate(script_data.get('sections', [])):
                section_title = section.get('title', f'Section {i+1}')
                story.append(Paragraph(section_title, heading_style))
                
                if section.get('content'):
                    story.append(Paragraph(section['content'], body_style))
                
                # Add math expressions if present
                if section.get('math_expressions'):
                    story.append(Paragraph("<b>Mathematical Expressions:</b>", body_style))
                    for expr in section['math_expressions']:
                        story.append(Paragraph(f"• {expr}", body_style))
                
                story.append(Spacer(1, 12))
            
            # Summary
            if script_data.get('summary'):
                story.append(Paragraph("Summary", heading_style))
                story.append(Paragraph(script_data['summary'], body_style))
                story.append(Spacer(1, 12))
            
            # Keywords
            if script_data.get('keywords'):
                story.append(Paragraph("Keywords", heading_style))
                keywords_text = ", ".join(script_data['keywords'])
                story.append(Paragraph(keywords_text, body_style))
            
            # Build PDF
            doc.build(story)
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error with ReportLab: {e}")
            raise
    
    def _generate_html(self, script_data: Dict[str, Any]) -> str:
        """Generate HTML content for the PDF."""
        title = html.escape(script_data.get('title', 'Educational Transcript'))
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
        </head>
        <body>
            <div class="header">
                <h1>{title}</h1>
                <div class="metadata">
                    <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p><strong>Subject:</strong> {script_data.get('subject_area', 'General').title()}</p>
                    <p><strong>Difficulty:</strong> {script_data.get('difficulty_level', 'Intermediate').title()}</p>
                    <p><strong>Duration:</strong> {script_data.get('total_duration', 0):.1f} seconds</p>
                </div>
            </div>
            
            <div class="content">
        """
        
        # Introduction
        if script_data.get('introduction'):
            html_content += f"""
                <section class="introduction">
                    <h2>Introduction</h2>
                    <p>{html.escape(script_data['introduction'])}</p>
                </section>
            """
        
        # Sections
        for i, section in enumerate(script_data.get('sections', [])):
            section_title = html.escape(section.get('title', f'Section {i+1}'))
            section_content = html.escape(section.get('content', ''))
            
            html_content += f"""
                <section class="section">
                    <h2>{section_title}</h2>
                    <p>{section_content}</p>
            """
            
            # Add math expressions if present
            if section.get('math_expressions'):
                html_content += """
                    <div class="math-expressions">
                        <h3>Mathematical Expressions:</h3>
                        <ul>
                """
                for expr in section['math_expressions']:
                    clean_expr = html.escape(str(expr))  # Convert to string first
                    html_content += f"<li><code>{clean_expr}</code></li>"
                html_content += """
                        </ul>
                    </div>
                """
            
            # Add visual cues
            if section.get('visual_cues'):
                html_content += """
                    <div class="visual-cues">
                        <h3>Visual Elements:</h3>
                        <ul>
                """
                for cue in section['visual_cues']:
                    html_content += f"<li>{html.escape(cue)}</li>"
                html_content += """
                        </ul>
                    </div>
                """
            
            html_content += "</section>"
        
        # Summary
        if script_data.get('summary'):
            html_content += f"""
                <section class="summary">
                    <h2>Summary</h2>
                    <p>{html.escape(script_data['summary'])}</p>
                </section>
            """
        
        # Keywords
        if script_data.get('keywords'):
            keywords_text = ", ".join(script_data['keywords'])
            html_content += f"""
                <section class="keywords">
                    <h2>Keywords</h2>
                    <p>{html.escape(keywords_text)}</p>
                </section>
            """
        
        html_content += """
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def _generate_css(self) -> str:
        """Generate CSS styles for the PDF."""
        return """
        @page {
            size: A4;
            margin: 1in;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 100%;
        }
        
        .header {
            text-align: center;
            border-bottom: 2px solid #1f4e79;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        
        .header h1 {
            color: #1f4e79;
            font-size: 28px;
            margin: 0 0 20px 0;
        }
        
        .metadata {
            font-size: 12px;
            color: #666;
        }
        
        .metadata p {
            margin: 5px 0;
        }
        
        .content {
            max-width: 100%;
        }
        
        section {
            margin-bottom: 30px;
            page-break-inside: avoid;
        }
        
        h2 {
            color: #2e75b6;
            font-size: 20px;
            margin: 20px 0 10px 0;
            border-bottom: 1px solid #ccc;
            padding-bottom: 5px;
        }
        
        h3 {
            color: #4a90a4;
            font-size: 16px;
            margin: 15px 0 8px 0;
        }
        
        p {
            margin: 10px 0;
            text-align: justify;
        }
        
        .math-expressions {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
        }
        
        .visual-cues {
            background-color: #fff3cd;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
        }
        
        ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        
        li {
            margin: 5px 0;
        }
        
        code {
            background-color: #f1f1f1;
            padding: 2px 4px;
            font-family: 'Courier New', monospace;
            border-radius: 3px;
        }
        
        .introduction {
            background-color: #e8f4fd;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #1f4e79;
        }
        
        .summary {
            background-color: #f0f8ff;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #2e75b6;
        }
        
        .keywords {
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
        }
        """
    
    def create_simple_pdf(self, title: str, content: str, output_path: str) -> str:
        """
        Create a simple PDF from title and content.
        
        Args:
            title: Document title
            content: Document content
            output_path: Output file path
            
        Returns:
            Path to the generated PDF
        """
        try:
            if self.use_reportlab:
                doc = SimpleDocTemplate(output_path, pagesize=letter)
                story = []
                styles = getSampleStyleSheet()
                
                # Title
                title_style = ParagraphStyle(
                    'Title',
                    parent=styles['Heading1'],
                    fontSize=24,
                    spaceAfter=30,
                    alignment=1
                )
                story.append(Paragraph(title, title_style))
                
                # Content
                content_style = ParagraphStyle(
                    'Content',
                    parent=styles['Normal'],
                    fontSize=12,
                    spaceAfter=12
                )
                
                # Split content into paragraphs
                paragraphs = content.split('\n\n')
                for para in paragraphs:
                    if para.strip():
                        story.append(Paragraph(para.strip(), content_style))
                        story.append(Spacer(1, 12))
                
                doc.build(story)
                
            elif self.use_weasyprint:
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>{html.escape(title)}</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 1in; }}
                        h1 {{ text-align: center; color: #333; }}
                        p {{ margin: 10px 0; text-align: justify; }}
                    </style>
                </head>
                <body>
                    <h1>{html.escape(title)}</h1>
                    <div>
                """
                
                # Process content with proper escaping (avoiding backslashes in f-string)
                escaped_content = html.escape(content)
                formatted_content = escaped_content.replace('\n\n', '</p><p>').replace('\n', '<br>')
                html_content += formatted_content
                
                html_content += """
                    </div>
                </body>
                </html>
                """
                
                HTML(string=html_content).write_pdf(output_path)
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating simple PDF: {e}")
            raise

# Example usage
if __name__ == "__main__":
    async def test_pdf_generator():
        """Test the PDF generator."""
        try:
            generator = PDFGenerator()
            
            # Sample script data
            sample_script = {
                "title": "Linear Regression Explained",
                "introduction": "This document explains the concept of linear regression in machine learning.",
                "sections": [
                    {
                        "title": "What is Linear Regression?",
                        "content": "Linear regression is a statistical method used to model the relationship between a dependent variable and one or more independent variables.",
                        "math_expressions": ["y = mx + b", "R² = 1 - (SS_res / SS_tot)"],
                        "visual_cues": ["Show scatter plot", "Display regression line"]
                    },
                    {
                        "title": "Mathematical Foundation",
                        "content": "The goal is to find the line that minimizes the sum of squared residuals.",
                        "math_expressions": ["min Σ(yi - ŷi)²"],
                        "visual_cues": ["Animate residuals", "Show cost function"]
                    }
                ],
                "summary": "Linear regression is a powerful tool for prediction and understanding relationships between variables.",
                "keywords": ["regression", "machine learning", "statistics", "prediction"],
                "subject_area": "machine learning",
                "difficulty_level": "intermediate",
                "total_duration": 180.0
            }
            
            print("Testing PDF generation...")
            pdf_path = await generator.create_pdf(sample_script)
            print(f"PDF generated: {pdf_path}")
            
            # Test simple PDF
            simple_pdf_path = "test_simple.pdf"
            generator.create_simple_pdf(
                "Test Document",
                "This is a test document with some content.\n\nThis is another paragraph.",
                simple_pdf_path
            )
            print(f"Simple PDF generated: {simple_pdf_path}")
            
        except Exception as e:
            print(f"Test failed: {e}")
    
    # Run test
    asyncio.run(test_pdf_generator())
