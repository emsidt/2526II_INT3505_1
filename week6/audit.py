from pathlib import Path

def audit_file(filename):
    content = Path(filename).read_text(encoding="utf-8")

    print("=== SECURITY AUDIT ===")

    if "localStorage" in content:
        print("- Cảnh báo: Có dùng localStorage -> dễ lộ token do XSS")

    if "console.log(token)" in content or "print(token)" in content:
        print("- Cảnh báo: Có log token ra màn hình")

    if "token=" in content or "access_token=" in content:
        print("- Cảnh báo: Có truyền token qua URL")

    if "httpOnly: true" in content:
        print("- Tốt: Cookie có httpOnly")

    if "sameSite:" in content:
        print("- Tốt: Cookie có sameSite")

    if "expiresIn" in content:
        print("- Tốt: Token có thời gian hết hạn")

    print("=== KẾT THÚC ===")

audit_file("server_secure.js")