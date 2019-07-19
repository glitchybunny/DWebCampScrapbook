Simple webapp to upload images to archive.org when internet is available, initially made for [dwebcamp 2019](https://dwebcamp.org/)!

# How to set up the local webapp
1. You'll need to generate some API keys for IAS3, which can be done here: [https://archive.org/account/s3.php](https://archive.org/account/s3.php)
2. You'll also need to generate a secret key for flask. Some simple instructions can found here: [https://stackoverflow.com/a/34903502](https://stackoverflow.com/a/34903502)
3. Create some environment variables with the respective API keys, name them IAS3_ACCESS_KEY, IAS3_SECRET_KEY and FLASK_SECRET_KEY.
4. Once all that is done, it should be as simple as running **app.py**.

By default the app runs on localhost:80/media, but all these things can be easily configured in the code.