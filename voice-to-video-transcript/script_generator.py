"""
Educational Script Generator using LLM
Converts raw transcripts into structured educational content.
"""

import os
import asyncio
import json
import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import openai
from openai import OpenAI
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ScriptSection:
    """Represents a section of the educational script."""
    title: str
    content: str
    section_type: str  # 'introduction', 'concept', 'example', 'summary'
    duration_estimate: float  # in seconds
    visual_cues: List[str]  # Instructions for animation
    math_expressions: List[str]  # LaTeX expressions if any

@dataclass
class EducationalScript:
    """Complete educational script structure."""
    title: str
    introduction: str
    sections: List[ScriptSection]
    summary: str
    full_text: str
    total_duration: float
    keywords: List[str]
    difficulty_level: str
    subject_area: str

class ScriptGenerator:
    """Generates structured educational scripts from raw transcripts."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize the script generator.
        
        Args:
            api_key: OpenAI API key
            model: Model to use (gpt-4, gpt-3.5-turbo, etc.)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        
        # Check if model supports json_object response format
        self.supports_json_format = model in ["gpt-4", "gpt-4-turbo", "gpt-4-1106-preview", "gpt-3.5-turbo-1106"]
        
        # System prompt for educational script generation
        self.system_prompt = """You are an expert educational content creator specializing in creating clear, engaging educational scripts in the style of 3Blue1Brown. Your job is to transform raw transcripts into well-structured educational content.

Key requirements:
1. Create a clear, logical flow of concepts
2. Include visual cues for animations (graphs, equations, diagrams)
3. Break down complex topics into digestible sections
4. Add mathematical expressions in LaTeX format when relevant
5. Estimate timing for each section
6. Include engaging introductions and clear summaries
7. Maintain the educational tone throughout

Output format should be valid JSON with the specified structure."""
    
    async def generate_script(self, transcript: str, topic_hint: str = "", 
                            target_duration: Optional[float] = None) -> Dict[str, Any]:
        """
        Generate a structured educational script from a transcript.
        
        Args:
            transcript: Raw transcript text
            topic_hint: Optional hint about the topic
            target_duration: Target duration in seconds
            
        Returns:
            Dictionary containing the structured script
        """
        try:
            logger.info(f"Generating educational script for transcript of length {len(transcript)}")
            
            # Prepare the prompt
            user_prompt = self._create_user_prompt(transcript, topic_hint, target_duration)
            
            # Make API call
            response = await self._call_openai(user_prompt)
            
            # Parse response
            script_data = self._parse_response(response)
            
            # Validate and enhance the script
            enhanced_script = self._enhance_script(script_data)
            
            logger.info("Educational script generated successfully")
            return enhanced_script
            
        except Exception as e:
            logger.error(f"Error generating script: {e}")
            raise
    
    def _create_user_prompt(self, transcript: str, topic_hint: str, 
                           target_duration: Optional[float]) -> str:
        """Create the user prompt for script generation."""
        
        duration_info = f"Target duration: {target_duration} seconds" if target_duration else "No specific duration target"
        topic_info = f"Topic hint: {topic_hint}" if topic_hint else "No specific topic hint"
        
        prompt = f"""Please convert this transcript into a well-structured educational script:

TRANSCRIPT:
{transcript}

CONTEXT:
{topic_info}
{duration_info}

REQUIREMENTS:
1. Analyze the transcript and identify the main educational concepts
2. Create a clear title that captures the essence of the content
3. Structure the content into logical sections (introduction, main concepts, examples, summary)
4. Add visual cues for animations (e.g., "Show graph of sine wave", "Animate matrix multiplication")
5. Include LaTeX expressions for mathematical content
6. Estimate timing for each section
7. Classify the difficulty level and subject area
8. Extract key keywords

OUTPUT FORMAT (JSON):
{{
    "title": "Clear, engaging title",
    "introduction": "Hook and overview of what will be covered",
    "sections": [
        {{
            "title": "Section title",
            "content": "Detailed explanation",
            "section_type": "introduction|concept|example|summary",
            "duration_estimate": 30.0,
            "visual_cues": ["Animation instruction 1", "Animation instruction 2"],
            "math_expressions": ["LaTeX expression 1", "LaTeX expression 2"]
        }}
    ],
    "summary": "Key takeaways and conclusion",
    "full_text": "Complete narration text",
    "total_duration": 300.0,
    "keywords": ["keyword1", "keyword2"],
    "difficulty_level": "beginner|intermediate|advanced",
    "subject_area": "mathematics|physics|computer_science|etc"
}}

Make sure the script is engaging, educational, and well-structured for video production."""
        
        return prompt
    
    async def _call_openai(self, prompt: str) -> str:
        """Make API call to OpenAI."""
        try:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            # Prepare parameters
            params = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 4000
            }
            
            # Only add response_format if supported
            if self.supports_json_format:
                params["response_format"] = {"type": "json_object"}
            
            response = self.client.chat.completions.create(**params)
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            raise
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse the JSON response from OpenAI."""
        try:
            # Try to parse as JSON first
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON response, attempting to extract JSON: {e}")
            
            # Try to extract JSON from the response if it's wrapped in other text
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    pass
            
            # If JSON parsing fails, create a basic structure
            logger.warning("Creating fallback script structure")
            return {
                "title": "Educational Content",
                "introduction": "This is educational content based on the provided transcript.",
                "sections": [
                    {
                        "title": "Main Content",
                        "content": response[:500] + "..." if len(response) > 500 else response,
                        "section_type": "concept",
                        "duration_estimate": 60.0,
                        "visual_cues": ["Display content"],
                        "math_expressions": []
                    }
                ],
                "summary": "This concludes the educational content.",
                "full_text": response,
                "total_duration": 120.0,
                "keywords": ["education", "learning"],
                "difficulty_level": "intermediate",
                "subject_area": "general"
            }
    
    def _enhance_script(self, script_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance and validate the script data."""
        try:
            # Ensure all required fields are present
            required_fields = ['title', 'introduction', 'sections', 'summary', 'full_text']
            for field in required_fields:
                if field not in script_data:
                    logger.warning(f"Missing required field: {field}")
                    script_data[field] = ""
            
            # Validate sections
            if 'sections' not in script_data or not script_data['sections']:
                script_data['sections'] = []
            
            # Ensure each section has required fields
            for i, section in enumerate(script_data['sections']):
                if 'visual_cues' not in section:
                    section['visual_cues'] = []
                if 'math_expressions' not in section:
                    section['math_expressions'] = []
                if 'duration_estimate' not in section:
                    section['duration_estimate'] = 30.0
                if 'section_type' not in section:
                    section['section_type'] = 'concept'
            
            # Calculate total duration if not provided
            if 'total_duration' not in script_data:
                script_data['total_duration'] = sum(
                    section.get('duration_estimate', 30.0) 
                    for section in script_data['sections']
                )
            
            # Set defaults for other fields
            script_data.setdefault('keywords', [])
            script_data.setdefault('difficulty_level', 'intermediate')
            script_data.setdefault('subject_area', 'general')
            
            # Generate full text if not provided
            if not script_data['full_text']:
                script_data['full_text'] = self._generate_full_text(script_data)
            
            return script_data
            
        except Exception as e:
            logger.error(f"Error enhancing script: {e}")
            raise
    
    def _generate_full_text(self, script_data: Dict[str, Any]) -> str:
        """Generate full narration text from script sections."""
        full_text = []
        
        # Add introduction
        if script_data.get('introduction'):
            full_text.append(script_data['introduction'])
        
        # Add section content
        for section in script_data.get('sections', []):
            if section.get('content'):
                full_text.append(section['content'])
        
        # Add summary
        if script_data.get('summary'):
            full_text.append(script_data['summary'])
        
        return ' '.join(full_text)
    
    def improve_script(self, script_data: Dict[str, Any], feedback: str) -> Dict[str, Any]:
        """
        Improve an existing script based on feedback.
        
        Args:
            script_data: Current script data
            feedback: Feedback for improvement
            
        Returns:
            Improved script data
        """
        try:
            improvement_prompt = f"""Please improve this educational script based on the feedback:

CURRENT SCRIPT:
{json.dumps(script_data, indent=2)}

FEEDBACK:
{feedback}

Please provide the improved version in the same JSON format, addressing the feedback while maintaining the educational quality and structure."""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": improvement_prompt}
                ],
                temperature=0.7,
                max_tokens=4000,
                response_format={"type": "json_object"}
            )
            
            improved_script = json.loads(response.choices[0].message.content)
            return self._enhance_script(improved_script)
            
        except Exception as e:
            logger.error(f"Error improving script: {e}")
            raise
    
    def extract_math_expressions(self, text: str) -> List[str]:
        """Extract LaTeX math expressions from text."""
        # Pattern to match LaTeX expressions
        latex_patterns = [
            r'\$\$([^$]+)\$\$',  # Display math
            r'\$([^$]+)\$',      # Inline math
            r'\\begin\{([^}]+)\}.*?\\end\{\1\}',  # Environment blocks
            r'\\[a-zA-Z]+\{[^}]*\}',  # LaTeX commands
        ]
        
        expressions = []
        for pattern in latex_patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            expressions.extend(matches)
        
        return list(set(expressions))  # Remove duplicates
    
    def generate_visual_cues(self, content: str, section_type: str) -> List[str]:
        """Generate visual cues based on content and section type."""
        cues = []
        
        # Keywords that suggest specific visual elements
        visual_keywords = {
            'graph': ['Show coordinate system', 'Plot function', 'Animate curve'],
            'equation': ['Display equation', 'Highlight terms', 'Show step-by-step solution'],
            'matrix': ['Show matrix', 'Animate matrix operations', 'Highlight elements'],
            'vector': ['Display vector', 'Show vector addition', 'Animate transformation'],
            'derivative': ['Show tangent line', 'Animate slope changes', 'Plot derivative'],
            'integral': ['Show area under curve', 'Animate Riemann sum', 'Display antiderivative'],
            'limit': ['Show approaching values', 'Animate limit process', 'Display epsilon-delta'],
            'theorem': ['Highlight theorem statement', 'Show proof steps', 'Display QED'],
            'example': ['Show worked example', 'Step-by-step solution', 'Highlight key steps'],
        }
        
        content_lower = content.lower()
        for keyword, suggestions in visual_keywords.items():
            if keyword in content_lower:
                cues.extend(suggestions[:2])  # Add max 2 suggestions per keyword
        
        # Default cues based on section type
        if section_type == 'introduction':
            cues.append('Show title and overview')
        elif section_type == 'summary':
            cues.append('Display key points')
        
        return cues[:5]  # Limit to 5 visual cues per section

# Example usage
if __name__ == "__main__":
    async def test_script_generator():
        """Test the script generator."""
        try:
            generator = ScriptGenerator()
            
            # Sample transcript
            sample_transcript = """
            Today I want to explain linear regression. Linear regression is a fundamental concept in machine learning and statistics. It's used to model the relationship between a dependent variable and one or more independent variables. The basic idea is to find a line that best fits through a set of data points. The equation of this line is y equals mx plus b, where m is the slope and b is the y-intercept. We can use this line to make predictions about new data points. The method to find the best fitting line is called the method of least squares, which minimizes the sum of squared residuals.
            """
            
            print("Testing script generation...")
            script = await generator.generate_script(
                sample_transcript, 
                topic_hint="Linear Regression Machine Learning"
            )
            
            print(f"Generated script title: {script['title']}")
            print(f"Number of sections: {len(script['sections'])}")
            print(f"Total duration: {script['total_duration']} seconds")
            print(f"Keywords: {script['keywords']}")
            
        except Exception as e:
            print(f"Test failed: {e}")
    
    # Run test
    asyncio.run(test_script_generator())
