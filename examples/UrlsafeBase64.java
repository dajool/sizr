public static byte[] encodeUrlSafe(byte[] data) {
    byte[] encode = Base64.encode(data);
    for (int i = 0; i < encode.length; i++) {
        if (encode[i] == '+') {
            encode[i] = '-';
        } else if (encode[i] == '/') {
            encode[i] = '_';
        }
    }
    return encode;
}

public static byte[] decodeUrlSafe(byte[] data) {
    byte[] encode = Arrays.copyOf(data, data.length);
    for (int i = 0; i < encode.length; i++) {
        if (encode[i] == '-') {
            encode[i] = '+';
        } else if (encode[i] == '_') {
            encode[i] = '/';
        }
    }
    return Base64.decode(encode);
}
