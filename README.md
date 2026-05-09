# Automated SEO Keyword Strategist

## Project Description
The Automated SEO Keyword Strategist is a lightweight, local, multi-agent AI tool. It analyzes your website's keyword mappings and URL structures to identify "keyword cannibalization"—where multiple pages on your own website compete for the exact same search query. By utilizing two local Ollama models in a pipeline, the system automatically clusters search intents, detects internal conflicts, and formats the findings into a clean, actionable Markdown report.

## Tech Stack
- **Language**: Python 3
- **AI Engine**: Ollama (Local AI inference)
- **Logic & Reasoning Model**: `hf.co/Jackrong/Qwen3.5-9B-DeepSeek-V4-Flash-GGUF` (Used for heavy analytical lifting and clustering).
- **Formatting Model**: `granite-direct:latest` (Custom Granite model used to strictly structure raw analysis into professional markdown).

## Setup Steps
1. **Install Python 3**: Ensure Python 3.8+ is installed on your machine.
2. **Install Ollama**: Download and install Ollama from [ollama.com](https://ollama.com).
3. **Registering Models from GGUF files (For New Users)**:
   If you are downloading `.gguf` files manually from HuggingFace instead of pulling them automatically, follow these exact steps to register them:
   
   **A. Download the Model**
   - Download your `.gguf` file (e.g., `Qwen3.5-9B...gguf`) into your project folder.
   
   **B. Create a Modelfile**
   - Create a plain text file named `Modelfile` (no file extension) in the same folder.
   - Add the path to your downloaded file inside the Modelfile:
     ```text
     FROM ./Qwen3.5-9B-DeepSeek-V4-Flash-Q2_K.gguf
     ```
   
   **C. Build and Register in Ollama**
   - Open your terminal in that folder and run the create command:
     ```bash
     ollama create local-deepseek -f Modelfile
     ```
     *(Repeat this process for your Granite model, e.g., `ollama create granite-direct -f Modelfile_granite`)*

4. **Update the Script**: 
   If you registered your model under a custom name (like `local-deepseek`), ensure you open `main.py` and update the `QWEN_MODEL` and `GRANITE_MODEL` variables at the top of the file to match the exact names you just registered.

## Run Steps
1. Ensure the Ollama background service is running on your machine (it typically runs automatically on port `11434`).
2. Navigate to the project directory in your terminal.
3. Verify that `sample_seo_data.txt` and `main.py` are in the directory.
4. Execute the script:
   ```bash
   python main.py
   ```
5. Wait for the pipeline to finish. It will print its progress to the console.

## Test Steps
1. Open the `sample_seo_data.txt` file and modify the contents. Add duplicate keywords targeting completely different URLs (e.g., add two URLs targeting "best wireless headphones").
2. Run `python main.py`.
3. Open the newly generated `SEO_Report.md`.
4. Verify that the report caught your deliberately injected cannibalization issues and properly clustered the intent.

## Explanation of Code Files

### 1. `main.py`
This is the core execution script. It handles reading the data, orchestrating the HTTP requests to the Ollama local API, and writing the final output. It defines the models, system prompts, and handles the `disable_think` parameter to speed up the Qwen model's inference by disabling its `<think>` token generation. It passes the output from Stage 1 (Qwen) directly into Stage 2 (Granite) for formatting.

### 2. `sample_seo_data.txt`
This acts as our dummy database or CSV export from an SEO tool (like Ahrefs or Search Console). It contains rows of URLs paired with their primary target keywords, estimated traffic, and intended search intent (Commercial, Informational, Transactional).

### 3. `SEO_Report.md` (Generated)
This file is not present initially but is created by the `main.py` script. It contains the final polished output formatted by the Granite model, making it ready to be presented to clients or marketing teams.

## 5 Practical Business Use Cases
1. **E-commerce Auditing**: Automatically find product pages and category pages that are competing for the exact same commercial search term, diluting the ranking power of the main category.
2. **Blog Content Pruning**: Identify older informational blog posts that are cannibalizing traffic from newer, updated guides, allowing content teams to merge or redirect them.
3. **Agency Client Reporting**: Digital marketing agencies can feed raw Search Console data into the tool to instantly generate professional, white-labeled audit reports for new clients.
4. **Site Migration Management**: When migrating domains or changing URL structures, use the tool to ensure new URLs aren't accidentally mapped to keywords already successfully held by existing legacy pages.
5. **Localization Strategy**: Analyze multi-regional sites to ensure that the UK version of a page isn't accidentally cannibalizing the US version of a page on global search results.

## 5 Future Feature Additions
1. **CSV / Excel Parsing**: Upgrade the script to use `pandas` so it can ingest raw `.csv` or `.xlsx` exports directly from tools like Google Search Console or SEMrush.
2. **Automated Redirect Mapping**: Add a third agent that writes actual `.htaccess` or Nginx 301 redirect rules to fix the cannibalization issues it finds.
3. **Web Scraping Integration**: Implement BeautifulSoup to automatically crawl the live URLs and check their actual H1 tags and Title tags for deeper context.
4. **Token Usage Logging**: Implement a lightweight SQLite database to track how many tokens the Qwen and Granite models are consuming per run.
5. **Interactive CLI Dashboard**: Wrap the Python script in a terminal UI (using libraries like `rich` or `textual`) to visualize the clustering process in real-time.
