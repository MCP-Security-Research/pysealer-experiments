import os
import subprocess

def run_command(command, cwd=None):
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(command, cwd=cwd, shell=True, check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}\n{e.stderr}")
        return None

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pre_tool_poisoning = os.path.join(base_dir, "tool-poisoning", "pre_tool_poisoning.py")
    pre_tool_shadowing = os.path.join(base_dir, "tool-shadowing", "pre_tool_shadowing.py")
    post_tool_poisoning = os.path.join(base_dir, "tool-poisoning", "post_tool_poisoning.py")
    post_tool_shadowing = os.path.join(base_dir, "tool-shadowing", "post_tool_shadowing.py")

    # Step 1: Run pysealer init
    print("Running pysealer init...")
    run_command("pysealer init", cwd=os.path.dirname(pre_tool_poisoning))
    run_command("pysealer init", cwd=os.path.dirname(pre_tool_shadowing))

    # Step 2: Run pysealer lock
    print("Running pysealer lock...")
    run_command("pysealer lock", cwd=os.path.dirname(pre_tool_poisoning))
    run_command("pysealer lock", cwd=os.path.dirname(pre_tool_shadowing))

    # Step 3: Run pysealer check (no changes added)
    print("Running pysealer check (no changes added)...")
    output_pre_poisoning = run_command("pysealer check", cwd=os.path.dirname(pre_tool_poisoning))
    output_pre_shadowing = run_command("pysealer check", cwd=os.path.dirname(pre_tool_shadowing))

    print("Output of pysealer check (pre-tool-poisoning):")
    print(output_pre_poisoning)
    print("Output of pysealer check (pre-tool-shadowing):")
    print(output_pre_shadowing)

    # Step 4: Apply changes from post-tool poisoning and post-tool shadowing
    print("Applying changes...")
    run_command(f"cp {post_tool_poisoning} {pre_tool_poisoning}")
    run_command(f"cp {post_tool_shadowing} {pre_tool_shadowing}")

    # Step 5: Run pysealer check (changes detected)
    print("Running pysealer check (changes detected)...")
    output_post_poisoning = run_command("pysealer check", cwd=os.path.dirname(pre_tool_poisoning))
    output_post_shadowing = run_command("pysealer check", cwd=os.path.dirname(pre_tool_shadowing))

    print("Output of pysealer check (post-tool-poisoning):")
    print(output_post_poisoning)
    print("Output of pysealer check (post-tool-shadowing):")
    print(output_post_shadowing)

    # Step 6: Cleanup
    print("Cleaning up...")
    run_command("unset PYSEALER_ENV_VAR")  # Example environment variable
    run_command("rm -f .git/hooks/pre-commit")  # Remove pre-commit hook if added

if __name__ == "__main__":
    main()