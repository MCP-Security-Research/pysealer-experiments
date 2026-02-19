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
    print("Evaluating Tool Poisoning and Tool Shadowing Attacks with PySealer...")

    # Step 1: Run pysealer init
    print("Running pysealer init...")
    run_command("pysealer init", cwd=os.path.dirname(pre_tool_poisoning))
    run_command("pysealer init", cwd=os.path.dirname(pre_tool_shadowing))

    # Step 2: Run pysealer lock
    print("Running pysealer lock...")
    run_command(f"pysealer lock {pre_tool_poisoning}", cwd=os.path.dirname(pre_tool_poisoning))
    run_command(f"pysealer lock {pre_tool_shadowing}", cwd=os.path.dirname(pre_tool_shadowing))

    # Step 3: Run pysealer check (no changes added)
    print("Running pysealer check (no changes)...")
    output_pre_poisoning = run_command(f"pysealer check {pre_tool_poisoning}", cwd=os.path.dirname(pre_tool_poisoning))
    output_pre_shadowing = run_command(f"pysealer check {pre_tool_shadowing}", cwd=os.path.dirname(pre_tool_shadowing))
    print("------------------------------------------------")
    print("Output before Attacks:")
    print(output_pre_poisoning)
    print(output_pre_shadowing)
    print("------------------------------------------------")

    # Step 4: Run execute scripts to perform attacks
    # this basically simulates the attacker doing their attack after the defender has locked the files
    print("Running execute scripts to perform attacks...")
    run_command("python tool-poisoning/execute_tool_poisoning_attack.py", cwd=base_dir)
    run_command("python tool-shadowing/execute_tool_shadowing_attack.py", cwd=base_dir)
    # if poisoning_exec_output:
    #  print(poisoning_exec_output.strip())
    #if shadowing_exec_output:
    #  print(shadowing_exec_output.strip())

    # Step 5: Run pysealer check on post-attack files
    print("Running pysealer check on post-attack files...")
    output_post_poisoning = run_command(f"pysealer check {pre_tool_poisoning}", cwd=os.path.dirname(pre_tool_poisoning))
    output_post_shadowing = run_command(f"pysealer check {pre_tool_shadowing}", cwd=os.path.dirname(pre_tool_shadowing))
    print("------------------------------------------------")
    print("Output after Attacks:")
    print(output_post_poisoning)
    print(output_post_shadowing)
    print("------------------------------------------------")

    # Display the content of the files after the attacks
    # print("Contents of tool_poisoning.py after attack:")
    # print(Path(pre_tool_poisoning).read_text())
    # print("Contents of tool_shadowing.py after attack:")
    # print(Path(pre_tool_shadowing).read_text())

    # Step 6: Cleanup
    print("Cleaning up...")
    run_command("unset PYSEALER_ENV_VAR")  # Example environment variable
    run_command("rm -f .git/hooks/pre-commit")  # Remove pre-commit hook if added
    print("")

if __name__ == "__main__":
    main()