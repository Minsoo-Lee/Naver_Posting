from ai import gemini
from ai.gemini import init_gemini
from data import const

# # gemini.init_gemini()
# response = gemini.create_content([const.CONTENT_EX1, const.CONTENT_EX2])
# print(response)

init_gemini()

title = gemini.create_title(
    titles=[],
    address="송파동",
    company="설비업체",
    place=""
)

print(title)


