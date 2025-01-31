import requests


def check_user_existence(jshshir, phone):
    url = f"https://dev-gateway.railwayinfra.uz/api/user/jshshir/{jshshir}?project=railmap"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("phone") == phone:
            return "Foydalanuvchi mavjud"
        else:
            return "Foydalanuvchi topildi, lekin telefon raqami mos kelmadi"
    elif response.status_code == 404:
        return "Foydalanuvchi topilmadi"
    else:
        return f"Xatolik: {response.status_code}"


jshshir = "31605942600028"
phone = "(93)-908-12-17"
result = check_user_existence(jshshir, phone)
print(result)
