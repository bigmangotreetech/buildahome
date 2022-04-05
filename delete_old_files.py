import os


BASE_DIR = '/home/buildahome2016/public_html'
abs_path = os.path.join(BASE_DIR, '/home/buildahome2016/public_html/app.buildahome.in/api/images')
files = os.listdir(abs_path)
try:
    for x in range(0, 100):
        i = files[x]
        print('Deleted file '+str(x))
        os.remove('/home/buildahome2016/public_html/app.buildahome.in/api/images/' + i)
        print(i+ " Deleted")
        print()
except Exception as e:
    print("Something Happened: ", e)
