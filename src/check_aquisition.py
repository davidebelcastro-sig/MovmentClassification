write = 1
while 1:
    t = input("blocca capture: ")
    if t.startswith("s"):
        fp = open("capture.txt", "w",encoding="utf-8")
        fp.write("0")
        fp.close()
    if t.startswith("n"):
        fp = open("capture.txt", "w",encoding="utf-8")
        fp.write("1")
        fp.close()
    if t.startswith("q"):
        try:
            fp.close()
            break
        except:
            break




