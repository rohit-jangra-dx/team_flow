import subprocess
import os

api_schema_url = "http://localhost:8000/api/schema/"

output_dir = os.path.join(os.getcwd(), 'src/api')

command = [
    'npx',
    'openapi-typescript-codegen',
    '--input', api_schema_url,
    '--output', output_dir,
    '--client', 'axios'
]

try:
    print("Generating API Client...")
    subprocess.run(command, check=True)
    print(f"API client generated successfully at {output_dir}")
except subprocess.CalledProcessError as e:
    print(f"Error generating API client: {e}")