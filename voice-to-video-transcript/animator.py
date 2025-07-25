"""
3Blue1Brown-style Video Animation Module using Manim
Creates beautiful mathematical and educational animations.
"""

import os
import asyncio
import tempfile
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import logging
import json
import re
from manim import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoAnimator:
    """Creates educational animations using Manim in 3Blue1Brown style."""
    
    def __init__(self, quality: str = "medium_quality", fps: int = 30):
        """
        Initialize the animator.
        
        Args:
            quality: Video quality (low_quality, medium_quality, high_quality, production_quality)
            fps: Frames per second
        """
        self.quality = quality
        self.fps = fps
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
        # Test Manim installation
        manim_test = self.test_manim_installation()
        if not manim_test['manim_available']:
            logger.error(f"Manim not properly installed: {manim_test['error']}")
            raise RuntimeError(f"Manim not available: {manim_test['error']}")
        else:
            logger.info(f"Manim available: {manim_test['version']}")
        
        # Animation scene templates
        self.scene_templates = {
            'introduction': self._generate_intro_content,
            'concept': self._generate_concept_content,
            'example': self._generate_example_content,
            'summary': self._generate_summary_content,
            'math': self._generate_concept_content,
            'graph': self._generate_concept_content,
            'theorem': self._generate_concept_content
        }
        
        # Color scheme (3Blue1Brown style)
        self.colors = {
            'blue': BLUE,
            'light_blue': BLUE_A,
            'dark_blue': BLUE_E,
            'yellow': YELLOW,
            'green': GREEN,
            'red': RED,
            'purple': PURPLE,
            'orange': ORANGE,
            'text': WHITE,
            'background': "#0e1116"
        }
    
    async def create_animation(self, script_data: Dict[str, Any]) -> str:
        """
        Create complete animation from script data.
        
        Args:
            script_data: Educational script data
            
        Returns:
            Path to the generated animation video
        """
        try:
            logger.info("Starting animation creation...")
            
            # Generate Manim scene file
            scene_file_path = self._generate_scene_file(script_data)
            
            # Render the animation
            video_path = await self._render_animation(scene_file_path)
            
            logger.info(f"Animation created successfully: {video_path}")
            return video_path
            
        except Exception as e:
            logger.error(f"Error creating animation: {e}")
            raise
    
    def _generate_scene_file(self, script_data: Dict[str, Any]) -> str:
        """
        Generate a Manim scene file from script data.
        
        Args:
            script_data: Educational script data
            
        Returns:
            Path to the generated scene file
        """
        try:
            # Create scene class code
            scene_code = self._create_scene_code(script_data)
            
            # Write to file
            scene_file_path = self.output_dir / "educational_scene.py"
            with open(scene_file_path, 'w', encoding='utf-8') as f:
                f.write(scene_code)
            
            logger.info(f"Scene file generated: {scene_file_path}")
            return str(scene_file_path)
            
        except Exception as e:
            logger.error(f"Error generating scene file: {e}")
            raise
    
    def _create_scene_code(self, script_data: Dict[str, Any]) -> str:
        """
        Create the complete Manim scene code.
        
        Args:
            script_data: Educational script data
            
        Returns:
            Complete Python code for Manim scene
        """
        title = script_data.get('title', 'Educational Video')
        
        # Shorten title if too long
        if len(title) > 50:
            title = title[:47] + "..."
        
        # Clean title for safety
        title = title.replace('"', "'").replace('\\', '').replace('\n', ' ')
        
        # Start with imports and class definition
        scene_code = f'''"""
Generated Manim scene for educational content
"""

from manim import *
import numpy as np

class EducationalScene(Scene):
    """Main educational scene with 3Blue1Brown styling."""
    
    def construct(self):
        """Construct the complete educational scene."""
        # Set background color
        self.camera.background_color = "#0e1116"
        
        # Title sequence
        self.create_title_sequence()
        
        # Simple content
        self.create_main_content()
        
        # Final summary
        self.create_summary()
    
    def create_title_sequence(self):
        """Create animated title sequence."""
        # Split title into lines if too long
        title_text = "{title}"
        
        if len(title_text) > 35:
            # Split at reasonable points
            words = title_text.split()
            line1 = " ".join(words[:len(words)//2])
            line2 = " ".join(words[len(words)//2:])
            
            title_line1 = Text(line1, font_size=36, color=BLUE)
            title_line1.to_edge(UP).shift(DOWN * 0.8)
            
            title_line2 = Text(line2, font_size=36, color=BLUE)
            title_line2.next_to(title_line1, DOWN, buff=0.2)
            
            title = VGroup(title_line1, title_line2)
        else:
            title = Text(title_text, font_size=42, color=BLUE)
        
        subtitle = Text("Educational Content", font_size=24, color=YELLOW)
        subtitle.next_to(title, DOWN, buff=0.8)
        
        # Animate title
        self.play(Write(title), run_time=2)
        self.play(FadeIn(subtitle), run_time=1)
        self.wait(2)
        
        # Clear title
        self.play(FadeOut(title), FadeOut(subtitle))
        self.wait(0.5)
    
    def create_main_content(self):
        """Create main educational content."""
        # Main concept
        concept_title = Text("Key Concepts", font_size=32, color=BLUE)
        concept_title.to_edge(UP)
        
        self.play(Write(concept_title))
        self.wait(1)
        
        # Add some visual elements
        point1 = Text("• Understanding the topic", font_size=24, color=WHITE)
        point1.to_edge(LEFT).shift(UP * 1)
        
        point2 = Text("• Applying the knowledge", font_size=24, color=WHITE)
        point2.next_to(point1, DOWN, buff=0.5)
        
        point3 = Text("• Real-world applications", font_size=24, color=WHITE)
        point3.next_to(point2, DOWN, buff=0.5)
        
        # Animate points
        self.play(FadeIn(point1), run_time=1)
        self.wait(1)
        self.play(FadeIn(point2), run_time=1)
        self.wait(1)
        self.play(FadeIn(point3), run_time=1)
        self.wait(2)
        
        # Add a simple visual
        circle = Circle(radius=1.5, color=BLUE)
        circle.shift(RIGHT * 3)
        
        self.play(Create(circle))
        self.wait(1)
        
        # Clear section
        self.play(FadeOut(point1), FadeOut(point2), FadeOut(point3))
        self.play(FadeOut(circle))
        self.play(FadeOut(concept_title))
        self.wait(0.5)
    
    def create_summary(self):
        """Create summary section."""
        summary_title = Text("Summary", font_size=36, color=YELLOW)
        summary_title.to_edge(UP)
        
        self.play(Write(summary_title))
        self.wait(1)
        
        # Summary content
        summary_text = Text("Thank you for watching!", font_size=28, color=WHITE)
        summary_text.move_to(ORIGIN)
        
        self.play(FadeIn(summary_text))
        self.wait(3)
        
        # Final fade
        self.play(FadeOut(summary_title), FadeOut(summary_text))
        self.wait(1)
'''
        return scene_code
    
    def _generate_section_calls(self, sections: List[Dict]) -> str:
        """Generate method calls for each section."""
        calls = []
        for i, section in enumerate(sections):
            calls.append(f"        self.section_{i}()  # {section.get('title', f'Section {i}')}")
        return '\n'.join(calls)
    
    def _generate_section_methods(self, sections: List[Dict]) -> str:
        """Generate methods for each section."""
        methods = []
        
        for i, section in enumerate(sections):
            section_type = section.get('section_type', 'concept')
            title = section.get('title', f'Section {i}')
            content = section.get('content', '')
            visual_cues = section.get('visual_cues', [])
            math_expressions = section.get('math_expressions', [])
            
            method_code = f'''
    def section_{i}(self):
        """Section: {title}"""
        # Section title
        section_title = Text("{title}", font_size=32, color=BLUE)
        section_title.to_edge(UP)
        
        self.play(Write(section_title))
        self.wait(1)
        
        {self._generate_section_content(section_type, content, visual_cues, math_expressions)}
        
        # Clear section
        self.clear()
        self.wait(0.5)
'''
            methods.append(method_code)
        
        return '\n'.join(methods)
    
    def _generate_section_content(self, section_type: str, content: str, 
                                 visual_cues: List[str], math_expressions: List[str]) -> str:
        """Generate content for a specific section."""
        
        if section_type == 'introduction':
            return self._generate_intro_content(content, visual_cues)
        elif section_type == 'concept':
            return self._generate_concept_content(content, visual_cues, math_expressions)
        elif section_type == 'example':
            return self._generate_example_content(content, visual_cues, math_expressions)
        elif section_type == 'summary':
            return self._generate_summary_content(content, visual_cues)
        else:
            return self._generate_default_content(content, visual_cues, math_expressions)
    
    def _generate_intro_content(self, content: str, visual_cues: List[str]) -> str:
        """Generate introduction section content."""
        return '''
        # Introduction content
        intro_text = Text("Introduction", font_size=28, color=YELLOW)
        intro_text.move_to(ORIGIN)
        
        self.play(FadeIn(intro_text))
        self.wait(2)
        
        # Add visual elements based on cues
        self.play(FadeOut(intro_text))
        '''
    
    def _generate_concept_content(self, content: str, visual_cues: List[str], 
                                 math_expressions: List[str]) -> str:
        """Generate concept section content."""
        content_code = '''
        # Concept explanation
        concept_text = Text("Key Concept", font_size=24, color=WHITE)
        concept_text.to_edge(LEFT).shift(UP * 2)
        
        self.play(Write(concept_text))
        self.wait(1)
        '''
        
        # Add mathematical expressions if present (limit and clean them)
        if math_expressions:
            content_code += '''
        
        # Mathematical expressions
        '''
            for i, expr in enumerate(math_expressions[:2]):  # Limit to 2 expressions
                # Clean the expression - remove problematic characters
                clean_expr = str(expr).replace('\\', '').replace('"', '').replace("'", "")
                # Keep it simple - just basic text
                if len(clean_expr) > 50:
                    clean_expr = clean_expr[:47] + "..."
                    
                content_code += f'''
        math_text_{i} = Text("{clean_expr}", font_size=24, color=BLUE)
        math_text_{i}.next_to(concept_text, DOWN, buff=1)
        self.play(Write(math_text_{i}))
        self.wait(2)
        '''
        
        # Add simple visual elements
        if any(word in str(visual_cues).lower() for word in ['graph', 'plot', 'chart']):
            content_code += '''
        
        # Simple visual representation
        circle = Circle(radius=1, color=BLUE)
        circle.shift(RIGHT * 3)
        
        self.play(Create(circle))
        self.wait(1)
        self.play(FadeOut(circle))
        '''
        
        content_code += '''
        self.wait(1)
        '''
        
        return content_code
    
    def _generate_example_content(self, content: str, visual_cues: List[str], 
                                 math_expressions: List[str]) -> str:
        """Generate example section content."""
        return '''
        # Example demonstration
        example_title = Text("Example", font_size=28, color=GREEN)
        example_title.to_edge(UP).shift(DOWN * 0.5)
        
        self.play(Write(example_title))
        self.wait(1)
        
        # Step-by-step example
        step1 = Text("Step 1: Setup", font_size=20, color=WHITE)
        step1.to_edge(LEFT).shift(UP * 1)
        
        self.play(FadeIn(step1))
        self.wait(2)
        
        step2 = Text("Step 2: Calculate", font_size=20, color=WHITE)
        step2.next_to(step1, DOWN, buff=0.5)
        
        self.play(FadeIn(step2))
        self.wait(2)
        
        step3 = Text("Step 3: Result", font_size=20, color=YELLOW)
        step3.next_to(step2, DOWN, buff=0.5)
        
        self.play(FadeIn(step3))
        self.wait(2)
        '''
    
    def _generate_summary_content(self, content: str, visual_cues: List[str]) -> str:
        """Generate summary section content."""
        return '''
        # Summary points
        summary_points = VGroup()
        
        point1 = Text("• Key Point 1", font_size=20, color=WHITE)
        point2 = Text("• Key Point 2", font_size=20, color=WHITE)
        point3 = Text("• Key Point 3", font_size=20, color=WHITE)
        
        point1.to_edge(LEFT)
        point2.next_to(point1, DOWN, buff=0.3)
        point3.next_to(point2, DOWN, buff=0.3)
        
        summary_points.add(point1, point2, point3)
        
        self.play(FadeIn(summary_points, lag_ratio=0.5))
        self.wait(3)
        '''
    
    def _generate_default_content(self, content: str, visual_cues: List[str], 
                                 math_expressions: List[str]) -> str:
        """Generate default content for sections."""
        return '''
        # Default content
        content_text = Text("Content", font_size=24, color=WHITE)
        content_text.move_to(ORIGIN)
        
        self.play(FadeIn(content_text))
        self.wait(2)
        
        self.play(FadeOut(content_text))
        '''
    
    def _generate_utility_methods(self) -> str:
        """Generate utility methods for the scene."""
        return '''
    def create_coordinate_system(self, x_range=(-3, 3), y_range=(-2, 2)):
        """Create a coordinate system."""
        axes = Axes(
            x_range=[*x_range, 1],
            y_range=[*y_range, 1],
            x_length=6,
            y_length=4,
            axis_config={"color": WHITE}
        )
        return axes
    
    def highlight_text(self, text_obj, color=YELLOW):
        """Highlight text with a colored background."""
        return SurroundingRectangle(text_obj, color=color, buff=0.1)
    
    def create_bullet_points(self, points, start_pos=UP*2+LEFT*3):
        """Create animated bullet points."""
        bullet_group = VGroup()
        current_pos = start_pos
        
        for point in points:
            bullet = Text(f"• {point}", font_size=18, color=WHITE)
            bullet.move_to(current_pos)
            bullet_group.add(bullet)
            current_pos += DOWN * 0.5
        
        return bullet_group
'''
    
    async def _render_animation(self, scene_file_path: str) -> str:
        """
        Render the Manim animation using isolated subprocess.
        
        Args:
            scene_file_path: Path to the scene file
            
        Returns:
            Path to the rendered video
        """
        try:
            # Determine quality flag
            quality_flags = {
                'low_quality': '-ql',
                'medium_quality': '-qm', 
                'high_quality': '-qh',
                'production_quality': '-qk'
            }
            
            quality_flag = quality_flags.get(self.quality, '-qm')
            
            # Prepare command with proper isolation
            cmd = [
                'manim',
                quality_flag,
                '--fps', str(self.fps),
                '--media_dir', str(self.output_dir),
                '--disable_caching',  # Disable caching to avoid conflicts
                '--verbosity', 'WARNING',  # Reduce verbose output
                scene_file_path,
                'EducationalScene'
            ]
            
            logger.info(f"Running Manim command: {' '.join(cmd)}")
            
            # Run in a completely isolated subprocess
            import subprocess
            import asyncio
            
            # Create a new process group to isolate from server reloads
            process = None
            try:
                # Use asyncio subprocess for better isolation
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=str(self.output_dir.parent),
                    # Create new process group on Windows
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
                )
                
                # Wait for completion with timeout
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), 
                    timeout=180  # 3 minute timeout
                )
                
                # Decode output
                stdout_text = stdout.decode('utf-8', errors='replace') if stdout else ''
                stderr_text = stderr.decode('utf-8', errors='replace') if stderr else ''
                
                # Log output for debugging
                if stdout_text:
                    logger.info(f"Manim stdout: {stdout_text[:500]}...")  # Truncate long output
                if stderr_text:
                    logger.info(f"Manim stderr: {stderr_text[:500]}...")
                
                if process.returncode != 0:
                    logger.error(f"Manim rendering failed with return code {process.returncode}")
                    logger.error(f"Command: {' '.join(cmd)}")
                    logger.error(f"Stderr: {stderr_text}")
                    logger.error(f"Stdout: {stdout_text}")
                    raise RuntimeError(f"Manim rendering failed: {stderr_text or stdout_text or 'Unknown error'}")
                
                logger.info("Manim rendering completed successfully")
                
            except asyncio.TimeoutError:
                if process:
                    try:
                        process.terminate()
                        await process.wait()
                    except:
                        pass
                logger.error("Manim rendering timed out after 3 minutes")
                raise RuntimeError("Manim rendering timed out after 3 minutes")
            
            except Exception as e:
                if process:
                    try:
                        process.terminate()
                        await process.wait()
                    except:
                        pass
                raise e
            
            # Find the output video file
            video_path = self._find_output_video()
            
            if not video_path:
                raise FileNotFoundError("Rendered video file not found")
            
            logger.info(f"Animation rendered successfully: {video_path}")
            return video_path
            
        except Exception as e:
            logger.error(f"Error rendering animation: {e}")
            raise
    
    def _find_output_video(self) -> Optional[str]:
        """Find the rendered video file in the output directory."""
        # Look for video files in media directory
        media_dir = self.output_dir / "videos"
        
        if media_dir.exists():
            for video_file in media_dir.rglob("*.mp4"):
                if "EducationalScene" in video_file.name:
                    return str(video_file)
        
        # Also check direct output directory
        for video_file in self.output_dir.glob("*.mp4"):
            return str(video_file)
        
        return None
    
    def create_custom_scene(self, scene_name: str, animations: List[Dict]) -> str:
        """
        Create a custom scene with specific animations.
        
        Args:
            scene_name: Name of the scene
            animations: List of animation specifications
            
        Returns:
            Path to the custom scene file
        """
        try:
            scene_code = f'''"""
Custom Manim scene: {scene_name}
"""

from manim import *
import numpy as np

class {scene_name}(Scene):
    def construct(self):
        self.camera.background_color = "#0e1116"
        
        {self._generate_custom_animations(animations)}

'''
            
            # Write custom scene file
            scene_file_path = self.output_dir / f"{scene_name.lower()}.py"
            with open(scene_file_path, 'w', encoding='utf-8') as f:
                f.write(scene_code)
            
            return str(scene_file_path)
            
        except Exception as e:
            logger.error(f"Error creating custom scene: {e}")
            raise
    
    def _generate_custom_animations(self, animations: List[Dict]) -> str:
        """Generate code for custom animations."""
        animation_code = ""
        
        for i, anim in enumerate(animations):
            anim_type = anim.get('type', 'text')
            
            if anim_type == 'text':
                text = anim.get('text', f'Animation {i}')
                animation_code += f'''
        text_{i} = Text("{text}", font_size=24, color=WHITE)
        self.play(Write(text_{i}))
        self.wait(2)
        self.play(FadeOut(text_{i}))
        '''
            
            elif anim_type == 'equation':
                equation = anim.get('equation', 'x^2 + y^2 = 1')
                animation_code += f'''
        eq_{i} = Text(r"{equation}", font_size=36, color=BLUE)
        self.play(Write(eq_{i}))
        self.wait(3)
        self.play(FadeOut(eq_{i}))
        '''
            
            elif anim_type == 'graph':
                function = anim.get('function', 'x**2')
                animation_code += f'''
        axes_{i} = Axes(x_range=[-3, 3], y_range=[-2, 2])
        graph_{i} = axes_{i}.plot(lambda x: {function}, color=BLUE)
        self.play(Create(axes_{i}))
        self.play(Create(graph_{i}))
        self.wait(3)
        self.play(FadeOut(axes_{i}), FadeOut(graph_{i}))
        '''
        
        return animation_code
    
    def get_animation_duration(self, script_data: Dict[str, Any]) -> float:
        """
        Estimate the total animation duration.
        
        Args:
            script_data: Educational script data
            
        Returns:
            Estimated duration in seconds
        """
        base_duration = 10  # Title sequence
        
        for section in script_data.get('sections', []):
            section_duration = section.get('duration_estimate', 30)
            base_duration += section_duration
        
        base_duration += 5  # Summary
        
        return base_duration
    
    def test_manim_installation(self) -> Dict[str, Any]:
        """Test if Manim is properly installed and configured."""
        try:
            import subprocess
            
            # Test manim command
            result = subprocess.run(
                ['manim', '--version'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10
            )
            
            return {
                'manim_available': result.returncode == 0,
                'version': result.stdout.strip() if result.returncode == 0 else None,
                'error': result.stderr if result.returncode != 0 else None
            }
        except Exception as e:
            return {
                'manim_available': False,
                'version': None,
                'error': str(e)
            }
    
# Example usage
if __name__ == "__main__":
    async def test_animator():
        """Test the animator functionality."""
        try:
            animator = VideoAnimator()
            
            # Sample script data
            sample_script = {
                "title": "Linear Regression Explained",
                "sections": [
                    {
                        "title": "Introduction to Linear Regression",
                        "content": "Linear regression is a fundamental statistical method",
                        "section_type": "introduction",
                        "visual_cues": ["show graph"],
                        "math_expressions": ["y = mx + b"],
                        "duration_estimate": 30
                    },
                    {
                        "title": "Mathematical Foundation",
                        "content": "The mathematical foundation involves finding the best fit line",
                        "section_type": "concept",
                        "visual_cues": ["animate line fitting"],
                        "math_expressions": ["\\sum (y_i - \\hat{y_i})^2"],
                        "duration_estimate": 45
                    }
                ]
            }
            
            print("Testing animation creation...")
            
            # Generate scene file
            scene_file = animator._generate_scene_file(sample_script)
            print(f"Scene file generated: {scene_file}")
            
            # Note: Actual rendering requires Manim to be installed
            print("Scene file created successfully. To render, run:")
            print(f"manim -qm {scene_file} EducationalScene")
            
        except Exception as e:
            print(f"Test failed: {e}")
    
    # Run test
    asyncio.run(test_animator())
