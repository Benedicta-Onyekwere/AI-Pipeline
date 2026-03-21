# Gemini CLI Installation Guide (Codespaces)

Follow these steps sequentially to set up the Gemini CLI in a GitHub Codespace environment.

## Phase 1: Preparation
1.  **Create a GitHub Repository**: Create a new repository on your GitHub account.
2.  **Upload Files**: Upload any initial files you want to work with (e.g., PDFs or data files).
3.  **Commit**: Commit the uploaded files to the main branch.
4.  **Open Codespaces**: Click the **Code** button, select the **Codespaces** tab, and click **Create codespace on main**.

## Phase 2: CLI Installation
Once the terminal in your Codespace is ready, run these commands in order:

### 1. Initialize PNPM
Run the setup command:
```bash
pnpm setup
```
**Important**: Follow the prompt's instructions. You will likely need to run the `source` command provided in the output (e.g., `source /home/codespace/.bashrc`) to apply the changes to your current session.

### 2. Install Gemini CLI
Install the package globally:
```bash
pnpm add -g @google/gemini-cli
```

It can also be easily installed using npm:
```bash
npm install -g @google/gemini-cli
```

Or run without installation using npx:
```bash
npx @google/gemini-cli
```

### 3. Approve Builds
Grant the necessary permissions for the CLI:
```bash
pnpm approve-builds -g
```

### 4. Authentication and Setup
1.  **Connect Prompt**: When asked if you want to connect to Gemini, click **No** (or select the negative option).
2.  **Google Account Link**: The terminal will provide a URL for your Google account. Copy this link.
3.  **Browser Login**: Open the link in a **different browser window** or a private tab.
4.  **Get Password**: Follow the authentication flow on the webpage to generate your password/authorization code.
5.  **Input Code**: Paste the code back into the terminal prompt and press **Enter**.

---
**Success!** You can now start using the Gemini CLI in your Codespace.

## The Power of Gemini CLI (Beyond the Chatbot)

Unlike a traditional chatbot that is restricted to text in a browser window, the **Gemini CLI** is a senior-level AI engineer that lives directly within your development environment.

### What the CLI Can Do (That a Chatbot Can't)
*   **Direct File Manipulation**: In this session, the CLI read a complex PDF (`lecture_1_slides.pdf`), analyzed its contents, and **automatically created** a brand-new summary file (`lecture_1_summary.md`) without any copy-pasting required from the user.
*   **Integrated Workflow Automation**: The CLI doesn't just explain concepts—it executes the follow-up tasks. It successfully **committed** the new summary file and **pushed** it directly to the main GitHub repository on its own.
*   **Contextual Awareness**: It understands your entire project structure. It can audit your folders, check your Git status, and update your `README.md` based on real-time session progress.
*   **Tool-Augmented Action**: It uses specialized tools (like `grep`, `read_file`, and `run_shell_command`) to interact with your system, allowing you to bridge the gap between AI analysis and actual code execution.

**In essence, the Gemini CLI isn't just a conversational assistant—it is a proactive collaborator that turns your verbal instructions into immediate, verified project updates.**
