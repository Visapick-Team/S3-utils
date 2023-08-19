import base64

def convert_base64_to_bytes(data: str) -> bytes:
    # Remember to remove data header if data comes from browser.
    try:
        data = data[5:]
        header, data = data.split(",")
        file_type, encode = header.split(";")
        print(f"{header=} {file_type=} {encode=}")
        img_data = data.encode()
        return base64.b64decode(img_data)
    except Exception as e:
        raise ValueError(f"Invalid base64 format. {e}, {data}")
