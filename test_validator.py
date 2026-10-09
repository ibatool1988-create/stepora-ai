
from app import validate_stepora_response

wrong_answer = (
"The ASCP MLS exam with a converted passing score of at least 75."
)

result = validate_stepora_response(
    wrong_answer,
    "My highest education is high school."
)

print(result)
