"""
Manim Code Generator Module

This module uses an LLM to generate Manim animation code based on scene text.
"""

import os
import openai
from typing import Optional

def generate_manim_code(scene_text: str, api_key: Optional[str] = None) -> str:
    """
    Generates Manim scene code from text using an LLM.

    Args:
        scene_text: The text content of the scene.
        api_key: The OpenAI API key.

    Returns:
        A string containing the Python code for the `construct` method of a Manim scene.
    """
    if not api_key:
        print("Warning: OPENAI_API_KEY not found. Using dummy Manim code.")
        # Fallback to a simple placeholder if no API key is available
        return f'''def construct(self):
    # Create a title from the first line of the text
    scene_text = """{scene_text.replace('"""', '\\"""')}"""
    lines = scene_text.strip().split('\\n')
    title_text = lines[0] if lines else "Placeholder"
    title = self.create_title(title_text)
    self.play(Write(title))

    # Display the rest of the text
    rest_of_text = '\\n'.join(lines[1:]).strip()
    if rest_of_text:
        content = self.create_paragraph_text(rest_of_text)
        content.next_to(title, DOWN, buff=0.5)
        self.play(Write(content))
    
    self.wait(2)'''

    try:
        openai.api_key = api_key
        
        prompt = f"""
        You are an expert Manim programmer. Your task is to generate the Python code for the `construct` method of a Manim `Scene` to create a compelling, 3Blue1Brown-style educational animation.

        The animation must visualize the following text:
        ---
        {scene_text}
        ---

        **Instructions:**
        1.  The code should be for the `construct(self)` method ONLY. Do not include the class definition.
        2.  Use ManimCE. Assume all necessary Manim objects are imported.
        3.  The animation should be visually engaging and reflect the 3Blue1Brown aesthetic (e.g., dark background, clear typography, fluid animations).
        4.  Use helper methods available on the `self` object when appropriate:
            - `self.create_title(text: str)`: Creates a styled and wrapped title.
            - `self.create_paragraph_text(text: str)`: Creates a wrapped paragraph.
            - `self.create_bullet_point(text: str)`: Creates a formatted bullet point.
        5.  The first line of the provided text should be the title. Use `self.create_title()` for it.
        6.  Use the remaining text as the main content for the visualization.
        7.  Generate creative and relevant visuals (graphs, shapes, code blocks, etc.) that match the text. Do NOT just display the text.
        8.  Ensure the animation timing is reasonable. Use `self.wait()` to pause where appropriate.

        **Example Code Structure:**
        ```python
        def construct(self):
            # 1. Create the title from the first line of the text.
            title = self.create_title("This is the Title")
            self.play(Write(title))
            self.wait(1)

            # 2. Create visualizations for the rest of the text.
            #    (e.g., create shapes, graphs, formulas, etc.)
            circle = Circle()
            self.play(Create(circle))
            self.wait(1)
        ```

        Now, generate the `construct` method for the provided text.
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a Manim programming expert."},
                {"role": "user", "content": prompt}
            ]
        )
        
        generated_code = response.choices[0].message['content']
        
        # Clean up the response to ensure it's valid Python code
        if "```python" in generated_code:
            generated_code = generated_code.split("```python")[1].split("```")[0]
        
        return generated_code.strip()

    except Exception as e:
        print(f"Error generating Manim code with LLM: {e}")
        # Fallback to the dummy code on API error
        return f'''def construct(self):
    scene_text = """{scene_text.replace('"""', '\\"""')}"""
    lines = scene_text.strip().split('\\n')
    title_text = lines[0] if lines else "Error"
    title = self.create_title(title_text)
    self.play(Write(title))
    error_text = self.create_paragraph_text("Could not generate visualization.\\nFalling back to placeholder.")
    error_text.next_to(title, DOWN, buff=0.5)
    self.play(Write(error_text))
    self.wait(2)'''
