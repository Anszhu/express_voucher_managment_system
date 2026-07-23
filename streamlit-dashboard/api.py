import requests
import streamlit as st
from config import EXPRESS_API_URL
from typing import Optional

SESSION = requests.Session()

def _headers() -> dict:
    token = st.session_state.get("access_token")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

def _handle_response(resp: requests.Response):
    if resp.status_code == 401:
        st.session_state.pop("access_token", None)
        st.session_state.pop("refresh_token", None)
        st.session_state.pop("user", None)
        st.error("Session expired. Please log in again.")
        st.rerun()
    return resp

def login(email: str, password: str) -> Optional[dict]:
    try:
        resp = SESSION.post(f"{EXPRESS_API_URL}/auth/login", json={"email": email, "password": password})
        if resp.status_code == 200:
            data = resp.json()
            st.session_state["access_token"] = data["accessToken"]
            st.session_state["refresh_token"] = data["refreshToken"]
            st.session_state["user"] = data["user"]
            return data
        return None
    except requests.ConnectionError:
        st.error("Cannot connect to API server. Is it running?")
        return None

def logout():
    try:
        refresh_token = st.session_state.get("refresh_token")
        if refresh_token:
            SESSION.post(f"{EXPRESS_API_URL}/auth/logout", json={"refreshToken": refresh_token}, headers=_headers())
    except:
        pass
    st.session_state.pop("access_token", None)
    st.session_state.pop("refresh_token", None)
    st.session_state.pop("user", None)

def get_me() -> Optional[dict]:
    try:
        resp = SESSION.get(f"{EXPRESS_API_URL}/auth/me", headers=_headers())
        _handle_response(resp)
        if resp.status_code == 200:
            return resp.json().get("user")
        return None
    except:
        return None

def health_check() -> dict:
    try:
        resp = SESSION.get(f"{EXPRESS_API_URL.rstrip('/api/v1')}/health", timeout=5)
        return resp.json() if resp.status_code == 200 else {"status": "error"}
    except:
        return {"status": "unreachable"}

def list_vouchers(params: Optional[dict] = None) -> dict:
    try:
        resp = SESSION.get(f"{EXPRESS_API_URL}/vouchers", headers=_headers(), params=params or {})
        _handle_response(resp)
        return resp.json() if resp.status_code == 200 else {"items": [], "pagination": {"page": 1, "limit": 20, "total": 0, "pages": 0}}
    except:
        return {"items": [], "pagination": {"page": 1, "limit": 20, "total": 0, "pages": 0}}

def get_voucher(voucher_id: str) -> Optional[dict]:
    try:
        resp = SESSION.get(f"{EXPRESS_API_URL}/vouchers/{voucher_id}", headers=_headers())
        _handle_response(resp)
        return resp.json() if resp.status_code == 200 else None
    except:
        return None

def create_voucher(data: dict) -> Optional[dict]:
    try:
        resp = SESSION.post(f"{EXPRESS_API_URL}/vouchers", headers=_headers(), json=data)
        _handle_response(resp)
        return resp.json() if resp.status_code == 201 else None
    except:
        return None

def update_voucher(voucher_id: str, data: dict) -> Optional[dict]:
    try:
        resp = SESSION.patch(f"{EXPRESS_API_URL}/vouchers/{voucher_id}", headers=_headers(), json=data)
        _handle_response(resp)
        return resp.json() if resp.status_code == 200 else None
    except:
        return None

def delete_voucher(voucher_id: str) -> bool:
    try:
        resp = SESSION.delete(f"{EXPRESS_API_URL}/vouchers/{voucher_id}", headers=_headers())
        _handle_response(resp)
        return resp.status_code == 204
    except:
        return False

def submit_voucher(voucher_id: str) -> Optional[dict]:
    try:
        resp = SESSION.post(f"{EXPRESS_API_URL}/vouchers/{voucher_id}/submit", headers={"Authorization": _headers().get("Authorization", "")})
        _handle_response(resp)
        return resp.json() if resp.status_code == 200 else None
    except:
        return None

def approve_voucher(voucher_id: str) -> Optional[dict]:
    try:
        resp = SESSION.post(f"{EXPRESS_API_URL}/vouchers/{voucher_id}/approve", headers={"Authorization": _headers().get("Authorization", "")})
        _handle_response(resp)
        return resp.json() if resp.status_code == 200 else None
    except:
        return None

def reject_voucher(voucher_id: str, reason: str) -> Optional[dict]:
    try:
        resp = SESSION.post(f"{EXPRESS_API_URL}/vouchers/{voucher_id}/reject", headers=_headers(), json={"reason": reason})
        _handle_response(resp)
        return resp.json() if resp.status_code == 200 else None
    except:
        return None

def dashboard_stats() -> dict:
    try:
        resp = SESSION.get(f"{EXPRESS_API_URL}/vouchers/dashboard", headers=_headers())
        _handle_response(resp)
        return resp.json() if resp.status_code == 200 else {"byStatus": [], "totalApprovedAmount": 0, "recent": []}
    except:
        return {"byStatus": [], "totalApprovedAmount": 0, "recent": []}

def list_users() -> list:
    try:
        resp = SESSION.get(f"{EXPRESS_API_URL}/users", headers=_headers())
        _handle_response(resp)
        data = resp.json() if resp.status_code == 200 else {"users": []}
        return data.get("users", [])
    except:
        return []
