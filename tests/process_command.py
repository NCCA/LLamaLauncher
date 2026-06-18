"""Pure command-building logic for llama-server process.

Extracted from main.py to enable unit testing without Qt dependencies.
Accepts a configuration dictionary and returns a list of command arguments
suitable for QProcess or subprocess.
"""

from typing import Any


class ProcessCommandBuilder:
    """Build llama-server command from configuration dictionary.

    Takes a config dict (from ConfigCollector.collect_config()) and returns
    a list of command arguments suitable for QProcess or subprocess.

    Attributes:
        config: Configuration dictionary containing files, server, sampling,
            performance, and advanced parameter settings.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize the builder with configuration.

        Args:
            config: Configuration dictionary from ConfigCollector.
        """
        self._config = config

    def build_command(self) -> list[str]:
        """Build the complete llama-server command.

        Returns:
            List of command arguments starting with 'llama-server'.
        """
        cmd: list[str] = []

        # 3.1 Base command
        cmd.extend(["llama-server", "--model", self._config["files"]["model_path"]])

        api_key = self._config["server"]["api_key"] or "12345"
        cmd.extend(["--api-key", api_key])

        # 3.2 Sampling parameters (conditional)
        sampling = self._config["sampling"]

        if sampling["temperature"]["enabled"]:
            cmd.extend(["--temp", str(sampling["temperature"]["value"])])
        if sampling["top_p"]["enabled"]:
            cmd.extend(["--top-p", str(sampling["top_p"]["value"])])
        if sampling["top_k"]["enabled"]:
            cmd.extend(["--top-k", str(sampling["top_k"]["value"])])
        if sampling["min_p"]["enabled"]:
            cmd.extend(["--min-p", str(sampling["min_p"]["value"])])
        if sampling["typical_p"]["enabled"]:
            cmd.extend(["--typical-p", str(sampling["typical_p"]["value"])])
        if sampling["repeat_penalty"]["enabled"]:
            cmd.extend(["--repeat-penalty", str(sampling["repeat_penalty"]["value"])])
        if sampling["repeat_last_n"]["enabled"]:
            cmd.extend(["--repeat-last-n", str(sampling["repeat_last_n"]["value"])])
        if sampling["presence_penalty"]["enabled"]:
            cmd.extend(
                ["--presence-penalty", str(sampling["presence_penalty"]["value"])]
            )
        if sampling["frequency_penalty"]["enabled"]:
            cmd.extend(
                ["--frequency-penalty", str(sampling["frequency_penalty"]["value"])]
            )
        if sampling["mirostat"]["enabled"]:
            cmd.extend(["--mirostat", str(sampling["mirostat"]["value"])])
        if sampling["mirostat_lr"]["enabled"]:
            cmd.extend(["--mirostat-lr", str(sampling["mirostat_lr"]["value"])])
        if sampling["mirostat_ent"]["enabled"]:
            cmd.extend(["--mirostat-ent", str(sampling["mirostat_ent"]["value"])])

        # 3.5 Server and Model Parameters
        # MMProj parameters
        mmproj_path = self._config["files"]["mmproj_path"]
        if mmproj_path:
            cmd.extend(["--mmproj", mmproj_path])
            if self._config.get("no_mmproj_offload", False):
                cmd.append("--no-mmproj-offload")

        # Extra flags from more_options
        more_options = self._config.get("more_options", "")
        if more_options:
            cmd.extend(more_options.split())

        # Context size
        context_size = self._config.get("context_size", 0)
        if context_size and context_size > 0:
            cmd.extend(["--ctx-size", str(context_size)])

        # Server settings
        server = self._config["server"]
        cmd.extend(["--host", server["host"], "--port", str(server["port"])])

        return cmd
