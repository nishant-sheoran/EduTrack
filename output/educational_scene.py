"""
Generated Manim scene for: Linear Regression Explained
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
        
        # Main content sections
        self.section_0()  # What is Linear Regression?
        self.section_1()  # Mathematical Foundation
        self.section_2()  # Real-World Example
        
        # Final summary
        self.create_summary()
    
    def create_title_sequence(self):
        """Create animated title sequence."""
        title = Text("Linear Regression Explained", font_size=48, color=BLUE)
        subtitle = Text("An Educational Explanation", font_size=24, color=YELLOW)
        subtitle.next_to(title, DOWN, buff=0.5)
        
        # Animate title
        self.play(Write(title), run_time=2)
        self.play(FadeIn(subtitle), run_time=1)
        self.wait(2)
        
        # Clear title
        self.play(FadeOut(title), FadeOut(subtitle))
        self.wait(0.5)
    
    
    def section_0(self):
        """Section: What is Linear Regression?"""
        # Section title
        section_title = Text("What is Linear Regression?", font_size=32, color=BLUE)
        section_title.to_edge(UP)
        
        self.play(Write(section_title))
        self.wait(1)
        
        
        # Concept explanation
        concept_text = Text("Key Concept", font_size=24, color=WHITE)
        concept_text.to_edge(LEFT).shift(UP * 2)
        
        self.play(Write(concept_text))
        self.wait(1)
        
        
        # Mathematical expressions
        
        math_expr_0 = Text(r"y = mx + b", font_size=36, color=BLUE)
        math_expr_0.next_to(concept_text, DOWN, buff=1)
        self.play(Write(math_expr_0))
        self.wait(2)
        
        math_expr_1 = Text(r"\\hat{y} = \\beta_0 + \\beta_1 x", font_size=36, color=BLUE)
        math_expr_1.next_to(concept_text, DOWN, buff=1)
        self.play(Write(math_expr_1))
        self.wait(2)
        
        self.wait(1)
        
        
        # Clear section
        self.clear()
        self.wait(0.5)


    def section_1(self):
        """Section: Mathematical Foundation"""
        # Section title
        section_title = Text("Mathematical Foundation", font_size=32, color=BLUE)
        section_title.to_edge(UP)
        
        self.play(Write(section_title))
        self.wait(1)
        
        
        # Concept explanation
        concept_text = Text("Key Concept", font_size=24, color=WHITE)
        concept_text.to_edge(LEFT).shift(UP * 2)
        
        self.play(Write(concept_text))
        self.wait(1)
        
        
        # Mathematical expressions
        
        math_expr_0 = Text(r"\\min \\sum_{i=1}^{n} (y_i - \\hat{y_i})^2", font_size=36, color=BLUE)
        math_expr_0.next_to(concept_text, DOWN, buff=1)
        self.play(Write(math_expr_0))
        self.wait(2)
        
        math_expr_1 = Text(r"RSS = \\sum_{i=1}^{n} (y_i - \\hat{y_i})^2", font_size=36, color=BLUE)
        math_expr_1.next_to(concept_text, DOWN, buff=1)
        self.play(Write(math_expr_1))
        self.wait(2)
        
        self.wait(1)
        
        
        # Clear section
        self.clear()
        self.wait(0.5)


    def section_2(self):
        """Section: Real-World Example"""
        # Section title
        section_title = Text("Real-World Example", font_size=32, color=BLUE)
        section_title.to_edge(UP)
        
        self.play(Write(section_title))
        self.wait(1)
        
        
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
        
        
        # Clear section
        self.clear()
        self.wait(0.5)

    
    def create_summary(self):
        """Create summary section."""
        summary_title = Text("Summary", font_size=36, color=YELLOW)
        summary_title.to_edge(UP)
        
        self.play(Write(summary_title))
        self.wait(1)
        
        # Add summary points
        summary_text = Text("Key Takeaways", font_size=24, color=WHITE)
        summary_text.next_to(summary_title, DOWN, buff=1)
        
        self.play(FadeIn(summary_text))
        self.wait(3)
        
        self.play(FadeOut(summary_title), FadeOut(summary_text))
    
    
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

