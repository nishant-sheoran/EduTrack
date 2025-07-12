"""
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
        title_text = "Demystifying Time Complexity in Computer Science"
        
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
