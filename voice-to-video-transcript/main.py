"""
Simple command-line interface for the Auto Educational Video Generator.

This module provides a simple CLI for testing and using the video generation pipeline.
"""

import argparse
import os
import sys
from typing import List

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pipeline import VideoGenerationPipeline

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Note: python-dotenv not installed. You can install it with: pip install python-dotenv")
    print("Alternatively, set OPENAI_API_KEY as a system environment variable.")

def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Auto Educational Video Generator - Create educational videos using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py "Explain Linear Regression"
  python main.py "Bayes Theorem" --preview
  python main.py "Calculus Derivatives" --output my_video.mp4
  python main.py --batch "Linear Regression" "Bayes Theorem" "Neural Networks"
        """
    )
    
    parser.add_argument(
        "topic",
        nargs="*",
        help="Educational topic to create video for"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Output filename for the video"
    )
    
    parser.add_argument(
        "--output-dir", "-d",
        type=str,
        default="output",
        help="Output directory for videos (default: output)"
    )
    
    parser.add_argument(
        "--preview", "-p",
        action="store_true",
        help="Generate a short preview instead of full video"
    )
    
    parser.add_argument(
        "--batch", "-b",
        action="store_true",
        help="Process multiple topics in batch mode"
    )
    
    parser.add_argument(
        "--no-cleanup",
        action="store_true",
        help="Keep temporary files for debugging"
    )
    
    parser.add_argument(
        "--status", "-s",
        action="store_true",
        help="Show pipeline status and exit"
    )
    
    parser.add_argument(
        "--list-videos", "-l",
        action="store_true",
        help="List existing videos in output directory"
    )
    
    args = parser.parse_args()
    
    # Initialize pipeline
    pipeline = VideoGenerationPipeline(
        output_dir=args.output_dir,
        cleanup_temp=not args.no_cleanup
    )
    
    # Handle status command
    if args.status:
        print("📊 Pipeline Status:")
        print("=" * 40)
        status = pipeline.get_pipeline_status()
        for key, value in status.items():
            if isinstance(value, dict):
                print(f"{key}:")
                for sub_key, sub_value in value.items():
                    print(f"  {sub_key}: {sub_value}")
            else:
                print(f"{key}: {value}")
        return
    
    # Handle list videos command
    if args.list_videos:
        print("📹 Existing Videos:")
        print("=" * 40)
        if os.path.exists(args.output_dir):
            video_files = [f for f in os.listdir(args.output_dir) if f.endswith('.mp4')]
            if video_files:
                for i, video_file in enumerate(video_files, 1):
                    video_path = os.path.join(args.output_dir, video_file)
                    size_mb = os.path.getsize(video_path) / (1024 * 1024)
                    print(f"{i:2d}. {video_file} ({size_mb:.1f} MB)")
            else:
                print("No videos found.")
        else:
            print(f"Output directory '{args.output_dir}' does not exist.")
        return
    
    # Check if topic is provided
    if not args.topic:
        print("❌ Error: Please provide a topic.")
        print("Example: python main.py \"Explain Linear Regression\"")
        parser.print_help()
        return
    
    # Handle batch mode
    if args.batch:
        print(f"🎬 Batch Mode: Processing {len(args.topic)} topics")
        videos = pipeline.batch_generate(args.topic)
        
        print(f"\n📊 Batch Results:")
        print(f"✅ Successful: {len(videos)}/{len(args.topic)}")
        
        if videos:
            print("\n📹 Generated Videos:")
            for video in videos:
                print(f"  • {os.path.basename(video)}")
        
        return
    
    # Handle single topic
    topic = " ".join(args.topic)
    
    if args.preview:
        print(f"🎬 Generating preview for: {topic}")
        video_path = pipeline.generate_preview(topic)
    else:
        print(f"🎬 Generating full video for: {topic}")
        video_path = pipeline.run_pipeline(topic, args.output)
    
    if video_path:
        print(f"\n🎉 Success! Video saved to: {video_path}")
        
        # Show file info
        if os.path.exists(video_path):
            size_mb = os.path.getsize(video_path) / (1024 * 1024)
            print(f"📊 File size: {size_mb:.1f} MB")
    else:
        print("\n❌ Failed to generate video.")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Generation interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
