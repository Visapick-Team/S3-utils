# S3-utils
By this library you can upload objects and share temp link of objects easily.

## installation

+ just run ``` pip install git+https://github.com/Visapick-Team/S3-utils```





s3_config.py
```python
from s3_utiles.manage import S3
endpoint = "<endpoint>"
access_key = "<access_key>"
secret_key = "<secret_key>"

s3 = S3(endpoint = endpoint,
    access_key = access_key,
    secret_key = secret_key)
```



uploader.py
```python
from s3_config import s3
filepath: str = "~/Videos/test.mp4
object_id: str = s3.upload(file_path = filepath, object_name = "test_1.mp4")
```