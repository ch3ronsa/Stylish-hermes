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


def patch_gateway(gateway_path: Path) -> None:
    text = gateway_path.read_text(encoding="utf-8")

    old_env_block = """        _agent_cfg = _cfg.get("agent", {})
        if _agent_cfg and isinstance(_agent_cfg, dict):
            if "max_turns" in _agent_cfg:
                os.environ["HERMES_MAX_ITERATIONS"] = str(_agent_cfg["max_turns"])
"""
    new_env_block = """        _agent_cfg = _cfg.get("agent", {})
        if _agent_cfg and isinstance(_agent_cfg, dict):
            if "max_turns" in _agent_cfg:
                os.environ["HERMES_MAX_ITERATIONS"] = str(_agent_cfg["max_turns"])
            if "max_tokens" in _agent_cfg:
                os.environ["HERMES_MAX_TOKENS"] = str(_agent_cfg["max_tokens"])
"""
    if old_env_block in text:
        text = text.replace(old_env_block, new_env_block, 1)
    elif 'os.environ["HERMES_MAX_TOKENS"]' not in text:
        raise RuntimeError("Could not find agent env block in gateway/run.py")

    marker = "            pr = self._provider_routing\n"
    inject = """            pr = self._provider_routing
            max_tokens = None
            try:
                max_tokens_env = os.getenv("HERMES_MAX_TOKENS")
                if max_tokens_env:
                    max_tokens = int(max_tokens_env)
            except Exception:
                max_tokens = None
"""
    if marker in text and "max_tokens_env = os.getenv(\"HERMES_MAX_TOKENS\")" not in text:
        text = text.replace(marker, inject, 1)

    old_agent_call = """                platform=platform_key,
                honcho_session_key=session_key,
                session_db=self._session_db,
            )
"""
    new_agent_call = """                platform=platform_key,
                honcho_session_key=session_key,
                session_db=self._session_db,
                max_tokens=max_tokens,
            )
"""
    if old_agent_call in text:
        text = text.replace(old_agent_call, new_agent_call, 1)
    elif "max_tokens=max_tokens" not in text:
        raise RuntimeError("Could not find main gateway agent call in gateway/run.py")

    backup = gateway_path.with_suffix(".py.bak")
    if not backup.exists():
        shutil.copy2(gateway_path, backup)
    gateway_path.write_text(text, encoding="utf-8")


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
    gateway_path = home / ".hermes" / "hermes-agent" / "gateway" / "run.py"
    config_path = home / ".hermes" / "config.yaml"
    patch_cli(cli_path)
    patch_gateway(gateway_path)
    patch_config(config_path)
    print("Patched Hermes CLI + gateway and set agent.max_tokens=4096")


if __name__ == "__main__":
    main()
