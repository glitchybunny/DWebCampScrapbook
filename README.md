Simple webapp to upload images to archive.org when internet is available, initially made for [dwebcamp 2019](https://dwebcamp.org/)!

## How to set up the web app
1. Make sure you're running python 3.7 or something around that, and you install all the packages as found in requirements.txt
2. ~~You'll need to generate some API keys for IAS3, which can be done here: [https://archive.org/account/s3.php](https://archive.org/account/s3.php)~~
3. You'll also need to generate a secret key for flask. Some simple instructions for generating such keys can found here: [https://stackoverflow.com/a/34903502](https://stackoverflow.com/a/34903502)
4. Create some environment variables with the respective API keys, name them ~~IAS3_ACCESS_KEY, IAS3_SECRET_KEY and~~ FLASK_SECRET_KEY 
5. Once all that is done, it should be as simple as running **app.py**

By default the flask server runs on 10.8.8.8:88 (because that was the app setup for dweb2019), but that can be changed. 

If you want different settings on different devices, having an environment var like DEBUG=true is useful.
