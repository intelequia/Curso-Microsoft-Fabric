import json
from pathlib import Path
from typing import Optional


def list_open_incidents(severity: Optional[str] = None) -> list:
    data_path = Path(__file__).parents[1] / "data" / "incidencias.json"
    incidents = json.loads(data_path.read_text(encoding="utf-8"))
    result = [item for item in incidents if item["status"] == "abierta"]
    if severity:
        result = [item for item in result if item["severity"] == severity.lower()]
    return result


if __name__ == "__main__":
    print(json.dumps(list_open_incidents(), ensure_ascii=False, indent=2))
