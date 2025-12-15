import os
from pathlib import Path
from .client import get_driver


def run_seed_script() -> None:
    driver = get_driver()
    current_dir = Path(__file__).parent
    
    schema_path = current_dir / "schema.cypher"
    seed_path = current_dir / "seed_data.cypher"
    
    with open(schema_path, encoding="utf-8") as f:
        schema_cypher = f.read()
    
    with open(seed_path, encoding="utf-8") as f:
        seed_cypher = f.read()
    
    cypher = schema_cypher + "\n" + seed_cypher
    
    lines = cypher.split("\n")
    cleaned_lines = []
    for line in lines:
        if line.strip().startswith("//"):
            continue
        if "//" in line:
            line = line[: line.index("//")]
        line = line.strip()
        if line:
            cleaned_lines.append(line)
    
    cleaned_cypher = "\n".join(cleaned_lines)
    
    with driver.session() as session:
        statements = cleaned_cypher.split(";")
        for stmt in statements:
            stmt = stmt.strip()
            if stmt:
                try:
                    session.run(stmt)
                except Exception as e:
                    if "already exists" not in str(e).lower() and "already in use" not in str(e).lower():
                        print(f"Warning: {e}")


if __name__ == "__main__":
    run_seed_script()


