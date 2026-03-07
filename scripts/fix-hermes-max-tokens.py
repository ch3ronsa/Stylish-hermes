from pathlib import Path
import re
import shutil


def patch_cli(cli_path: Path) -> None:
    text = cli_path.read_text(encoding="utf-8")
    old_block = """        if max_turns is not None:  # CLI arg was explicitly set
            self.max_turns = max_turns
        elif CLI_CONFIG["agent"].get("max_turns"):
            self.max_turns = CLI_CONFIG["agent"]["max_turns"]
        elif CLI_CONFIG.get("max_turns"):  # Backwards compat: root-level max_turns
            self.max_turns = CLI_CONFIG["max_turns"]
        elif os.getenv("HERMES_MAX_ITERATIONS"):
            self.max_turns = int(os.getenv("HERMES_MAX_ITERATIONS"))
        else:
            self.max_turns = 90
"""
    new_block = old_block + """
        # Max output tokens priority: config file > root-level fallback > default None
        if CLI_CONFIG["agent"].get("max_tokens") is not None:
            self.max_tokens = int(CLI_CONFIG["agent"]["max_tokens"])
        elif CLI_CONFIG.get("max_tokens") is not None:
            self.max_tokens = int(CLI_CONFIG["max_tokens"])
        else:
            self.max_tokens = None
"""
    if old_block not in text and 'self.max_tokens = int(CLI_CONFIG["agent"]["max_tokens"])' in text:
        return
    if old_block not in text:
        raise RuntimeError("Could not find max_turns block in cli.py")
    text = text.replace(old_block, new_block, 1)

    old_call = """                honcho_session_key=self.session_id,
            )
"""
    new_call = """                honcho_session_key=self.session_id,
                max_tokens=self.max_tokens,
            )
"""
    if old_call in text:
        text = text.replace(old_call, new_call, 1)
    elif "max_tokens=self.max_tokens" not in text:
        raise RuntimeError("Could not find AIAgent call block in cli.py")

    backup = cli_path.with_suffix(".py.bak")
    if not backup.exists():
        shutil.copy2(cli_path, backup)
    cli_path.write_text(text, encoding="utf-8")


def patch_config(config_path: Path, limit: int = 4096) -> None:
    text = config_path.read_text(encoding="utf-8")
    if "  max_tokens:" not in text:
        needle = "agent:\n  max_turns: 60\n"
        repl = f"agent:\n  max_turns: 60\n  max_tokens: {limit}\n"
        if needle not in text:
            raise RuntimeError("Could not find agent block in config.yaml")
        text = text.replace(needle, repl, 1)
    else:
        text = re.sub(r"(^\s{2}max_tokens:\s*)\d+", rf"\g<1>{limit}", text, flags=re.M)

    backup = config_path.with_suffix(".yaml.bak")
    if not backup.exists():
        shutil.copy2(config_path, backup)
    config_path.write_text(text, encoding="utf-8")


def main() -> None:
    home = Path.home()
    cli_path = home / ".hermes" / "hermes-agent" / "cli.py"
    config_path = home / ".hermes" / "config.yaml"
    patch_cli(cli_path)
    patch_config(config_path)
    print("Patched Hermes CLI and set agent.max_tokens=4096")


if __name__ == "__main__":
    main()
