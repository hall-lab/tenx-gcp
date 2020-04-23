"""
Assemblies table
"""

from yoyo import step

steps = [
    step(
        "CREATE TABLE IF NOT EXISTS assemblies (id INTEGER PRIMARY KEY, sample_name VARCHAR(64), directory VARCHAR(128), url VARCHAR(128))",
        "DROP TABLE IF EXISTS assemblies",
    )
]
