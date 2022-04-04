from werkzeug.datastructures import FileStorage
import os
import boto3
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ.get('S3_KEY'),
    aws_secret_access_key=os.environ.get('S3_SECRET')
)
print(s3)

def send_to_s3(file, bucket_name, filename, acl="public-read"):
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type  # Set appropriate content type as per the file
            }
        )
    except Exception as e:
        print("Something Happened: ", e)
        return str(e)
    return 'success'

BASE_DIR = '/home/buildahome2016/public_html'
abs_path = os.path.join(BASE_DIR, '/home/buildahome2016/public_html/app.buildahome.in/api/images')
files = os.listdir(abs_path)
try:
    for x in range(100, 500):
        i = files[x]
        print('Uploading file '+str(x))
        with open(
                '/home/buildahome2016/public_html/app.buildahome.in/api/images/' + i,
                'rb') as fp:
            file = FileStorage(fp, content_type='image/' + i.split('.')[-1])
            send_to_s3(file, os.environ.get('S3_BUCKET'), 'migrated/'+i)
        print('Uploaded '+i)
        print()
except Exception as e:
    print("Something Happened: ", e)
