import re
from datetime import date
from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel, Field, EmailStr, validator, root_validator


CODES_MOBILE_UA = ['067', '096', '097', '098',
                   '050', '066', '095', '099',
                   '063', '073', '093',
                   '070', '080', '090', '056', '057',
                   '091', '092', '094']


def phone_normalize(value: str) -> str:
    """
    The phone_normalize function takes a phone number as a string and returns it in the format +380XXXXXXXXX.

    :param value: str: Specify the type of the value parameter
    :return: A string
    """
    clean_phone = (
        value.strip()
        .removeprefix("+")
        .replace("(", "")
        .replace(")", "")
        .replace("-", "")
        .replace(" ", "")
    )

    codes = '|'.join(CODES_MOBILE_UA)
    pattern = r"(?:38|8)?(?:" + codes + r")\d{7}"
    phone = re.search(pattern, clean_phone)

    if not phone:
        raise ValueError(f"Phone number \"{clean_phone}\" is not valid")

    phone = phone.group()

    if phone.startswith('8'):
        return '3' + phone
    elif phone.startswith('0'):
        return '38' + phone

    return phone


class ContactModel(BaseModel):
    first_name: str = Field(default=..., min_length=3, max_length=100, example="Stepan")
    last_name: str = Field(default=..., min_length=3, max_length=100, example="Bogdaniv")
    email: EmailStr
    phone_number: str = Field(default=..., example="380973458623")
    birth_date: date
    additional_data: Optional[str] = Field(default=None, example="Additional information about the client (optional)")

    _normalize_phone_number = validator('phone_number', pre=True, allow_reuse=True)(phone_normalize)


class ContactUpdateModel(ContactModel):
    pass


class ContactPartialUpdateModel(BaseModel):
    first_name: Optional[str] = Field(min_length=3, max_length=100, example="Stepan")
    last_name: Optional[str] = Field(min_length=3, max_length=100, example="Bogdaniv")
    email: Optional[EmailStr]
    phone_number: Optional[str] = Field(example="380973458623")
    birth_date: Optional[date]
    additional_data: Optional[str] = Field(example="Additional information about the client (optional)")

    @root_validator(pre=True)
    def check_values_is_not_none(cls, values):
        if not values:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
            # raise ValueError("At least one body field must be present!")
        return values

    _normalize_phone_number = validator('phone_number', pre=True, allow_reuse=True)(phone_normalize)


class ContactResponse(BaseModel):
    id: int = 1
    first_name: str = Field(default=..., min_length=3, max_length=100, example="Stepan")
    last_name: str = Field(default=..., min_length=3, max_length=100, example="Bogdaniv")
    email: EmailStr
    phone_number: str = Field(default=..., example="380973458623")
    birth_date: date
    additional_data: Optional[str] = Field(example="Additional information about the client (optional)")

    class Config:
        orm_mode = True
