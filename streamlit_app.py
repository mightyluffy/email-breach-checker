import streamlit as st
import requests
import os
from urllib.parse import quote

redirect_map = {
    "gmail.com": "https://myaccount.google.com/security",
    "outlook.com": "https://account.live.com/password/reset",
    "hotmail.com": "https://account.live.com/password/reset",
    "yahoo.com": "https://login.yahoo.com/account/security",
    "protonmail.com": "https://account.proton.me/security",
    "icloud.com": "https://iforgot.apple.com/password/verify/appleid",
    "live.com": "https://account.live.com/password/reset"
}

def get_reset_url(domain):
    return redirect_map.get(domain, "https://haveibeenpwned.com/")

def check_breach(email, api_key):
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{quote(email)}"
    headers = {
        "hibp-api-key": api_key,
        "User-Agent": "EmailSecurityChecker"
    }
    response = requests.get(url, headers=headers)
    return response.status_code == 200

st.title("🔐 Email Breach Checker (Powered by HIBP)")
st.write("Unesite email adresu i saznajte da li se pojavljuje u poznatim sigurnosnim incidentima.")

email = st.text_input("Email adresa:")
api_key = os.getenv("HIBP_API_KEY")

if not api_key:
    st.warning("⚠️ API ključ nije postavljen. Postavite HIBP_API_KEY kao varijablu okruženja.")
elif email:
    email_domain = email.split("@")[-1]
    try:
        if check_breach(email, api_key):
            st.error(f"⚠️ Email {email} je kompromitovan.")
            st.markdown(f"🔁 [Kliknite da resetujete lozinku za {email_domain}]({get_reset_url(email_domain)})")
        else:
            st.success(f"✅ Email {email} nije pronađen u poznatim curenjima.")
    except Exception as e:
        st.error(f"Greška prilikom provjere: {e}")
