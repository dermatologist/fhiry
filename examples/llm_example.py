"""Example of using LLMs with FHIRy
git clone https://github.com/dermatologist/fhiry.git@develop
cd fhiry
pip install -e .[llm]
"""
# Import any LLMs that llama_index supports and you have access to
# Require OpenAI API key to use OpenAI LLMs
from llama_index.llms import Vertex
from fhiry.fhirsearch import Fhirsearch

fs = Fhirsearch(fhir_base_url = "https://hapi.fhir.org/baseR4/")
df = fs.search(resource_type = "Condition", search_parameters = {})
# print(df.info())

# Create a Vertex LLM
llm = Vertex(
    model="chat-bison"
)
query = "How many patients have a disease like rheumatoid arthritis?"
_command = fs.llm_query(query, llm)

print(_command)

print(df["resource.code.text"].str.contains("rheumatoid arthritis").sum())

