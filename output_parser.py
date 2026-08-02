from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

class AnalisisTexto(BaseModel):
    texto: str = Field(description="Texto a analizar")
    sentimiento: str = Field(description="Sentimiento del texto (positivo, negativo o neutral)")

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5)

structured_llm = llm.with_structured_output(AnalisisTexto)
texto_prueba = "El producto es excelente, pero el servicio al cliente podría mejorar."
resultado = structured_llm.invoke(texto_prueba)

print(resultado)
