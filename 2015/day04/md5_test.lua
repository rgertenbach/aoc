local md5 = require "md6"

print(md5.sumhexa("abc")  == "900150983cd24fb0d6963f7d28e17f72")
print(md5.sumhexa("def")  == "4ed9407630eb1000c0f6b63842defa7d")
print(md5.sumhexa("def1") == "4c0844ca6271ec6bf35b9399726eb195")
print(md5.sumhexa("def2") == "9f480132cb9b80a5de20bfec0c1cde96")






