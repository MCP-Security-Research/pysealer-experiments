#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

def run_command(command, cwd=None):
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(command, cwd=cwd, shell=True, check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        combined_output = "".join(part for part in [e.stdout, e.stderr] if part)
        return combined_output if combined_output else None

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pre_tool_poisoning = os.path.join(base_dir, "tool-poisoning", "tool_poisoning.py")
    pre_tool_shadowing = os.path.join(base_dir, "tool-shadowing", "tool_shadowing.py")

    print("")
    print("Evaluating Tool Poisoning and Tool Shadowing Attacks with pysealer...")

    # Run pysealer init
    run_command("pysealer init", cwd=os.path.dirname(pre_tool_poisoning))
    run_command("pysealer init", cwd=os.path.dirname(pre_tool_shadowing))

    # Run pysealer lock
    run_command(f"pysealer lock {pre_tool_poisoning}", cwd=os.path.dirname(pre_tool_poisoning))
    run_command(f"pysealer lock {pre_tool_shadowing}", cwd=os.path.dirname(pre_tool_shadowing))

    # Run pysealer check (no changes added)
    output_pre_poisoning = run_command(f"pysealer check {pre_tool_poisoning}", cwd=os.path.dirname(pre_tool_poisoning))
    output_pre_shadowing = run_command(f"pysealer check {pre_tool_shadowing}", cwd=os.path.dirname(pre_tool_shadowing))
    print("------------------------------------------------")
    print("Pre-Tool-Poisoning Output:")
    print(output_pre_poisoning)
    print("Pre-Tool-Shadowing Output:")
    print(output_pre_shadowing)
    print("------------------------------------------------")

    # Run execute scripts to perform attacks
    # this basically simulates the attacker doing their attack after the defender has locked the files
    run_command("python tool-poisoning/execute_tool_poisoning_attack.py", cwd=base_dir)
    run_command("python tool-shadowing/execute_tool_shadowing_attack.py", cwd=base_dir)

    # Run pysealer check on post-attack files
    output_post_poisoning = run_command(f"pysealer check {pre_tool_poisoning}", cwd=os.path.dirname(pre_tool_poisoning))
    output_post_shadowing = run_command(f"pysealer check {pre_tool_shadowing}", cwd=os.path.dirname(pre_tool_shadowing))
    print("------------------------------------------------")
    print("Post-Tool-Poisoning Output:")
    print(output_post_poisoning)
    print("Post-Tool-Shadowing Output:")
    print(output_post_shadowing)
    print("------------------------------------------------")

    # Cleanup
    run_command("unset PYSEALER_ENV_VAR")  # Example environment variable
    run_command("rm -f .git/hooks/pre-commit")  # Remove pre-commit hook if added
    # return the tool_poisoning.py and tool_shadowing.py files to their original state
    run_command("python tool-poisoning/unexecute_tool_poisoning_attack.py", cwd=base_dir)
    run_command("python tool-shadowing/unexecute_tool_shadowing_attack.py", cwd=base_dir)
    print("")

    # Run mcp-scan on the post-attack files to see if it detects the attacks
    print("Evaluating Tool Poisoning and Tool Shadowing Attacks with mcp-scan...")

    # Run mcp-scan on pre-attack files
    poisoning_pre_scan_output = run_command(f"mcp-scan scan tool-poisoning/pre_mcp_config.json", cwd=base_dir)
    shadowing_pre_scan_output = run_command(f"mcp-scan scan tool-shadowing/pre_mcp_config.json", cwd=base_dir)
    print("------------------------------------------------")
    print("Pre-Tool-Poisoning Output:")
    print(poisoning_pre_scan_output)
    print("Pre-Tool-Shadowing Output:")
    print(shadowing_pre_scan_output)
    print("------------------------------------------------")

    # Run mcp-scan on post-attack files
    poisoning_post_scan_output = run_command(f"mcp-scan scan tool-poisoning/post_mcp_config.json", cwd=base_dir)
    shadowing_post_scan_output = run_command(f"mcp-scan scan tool-shadowing/post_mcp_config.json", cwd=base_dir)
    print("------------------------------------------------")
    print("Post-Tool-Poisoning Output:")
    print(poisoning_post_scan_output)
    print("Post-Tool-Shadowing Output:")
    print(shadowing_post_scan_output)
    print("------------------------------------------------")
    print("")

if __name__ == "__main__":
    main()