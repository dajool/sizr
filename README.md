# sizr - Fast scaling of images for web and mobile with caching

sizr is a django app that can resize images on the fly with just a GET request. sizr then fetches the image, resizes it caches the image in a "bucket" and redirects you to the local copy. The next request then gets redirected directly.

At the moment sizr has the status "prove of concept", so don't expect it to work with every image format or think of it as unbreakable.

# Dependencies

* Django 1.4.10
* Grapelli 2.4.8
* Python Requests (>= 0.8.2-1 | shipped with Ubuntu 12.04)


# Some notes on base64

sizr uses base64 to encode URLs. But it has to be URL-safe, which standard base64 isn't.

iOS: http://stackoverflow.com/questions/11106393/url-safe-base64-in-objective-c
Java: http://commons.apache.org/proper/commons-codec/apidocs/org/apache/commons/codec/binary/Base64.html#Base64%28boolean%29
Perl: http://search.cpan.org/~kazuho/MIME-Base64-URLSafe-0.01/lib/MIME/Base64/URLSafe.pm
