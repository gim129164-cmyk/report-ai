import streamlit as st
from openai import OpenAI


# ============================================================
# 기본 설정
# ============================================================

st.set_page_config(
    page_title="Report AI",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Report AI")
st.write("나의 보고서를 분석하고 탐구와 면접을 준비하는 AI")


# ============================================================
# API 연결
# ============================================================

try:
    UPSTAGE_API_KEY = up_Y7OKHBUB2q7pi7C4E1ILIWItBAUOG

    client = OpenAI(
        api_key=UPSTAGE_API_KEY,
        base_url="https://api.upstage.ai/v1"
    )

except Exception:
    client = None


# ============================================================
# AI 함수
# ============================================================

def ask_ai(prompt):

    if client is None:
        return (
            "⚠️ API 키가 설정되지 않았습니다.\n\n"
            "Streamlit Cloud의 Secrets에 "
            "`UPSTAGE_API_KEY`를 설정해주세요."
        )

    try:

        response = client.chat.completions.create(
            model="solar-pro3",
            messages=[
                {
                    "role": "system",
                    "content": """
너는 학생의 탐구 보고서를 분석하고
대학 입학 면접을 준비하도록 돕는 AI이다.

반드시 학생이 입력한 보고서와
실제 면접 대화 내용을 근거로 답변한다.

보고서에 없는 활동이나 실험을
학생이 실제로 했다고 가정하지 않는다.

학생이 실제로 말하지 않은 내용을
학생의 답변에 포함시키지 않는다.

면접관의 발언과 학생의 발언을
절대로 혼동하지 않는다.

AI가 이전에 설명한 내용을
학생이 알고 있다고 판단하지 않는다.

학생의 답변이 부족하면 부족하다고
명확하게 평가한다.

모든 답변은 한국어로 작성한다.

영어 전문용어가 필요한 경우에는
한국어 설명을 먼저 작성하고
괄호 안에 영어 용어를 표시한다.
"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"""
⚠️ AI 요청 중 오류가 발생했습니다.

오류 내용:
{str(e)}
"""


# ============================================================
# 세션 상태 초기화
# ============================================================

if "report_title" not in st.session_state:
    st.session_state["report_title"] = ""

if "report_content" not in st.session_state:
    st.session_state["report_content"] = ""

if "interview_messages" not in st.session_state:
    st.session_state["interview_messages"] = []

if "interview_started" not in st.session_state:
    st.session_state["interview_started"] = False

if "interview_finished" not in st.session_state:
    st.session_state["interview_finished"] = False

if "interview_evaluation" not in st.session_state:
    st.session_state["interview_evaluation"] = ""


# ============================================================
# 사이드바
# ============================================================

st.sidebar.title("📚 Report AI")

st.sidebar.write("### 📄 보고서 입력")

report_title = st.sidebar.text_input(
    "보고서 제목",
    value=st.session_state["report_title"],
    placeholder="예: 스마트폰 사용이 학생들의 수면에 미치는 영향"
)

report_content = st.sidebar.text_area(
    "보고서 내용을 입력하세요.",
    value=st.session_state["report_content"],
    height=400,
    placeholder="보고서 내용을 여기에 붙여넣으세요."
)


# ============================================================
# 보고서 저장
# ============================================================

if st.sidebar.button(
    "📥 보고서 적용",
    use_container_width=True
):

    if report_title.strip() == "":
        st.sidebar.warning("보고서 제목을 입력해주세요.")

    elif report_content.strip() == "":
        st.sidebar.warning("보고서 내용을 입력해주세요.")

    else:

        st.session_state["report_title"] = report_title
        st.session_state["report_content"] = report_content

        # 기존 면접 내용 초기화
        st.session_state["interview_messages"] = []
        st.session_state["interview_started"] = False
        st.session_state["interview_finished"] = False
        st.session_state["interview_evaluation"] = ""

        st.sidebar.success("보고서가 적용되었습니다.")

        st.rerun()


# ============================================================
# 현재 보고서 가져오기
# ============================================================

current_title = st.session_state["report_title"]
current_report = st.session_state["report_content"]


# ============================================================
# 보고서가 없는 경우
# ============================================================

if current_report.strip() == "":

    st.info(
        "👈 왼쪽 사이드바에 보고서 제목과 내용을 입력한 후 "
        "'📥 보고서 적용' 버튼을 눌러주세요."
    )

    st.markdown(
        """
### 사용 방법

**1. 보고서 제목 입력**

예:
> 예쁜꼬마선충의 신경망 재현을 통한 뉴로모픽 반도체 기술 탐구

**2. 보고서 내용 입력**

생기부나 탐구보고서의 내용을 그대로 붙여넣으면 됩니다.

**3. 보고서 적용**

왼쪽의 `📥 보고서 적용` 버튼을 누릅니다.

**4. AI 기능 사용**

- 📝 보고서 요약
- 💡 후속 탐구
- 🎤 AI 모의면접

을 사용할 수 있습니다.
"""
    )

    st.stop()


# ============================================================
# 메인 화면
# ============================================================

st.header(current_title)

st.caption("현재 입력된 보고서를 기반으로 AI가 분석합니다.")


# ============================================================
# 탭
# ============================================================

tab1, tab2, tab3 = st.tabs(
    [
        "📝 보고서 분석",
        "💡 후속 탐구",
        "🎤 모의면접"
    ]
)


# ============================================================
# TAB 1
# 보고서 분석
# ============================================================

with tab1:

    st.subheader("📄 입력한 보고서")

    with st.expander(
        "보고서 원문 보기",
        expanded=False
    ):

        st.markdown(current_report)

    st.divider()

    st.subheader("🤖 AI 보고서 분석")

    if st.button(
        "보고서 핵심 내용 분석",
        key="analyze_report"
    ):

        prompt = f"""
다음은 학생이 직접 입력한 탐구 보고서이다.

[보고서 제목]
{current_title}

[보고서 내용]
{current_report}

이 보고서를 바탕으로 다음 내용을 분석해줘.

1. 탐구 주제
2. 탐구 동기
3. 핵심 개념
4. 탐구 과정
5. 탐구를 통해 알게 된 점
6. 보고서에서 드러나는 학생의 관심 분야
7. 대학 면접에서 질문할 가능성이 높은 부분

반드시 보고서에 실제로 적혀 있는 내용만 근거로 작성해라.

보고서에 없는 활동이나 실험을
학생이 수행했다고 가정하지 마라.

한국어로 작성해라.
"""

        with st.spinner(
            "보고서를 분석하고 있습니다..."
        ):

            result = ask_ai(prompt)

        st.markdown(result)


# ============================================================
# TAB 2
# 후속 탐구
# ============================================================

with tab2:

    st.subheader("💡 후속 탐구 주제 추천")

    st.write(
        "현재 보고서에서 자연스럽게 확장할 수 있는 "
        "탐구 주제를 추천합니다."
    )

    if st.button(
        "💡 후속 탐구 주제 추천",
        key="recommend_topics"
    ):

        prompt = f"""
다음은 학생이 직접 작성한 탐구 보고서이다.

[보고서 제목]
{current_title}

[보고서 내용]
{current_report}

이 보고서에서 자연스럽게 발전시킬 수 있는
후속 탐구 주제를 5개 추천해줘.

각 주제마다 다음 내용을 작성해줘.

1. 후속 탐구 주제
2. 기존 보고서와의 연결점
3. 탐구 가치
4. 예상되는 탐구 방법
5. 기존 탐구보다 발전된 점

중요한 조건:

- 기존 보고서와 관련성이 높아야 한다.
- 완전히 다른 분야의 주제를 추천하지 않는다.
- 학생이 이미 수행했다고 표현하지 않는다.
- 실제로 추가 탐구할 수 있는 수준의 주제를 추천한다.
- 대학 입시 생기부와 연결하기 좋은 심화 탐구가 되도록 한다.

한국어로 작성해라.
"""

        with st.spinner(
            "후속 탐구 주제를 생성하고 있습니다..."
        ):

            result = ask_ai(prompt)

        st.markdown(result)


# ============================================================
# TAB 3
# 모의면접
# ============================================================

with tab3:

    st.subheader("🎤 AI 모의면접")

    st.write(
        "실제 대학 면접처럼 AI 면접관이 질문을 하나씩 제시합니다."
    )

    # --------------------------------------------------------
    # 면접 시작 전
    # --------------------------------------------------------

    if not st.session_state["interview_started"]:

        st.info(
            "보고서를 바탕으로 대학 면접관이 질문을 하나씩 제시합니다."
        )

        if st.button(
            "🎤 모의면접 시작",
            key="start_interview"
        ):

            prompt = f"""
너는 대학 입학 면접관이다.

다음 학생의 탐구 보고서를 바탕으로
첫 번째 면접 질문을 하나 만들어라.

[보고서 제목]
{current_title}

[보고서 내용]
{current_report}

질문은 탐구 동기나
주제 선정 이유를 묻는 질문으로 시작해라.

반드시 질문 하나만 출력한다.

다음 내용을 출력하지 않는다.

- 질문에 대한 설명
- 질문을 만든 이유
- 보고서 분석
- 학생 답변
- 평가
- 피드백
- "다음 질문입니다" 등의 안내 문구

반드시 한국어로 작성한다.
"""

            with st.spinner(
                "면접관이 첫 질문을 준비하고 있습니다..."
            ):

                first_question = ask_ai(prompt)

            st.session_state["interview_messages"] = [
                {
                    "role": "assistant",
                    "content": first_question
                }
            ]

            st.session_state["interview_started"] = True
            st.session_state["interview_finished"] = False
            st.session_state["interview_evaluation"] = ""

            st.rerun()


    # --------------------------------------------------------
    # 면접 진행
    # --------------------------------------------------------

    if st.session_state["interview_started"]:

        st.divider()

        # ----------------------------------------------------
        # 기존 대화 출력
        # ----------------------------------------------------

        for message in st.session_state["interview_messages"]:

            if message["role"] == "assistant":

                st.markdown("### 🧑‍💼 면접관")
                st.markdown(message["content"])

            elif message["role"] == "user":

                st.markdown("### 👤 학생")
                st.markdown(message["content"])


        # ----------------------------------------------------
        # 면접 진행 중
        # ----------------------------------------------------

        if not st.session_state["interview_finished"]:

            st.divider()

            # 질문 번호
            question_number = 0

            for message in st.session_state["interview_messages"]:

                if message["role"] == "assistant":
                    question_number += 1

            answer_key = f"answer_{question_number}"

            answer = st.text_area(
                "👤 답변을 입력하세요.",
                height=180,
                placeholder="면접관의 질문에 답변해보세요.",
                key=answer_key
            )

            col1, col2 = st.columns(2)

            # ------------------------------------------------
            # 답변 제출
            # ------------------------------------------------

            with col1:

                submit_button = st.button(
                    "📤 답변 제출",
                    key=f"submit_{question_number}",
                    use_container_width=True
                )

            # ------------------------------------------------
            # 면접 종료
            # ------------------------------------------------

            with col2:

                finish_button = st.button(
                    "🛑 면접 종료",
                    key=f"finish_{question_number}",
                    use_container_width=True
                )

            # ------------------------------------------------
            # 면접 종료 처리
            # ------------------------------------------------

            if finish_button:

                st.session_state["interview_finished"] = True

                st.rerun()


            # ------------------------------------------------
            # 답변 제출 처리
            # ------------------------------------------------

            if submit_button:

                if answer.strip() == "":

                    st.warning(
                        "답변을 입력해주세요."
                    )

                else:

                    # ----------------------------------------
                    # 학생 답변 저장
                    # ----------------------------------------

                    st.session_state[
                        "interview_messages"
                    ].append(
                        {
                            "role": "user",
                            "content": answer
                        }
                    )


                    # ----------------------------------------
                    # 전체 대화 만들기
                    # ----------------------------------------

                    conversation = ""

                    for message in st.session_state[
                        "interview_messages"
                    ]:

                        if message["role"] == "assistant":

                            conversation += (
                                "면접관: "
                                + message["content"]
                                + "\n"
                            )

                        elif message["role"] == "user":

                            conversation += (
                                "학생: "
                                + message["content"]
                                + "\n"
                            )


                    # ----------------------------------------
                    # 다음 질문 생성
                    # ----------------------------------------

                    prompt = f"""
너는 대학 입학 면접관이다.

학생의 탐구 보고서와
지금까지 실제로 진행된 면접 대화를 바탕으로
다음 면접 질문을 하나 만들어라.

[보고서 제목]
{current_title}

[보고서 내용]
{current_report}

[실제 면접 대화]
{conversation}

중요한 원칙:

1. 직전 학생 답변과 자연스럽게 연결한다.

2. 학생의 답변이 부족했다면
   그 부분을 확인하는 꼬리질문을 할 수 있다.

3. 보고서에 실제로 포함된 내용을 중심으로 질문한다.

4. 보고서에 없는 활동을
   학생이 했다고 가정하지 않는다.

5. 이미 물어본 질문을 그대로 반복하지 않는다.

6. 면접이 진행될수록 조금씩 심화한다.

7. 학생이 실제로 답변한 내용과
   보고서 내용을 절대로 혼동하지 않는다.

8. 면접관이 설명한 내용을
   학생이 알고 있다고 가정하지 않는다.

반드시 질문 하나만 출력한다.

다음 내용을 절대로 출력하지 않는다.

- 학생 답변 평가
- 학생 답변 분석
- 질문을 만든 이유
- 질문의 의도
- 보고서 분석
- 면접관의 생각
- 피드백
- 마크다운 제목
- "다음 질문입니다" 등의 안내 문구

한국어로 작성한다.
"""

                    with st.spinner(
                        "면접관이 다음 질문을 생각하고 있습니다..."
                    ):

                        next_question = ask_ai(prompt)


                    # ----------------------------------------
                    # 다음 질문 저장
                    # ----------------------------------------

                    st.session_state[
                        "interview_messages"
                    ].append(
                        {
                            "role": "assistant",
                            "content": next_question
                        }
                    )

                    st.rerun()


    # ========================================================
    # 면접 총평
    # ========================================================

    if st.session_state["interview_finished"]:

        st.divider()

        st.markdown("## 📊 모의면접 총평")

        # ----------------------------------------------------
        # 실제 대화 만들기
        # ----------------------------------------------------

        conversation = ""

        for message in st.session_state["interview_messages"]:

            if message["role"] == "assistant":

                conversation += (
                    "면접관: "
                    + message["content"]
                    + "\n"
                )

            elif message["role"] == "user":

                conversation += (
                    "학생: "
                    + message["content"]
                    + "\n"
                )


        # ----------------------------------------------------
        # 평가가 아직 없으면 생성
        # ----------------------------------------------------

        if st.session_state["interview_evaluation"] == "":

            prompt = f"""
너는 대학 입학 면접관이다.

학생의 모의면접 전체 대화를
매우 엄격하게 평가해야 한다.

[보고서 제목]
{current_title}

[보고서]
{current_report}

[전체 실제 면접 대화]
{conversation}

가장 중요한 평가 원칙:

학생이 실제로 말한 답변만 평가한다.

보고서에 적혀 있다는 이유만으로
학생이 그 내용을 알고 있다고 판단하지 않는다.

면접관이 말한 내용은
학생의 지식으로 인정하지 않는다.

AI가 이전에 설명한 내용도
학생의 지식으로 인정하지 않는다.

학생이 실제 답변에서 해당 개념을 설명했다면
그때만 지식과 이해도를 인정한다.

특히 학생이

"기억이 안 납니다."
"모르겠습니다."
"잘 모르겠습니다."
"생각이 안 납니다."

등으로 답했다면,

그 질문에 대해서는
지식이나 이해도를 보여주지 못한 것으로 평가한다.

이 경우 보고서에 관련 내용이 있더라도
그 내용을 학생의 답변에 대신 넣어서
점수를 올리지 않는다.

점수는 엄격하게 부여한다.

점수 기준:

95~100점
거의 완벽한 답변

90~94점
매우 좋은 답변

80~89점
좋은 답변

70~79점
보통 이상의 답변

60~69점
부분적으로 답변함

50~59점
부족한 답변

30~49점
매우 부족한 답변

10~29점
거의 답변하지 못함

0~9점
질문과 전혀 관련 없는 답변

중요:

학생이 한두 개의 핵심 질문에
"기억이 안 납니다."라고 답했다면
보고서에 좋은 내용이 많이 있어도
면접 점수를 높게 주지 않는다.

학생이 실제로 말한 내용에서
확인되는 강점만 인정한다.

학생 답변에 강점이 없다면
억지로 장점을 만들어내지 않는다.

반드시 아래 형식으로 출력한다.

## 📊 총점

점수: ○○점 / 100점

## 👍 잘한 점

학생이 실제로 말한 답변에서
확인되는 강점만 작성한다.

## ⚠️ 부족한 점

학생의 실제 답변을 기준으로
구체적으로 지적한다.

특히 답변하지 못한 질문이 있다면
어떤 질문에서 무엇을 답하지 못했는지 설명한다.

## 💡 개선 방법

실제 면접에서 더 좋은 답변을 하기 위해
어떤 내용을 추가하고
어떻게 설명해야 하는지 작성한다.

단, 학생이 실제로 수행하지 않은 활동을
했다고 가정하지 않는다.

## 🎯 종합 평가

대학 면접관의 입장에서
학생의 실제 면접 대응력을 평가한다.

보고서의 수준이 아니라
학생이 실제 면접에서 보여준 답변을 기준으로 평가한다.

평가 과정이나 분석 과정을
별도로 설명하지 않는다.

한국어로 작성한다.
"""

            with st.spinner(
                "면접 내용을 매우 엄격하게 평가하고 있습니다..."
            ):

                evaluation = ask_ai(prompt)

            st.session_state[
                "interview_evaluation"
            ] = evaluation


        # ----------------------------------------------------
        # 평가 출력
        # ----------------------------------------------------

        st.markdown(
            st.session_state["interview_evaluation"]
        )


        # ----------------------------------------------------
        # 새로운 면접
        # ----------------------------------------------------

        st.divider()

        if st.button(
            "🔄 새로운 모의면접 시작",
            key="restart_interview",
            use_container_width=True
        ):

            st.session_state["interview_messages"] = []
            st.session_state["interview_started"] = False
            st.session_state["interview_finished"] = False
            st.session_state["interview_evaluation"] = ""

            st.rerun()


# ============================================================
# 하단
# ============================================================

st.divider()

st.caption(
    "Report AI | LLM 기반 개인 보고서 분석 및 면접 지원 시스템"
)
