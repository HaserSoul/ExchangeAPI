import re 
from fastapi import HTTPException, status

async def validate_exchange_input(code_from: str, code_to: str, amount: float) -> None:
    if not amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Input data error"
        )

    try:
        float(amount)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="amount should be a number."
        )

    if not code_from or not code_to:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Input data error"
        )

    pattern = re.compile("^[A-Z]{3}$")

    if not pattern.match(string=code_from) or not pattern.match(string=code_to):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Input data error"
        )

    return code_from.upper(), code_to.upper(), amount
