import subprocess

def generate_preview_slug(text: str) -> str:
    # Bandit finding: shell command with unsanitized input
    cmd = f"echo {text} | tr '[:upper:]' '[:lower:]' | sed -e 's/[^a-z0-9]/-/g'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()
