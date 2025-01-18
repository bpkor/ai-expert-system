import os
import functions_framework
from flask import render_template_string, request
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# HTML 템플릿은 그대로...

@functions_framework.http
def hello_http(request):
    if request.method == "GET":
        return render_template_string(HTML_TEMPLATE, topic="", poem="")
    
    if request.method == "POST":
        topic = request.form.get("topic", "")
        if not topic:
            return render_template_string(HTML_TEMPLATE, topic="", poem="")
        
        try:
            chat_model = ChatOpenAI(
                temperature=0.7,
                api_key=os.getenv("OPENAI_API_KEY")
            )
            
            prompt = PromptTemplate(
                input_variables=["topic"],
                template=PROMPT_TEMPLATE
            )
            
            chain = LLMChain(llm=chat_model, prompt=prompt)
            result = chain.invoke({"topic": topic})
            poem = result["text"]
            
        except Exception as e:
            poem = f"시 생성 중 오류가 발생했습니다: {str(e)}"
        
        return render_template_string(HTML_TEMPLATE, topic=topic, poem=poem)
