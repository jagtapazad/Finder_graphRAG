from .client import get_driver


def run_seed_script() -> None:
    driver = get_driver()
    with open("backend/kg/seed_data.cypher", encoding="utf-8") as f:
        cypher = f.read()
    
    # Remove comment lines and inline comments
    lines = cypher.split("\n")
    cleaned_lines = []
    for line in lines:
        # Remove inline comments (everything after //)
        if "//" in line:
            line = line[: line.index("//")]
        line = line.strip()
        # Skip empty lines and lines that are only whitespace
        if line:
            cleaned_lines.append(line)
    
    # Rejoin and split by semicolon
    cleaned_cypher = "\n".join(cleaned_lines)
    
    with driver.session() as session:
        for stmt in cleaned_cypher.split(";"):
            stmt = stmt.strip()
            if stmt:
                session.run(stmt)


if __name__ == "__main__":
    run_seed_script()


