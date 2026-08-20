from openai import OpenAI

from config import (
    FOUNDRY_URL,
    FOUNDRY_API_KEY,
    CHAT_MODEL
)


client = OpenAI(
    base_url=FOUNDRY_URL,
    api_key=FOUNDRY_API_KEY
)


def ask_llm(context, question):

    system_prompt = """
Sen Türkçe çalışan bir soru-cevap asistanısın.

Cevaplama kuralları:

1. Öncelikle verilen PDF metinlerini dikkate al.
2. PDF'de sorunun cevabı varsa PDF'deki bilgiyi esas al.
3. PDF'de açık bir tanım varsa tanımı mümkün olduğunca doğru ve anlaşılır şekilde aktar.
4. PDF'de bilgi yoksa genel bilgini kullanarak soruyu doğru şekilde cevapla.
5. PDF ile genel bilgi arasında çelişki varsa PDF'deki bilgiyi esas al.
6. PDF'de olmayan bilgiyi PDF'den alınmış gibi gösterme.
7. Tahmin veya uydurma bilgi verme.
8. Soruyla ilgisiz bilgileri ekleme.
9. Gereksiz giriş cümleleri kullanma.
10. Cevabı doğrudan sorunun cevabıyla başlat.
11. Cevap mümkün olduğunca kısa ve öz olsun.
12. Basit sorulara 1-2 cümle, açıklama gerektiren sorulara en fazla 4 cümleyle cevap ver.
13. Kullanıcı "nedir?" diye soruyorsa önce doğrudan tanımı ver.
14. Gerekli olduğunda kısa bir örnek verebilirsin.
15. İngilizce ifadeler kullanma; Türkçe karşılığı varsa onu kullan.
16. İnternet sitesi, URL veya kaynak adı ekleme.
17. "PDF'de bulunmuyor" gibi ifadeler kullanma; PDF'de bilgi yoksa genel bilginle cevap ver.
"""

    user_prompt = f"""
Aşağıda PDF belgelerinden alınmış bilgiler bulunmaktadır.

PDF BİLGİLERİ:
----------------
{context}
----------------

SORU:
{question}

Önce PDF bilgilerinde sorunun cevabını ara.

Eğer cevap PDF'de varsa:
- PDF'deki bilgiyi esas al.
- Özellikle tanım varsa doğru ve kısa şekilde aktar.
- Gereksiz ayrıntı ekleme.

Eğer cevap PDF'de yoksa:
- Genel bilgini kullan.
- Soruyu doğru ve anlaşılır şekilde cevapla.

SADECE CEVABI YAZ.
"""

    response = client.chat.completions.create(
        model=CHAT_MODEL,

        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],

        temperature=0.0,
        top_p=0.1,
        max_tokens=150
    )

    return response.choices[0].message.content.strip()