import gradio as gr
import os
import requests
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import google.generativeai as genai
from typing import Optional, List, Dict

# Load environment variables
load_dotenv(override=True)
api_key = os.getenv('GEMINI_API_KEY')

# Configure Gemini API
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-2.5-flash-lite')
else:
    model = None

# Global storage for summaries
summaries_history = []
SUMMARIES_FILE = "summaries_history.json"

# Headers for web scraping
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:
    """Enhanced website scraper with better error handling"""

    def __init__(self, url: str):
        self.url = url
        self.title = "Unknown Title"
        self.text = ""
        self.error = None

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            self.title = soup.title.string if soup.title else "No title found"

            # Remove script and style elements
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()

            self.text = soup.body.get_text(separator="\n", strip=True) if soup.body else ""

        except requests.exceptions.RequestException as e:
            self.error = f"Failed to fetch website: {str(e)}"
        except Exception as e:
            self.error = f"Error processing website: {str(e)}"

def create_system_prompt(summary_type: str = "short") -> str:
    """Create system prompt based on summary type"""
    base_prompt = "You are an assistant that analyzes the contents of a website and provides a summary, ignoring text that might be navigation related."

    if summary_type == "short":
        return base_prompt + " Respond with a short summary in markdown."
    elif summary_type == "detailed":
        return base_prompt + " Respond with a detailed summary in markdown, including key points and main topics."
    elif summary_type == "bullet_points":
        return base_prompt + " Respond with a bullet-point summary in markdown, highlighting the main ideas."
    else:
        return base_prompt + " Respond in markdown."

def summarize_website(url: str, summary_type: str = "short") -> str:
    """Main function to summarize a website"""
    if not api_key:
        return "❌ **Error**: No Gemini API key found. Please check your .env file."

    if not model:
        return "❌ **Error**: Failed to initialize Gemini model."

    try:
        # Scrape the website
        website = Website(url)

        if website.error:
            return f"❌ **Error**: {website.error}"

        if not website.text.strip():
            return "❌ **Error**: No content could be extracted from the website."

        # Create the prompt
        system_prompt = create_system_prompt(summary_type)

        user_prompt = f"You are looking at a website titled '{website.title}'\n\n"
        user_prompt += "The contents of this website are as follows; please provide a summary of this website in markdown. "
        user_prompt += "If it includes news or announcements, summarize these too.\n\n"
        user_prompt += website.text[:8000]  # Limit text length to avoid token limits

        # Generate summary using Gemini
        chat = model.start_chat(history=[])
        response = chat.send_message(user_prompt)

        return response.text

    except Exception as e:
        return f"❌ **Error**: Failed to generate summary: {str(e)}"

def save_summary(url: str, summary: str, summary_type: str) -> Dict:
    """Save a summary to history"""
    timestamp = datetime.now().isoformat()
    summary_data = {
        "url": url,
        "summary": summary,
        "summary_type": summary_type,
        "timestamp": timestamp,
        "title": Website(url).title if not Website(url).error else "Unknown Title"
    }

    summaries_history.append(summary_data)

    # Save to file
    try:
        with open(SUMMARIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(summaries_history, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Warning: Could not save to file: {e}")

    return summary_data

def load_summaries() -> List[Dict]:
    """Load summaries from file"""
    global summaries_history
    try:
        if os.path.exists(SUMMARIES_FILE):
            with open(SUMMARIES_FILE, 'r', encoding='utf-8') as f:
                summaries_history = json.load(f)
    except Exception as e:
        print(f"Warning: Could not load summaries: {e}")
        summaries_history = []
    return summaries_history

def summarize_multiple(urls_text: str, summary_type: str = "short", progress=gr.Progress()) -> str:
    """Summarize multiple URLs"""
    if not api_key:
        return "❌ **Error**: No Gemini API key found. Please check your .env file."

    if not urls_text.strip():
        return "❌ **Error**: Please enter at least one URL."

    urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
    if not urls:
        return "❌ **Error**: No valid URLs found."

    results = []
    total_urls = len(urls)

    for i, url in enumerate(urls):
        progress((i) / total_urls, f"Processing {i+1}/{total_urls}: {url}")

        try:
            summary = summarize_website(url, summary_type)
            if not summary.startswith("❌"):
                save_summary(url, summary, summary_type)
                results.append(f"## {Website(url).title}\n**URL:** {url}\n\n{summary}\n")
            else:
                results.append(f"## ❌ {Website(url).title}\n**URL:** {url}\n\n{summary}\n")

            # Small delay to avoid rate limits
            time.sleep(1)

        except Exception as e:
            results.append(f"## ❌ Error\n**URL:** {url}\n\n❌ **Error**: {str(e)}\n")

        progress((i + 1) / total_urls)

    return "\n---\n".join(results)

def export_summaries(format_type: str = "markdown") -> str:
    """Export all summaries in different formats"""
    if not summaries_history:
        return "❌ **Error**: No summaries to export."

    if format_type == "markdown":
        output = "# Website Summaries Export\n\n"
        for summary in summaries_history:
            output += f"## {summary['title']}\n"
            output += f"**URL:** {summary['url']}\n"
            output += f"**Summary Type:** {summary['summary_type']}\n"
            output += f"**Date:** {summary['timestamp']}\n\n"
            output += f"{summary['summary']}\n\n---\n\n"

    elif format_type == "json":
        output = json.dumps(summaries_history, indent=2, ensure_ascii=False)

    elif format_type == "txt":
        output = "WEBSITE SUMMARIES EXPORT\n\n"
        for summary in summaries_history:
            output += f"Title: {summary['title']}\n"
            output += f"URL: {summary['url']}\n"
            output += f"Type: {summary['summary_type']}\n"
            output += f"Date: {summary['timestamp']}\n"
            output += f"Summary:\n{summary['summary']}\n\n{'='*50}\n\n"

    return output

# Gradio Interface
def create_ui():
    """Create the main Gradio interface"""

    with gr.Blocks(
        title="Website Summarizer with Gemini AI",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px;
            margin: auto;
        }
        .title {
            text-align: center;
            color: #2563eb;
            font-size: 2.5em;
            margin-bottom: 1em;
        }
        .subtitle {
            text-align: center;
            color: #64748b;
            font-size: 1.2em;
            margin-bottom: 2em;
        }
        .tab-content {
            padding: 1em 0;
        }
        """
    ) as app:

        # Load existing summaries on startup
        load_summaries()

        # Header
        gr.HTML("""
        <div class="title">🌐 Website Summarizer</div>
        <div class="subtitle">Powered by Google's Gemini AI</div>
        """)

        # Tabs for different functionalities
        with gr.Tabs():

            # Single URL Tab
            with gr.Tab("🔗 Single URL"):
                with gr.Row():
                    with gr.Column(scale=3):
                        url_input = gr.Textbox(
                            label="Website URL",
                            placeholder="https://example.com",
                            lines=1,
                            info="Enter the URL of the website you want to summarize"
                        )

                    with gr.Column(scale=1):
                        summary_type = gr.Dropdown(
                            choices=["short", "detailed", "bullet_points"],
                            value="short",
                            label="Summary Type",
                            info="Choose your preferred summary style"
                        )

                with gr.Row():
                    summarize_btn = gr.Button(
                        "🚀 Summarize Website",
                        variant="primary",
                        size="lg"
                    )
                    clear_btn = gr.Button(
                        "🗑️ Clear",
                        variant="secondary"
                    )

                summary_output = gr.Markdown(
                    label="Summary",
                    show_label=True
                )

            # Batch Processing Tab
            with gr.Tab("📚 Batch Processing"):
                with gr.Row():
                    with gr.Column():
                        urls_input = gr.Textbox(
                            label="Website URLs",
                            placeholder="https://example1.com\nhttps://example2.com\nhttps://example3.com",
                            lines=8,
                            info="Enter multiple URLs, one per line"
                        )

                    with gr.Column():
                        batch_summary_type = gr.Dropdown(
                            choices=["short", "detailed", "bullet_points"],
                            value="short",
                            label="Summary Type",
                            info="Choose your preferred summary style"
                        )

                        batch_btn = gr.Button(
                            "🚀 Summarize All",
                            variant="primary",
                            size="lg"
                        )

                batch_output = gr.Markdown(
                    label="Batch Results",
                    show_label=True
                )

            # History & Export Tab
            with gr.Tab("📋 History & Export"):
                with gr.Row():
                    with gr.Column():
                        export_format = gr.Dropdown(
                            choices=["markdown", "json", "txt"],
                            value="markdown",
                            label="Export Format",
                            info="Choose export format for all summaries"
                        )

                        export_btn = gr.Button(
                            "📥 Export Summaries",
                            variant="primary"
                        )

                        clear_history_btn = gr.Button(
                            "🗑️ Clear History",
                            variant="secondary"
                        )

                    with gr.Column():
                        history_info = gr.Markdown(
                            value=f"**Total Summaries:** {len(summaries_history)}\n\n"
                            "Summaries are automatically saved to history when generated."
                        )

                export_output = gr.Textbox(
                    label="Export Data",
                    lines=15,
                    show_copy_button=True
                )

        # Status display (hidden but used for feedback)
        status_output = gr.Textbox(
            label="Status",
            visible=False
        )

        # Event handlers
        def process_single_summary(url, summary_type_value):
            if not url.strip():
                return "❌ Please enter a valid URL"

            try:
                result = summarize_website(url, summary_type_value)

                if not result.startswith("❌"):
                    # Save successful summary
                    save_summary(url, result, summary_type_value)
                    # Update history info
                    return result
                else:
                    return result

            except Exception as e:
                return f"❌ **Error**: {str(e)}"

        def process_batch_summary(urls_text, summary_type_value, progress=gr.Progress()):
            return summarize_multiple(urls_text, summary_type_value, progress)

        def export_data(format_type):
            global summaries_history
            if not summaries_history:
                return "❌ **Error**: No summaries to export."

            # Update history info first
            history_info.value = f"**Total Summaries:** {len(summaries_history)}\n\nSummaries are automatically saved to history when generated."

            return export_summaries(format_type)

        def clear_history():
            global summaries_history
            summaries_history = []
            try:
                if os.path.exists(SUMMARIES_FILE):
                    os.remove(SUMMARIES_FILE)
            except Exception as e:
                pass

            # Update history info
            history_info.value = "**Total Summaries:** 0\n\nSummaries are automatically saved to history when generated."

            return "✅ History cleared successfully!"

        def clear_single():
            return ""

        def clear_batch():
            return ""

        # Connect events
        summarize_btn.click(
            process_single_summary,
            inputs=[url_input, summary_type],
            outputs=[summary_output]
        )

        clear_btn.click(
            clear_single,
            inputs=[],
            outputs=[url_input]
        )

        batch_btn.click(
            process_batch_summary,
            inputs=[urls_input, batch_summary_type],
            outputs=[batch_output]
        )

        export_btn.click(
            export_data,
            inputs=[export_format],
            outputs=[export_output]
        )

        clear_history_btn.click(
            clear_history,
            inputs=[],
            outputs=[export_output]
        )

        # Footer
        gr.HTML("""
        <div style="text-align: center; margin-top: 2em; color: #64748b; font-size: 0.9em;">
            Built with Gradio and Google's Gemini AI
        </div>
        """)

    return app

# Launch the app
if __name__ == "__main__":
    app = create_ui()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_api=False
    )
