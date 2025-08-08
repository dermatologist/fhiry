"""Example of using LLMs with FHIRy
git clone https://github.com/dermatologist/fhiry.git@develop
cd fhiry
pip install -e .[llm]

You will need to get an API key from Google AI Studio: https://aistudio.google.com/
Once you have one, you can either pass it  to the model.
"""

# Import any LLMs that llama_index supports and you have access to
# Require OpenAI API key to use OpenAI LLMs
from llama_index.llms.google_genai import GoogleGenAI
from fhiry.fhirsearch import Fhirsearch

fs = Fhirsearch(fhir_base_url="https://hapi.fhir.org/baseR4")
df = fs.search(resource_type="Condition", search_parameters={})
# print(df.info())

# Create a Vertex LLM
llm = GoogleGenAI(
    model="gemini-2.0-flash",
    api_key="some-key",  # Replace this with your key
)
query = "How many patients have a disease like rheumatoid arthritis?"
_command = fs.llm_query(query, llm)

print(_command)

print(df["resource.code.text"].str.contains("rheumatoid arthritis").sum())
