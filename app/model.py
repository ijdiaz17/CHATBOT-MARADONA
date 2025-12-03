import os
from dotenv import load_dotenv
from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions

# 1. Configuración Inicial
load_dotenv()

# Configurar clientes
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
chroma_client = chromadb.PersistentClient(path="./data/chroma_db")

# Función de embedding
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-small"
)

# Obtener colección existente
collection = chroma_client.get_or_create_collection(
    name="maradona_diegodijo",
    embedding_function=openai_ef
)

# 2. Funciones del Chatbot
def buscar_frase(consulta, top_k=5):
    """Busca las frases más relevantes en la base de datos vectorial."""
    results = collection.query(
        query_texts=[consulta],
        n_results=top_k
    )
    if results.get('documents') and results['documents'][0]:
        return results['documents'][0]
    return []

def generar_respuesta(consulta, historial=[]):
    """Genera una respuesta estilo Maradona usando RAG y memoria a corto plazo."""
    # Recuperar contexto (RAG)
    frases_contexto = buscar_frase(consulta, top_k=5)
    
    contexto_str = ""
    if frases_contexto:
        contexto_str = "\n".join(frases_contexto)
    
    # Formatear historial de conversación
    historial_str = ""
    if historial:
        # El historial viene del más reciente al más antiguo, así que lo invertimos
        for interaccion in reversed(historial):
            historial_str += f"Usuario: {interaccion.input_text}\nDiego: {interaccion.prediction}\n"

    # Prompt del Sistema
    system_prompt = """
    Eres Diego Armando Maradona. 
    Tu personalidad es apasionada, desafiante, emotiva y usas lunfardo argentino (palabras como 'fiera', 'maestro', 'papá', 'mostro').
    
    INSTRUCCIONES:
    1. Responde a la pregunta del usuario basándote en el CONTEXTO (tus frases) y el HISTORIAL de la charla.
    2. Si el contexto no tiene la respuesta exacta, improvisa manteniendo tu estilo.
    3. Sé conciso pero contundente. Cuando te pregunten cosas sobre tu vida personal, responde con tus y ahí sí puedes explayarte un poco. PEro si te preguntan sobre otras cosas, intenta ser más contundente, hay frases históricas sobre personajes históricos que son increíbles y que queda bien que respondas de manera más concreta.
    4. Nunca digas 'según el contexto' o 'en el texto dice'. Habla como si fueran tus recuerdos.
    5. Debes hablar SIEMPRE en argentino, con VOS y lunfardo argentino pero no abuses, no uses 'fiera' o 'papá' en todas las frases.
    6. IMPORTANTE: NUNCA empieces tu respuesta con "Diego:" o "Maradona:". Responde directamente.
    """
    
    user_message = f"""
    Contexto (Frases Célebres):
    {contexto_str}

    Historial de Conversación Reciente:
    {historial_str}

    Usuario: {consulta}
    """

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7
    )
    
    return response.choices[0].message.content
