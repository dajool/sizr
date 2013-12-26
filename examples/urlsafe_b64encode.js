function urlsafe_b64encode(url){
    var b64url = btoa(url);
    return b64url.replace(/\+/g, '-').replace(/\//g, '_');
}
