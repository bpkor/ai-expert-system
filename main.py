import os
import functions_framework
from flask import render_template_string, request
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# HTML 템플릿 (이전과 동일)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI 시인 & 전문가 시스템</title>
    <style>
        body { font-family: 'Malgun Gothic', sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .input-section { margin: 20px 0; }
        .result-section { margin: 20px 0; white-space: pre-line; }
        textarea { width: 100%; padding: 10px; }
        button { padding: 10px 20px; background-color: #4285f4; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <h1>AI 시인</h1>
    <div class="input-section">
        <form method="POST">
            <textarea name="topic" rows="3" placeholder="시의 주제를 입력하세요...">{{topic}}</textarea>
            <button type="submit">시 생성하기</button>
        </form>
    </div>
    {% if poem %}
    <div class="result-section">
        {{poem}}
    </div>
    {% endif %}
</body>
</html>
"""

# 프롬프트 템플릿
PROMPT_TEMPLATE = """
다음 주제로 아름다운 한국어 시를 써주세요.
주제: {topic}

규칙:
1. 현대적인 감성을 담을 것
2. 3~4연으로 구성할 것
3. 깊이 있는 은유와 상징을 사용할 것
4. 마지막 연에서 의미있는 마무리를 할 것
5. 각 연 사이에는 빈 줄을 넣을 것
"""

import os
from functions_framework import http

@http
def hello_http(request):
    # 나머지 코드는 그대로
    # 기본값 설정
    topic = request.form.get('topic', '') if request.method == 'POST' else ''
    poem = ""
    
    if topic:
        try:
            # OpenAI 초기화
            chat_model = ChatOpenAI(
                temperature=0.7,
                api_key=os.getenv('OPENAI_API_KEY')
            )
            
            # 프롬프트 설정
            prompt = PromptTemplate(
                input_variables=["topic"],
                template=PROMPT_TEMPLATE
            )
            
            # 체인 생성 및 실행
            chain = LLMChain(llm=chat_model, prompt=prompt)
            result = chain.invoke({"topic": topic})
            poem = result['text']
            
        except Exception as e:
            poem = f"시 생성 중 오류가 발생했습니다: {str(e)}"
    
    # 템플릿 렌더링
    return render_template_string(HTML_TEMPLATE, topic=topic, poem=poem)
