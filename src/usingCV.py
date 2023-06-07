import cv2
import string
n=0
aux=2
img1 = cv2.imread("./resources/images/image1.jpg")
img2 = cv2.imread("./resources/images/image2.jpg")
while True:
    if(n==1):
        aux=aux+1
        if(aux==6):
            aux=1
        img1 = img2
        i2="./resources/images/image"+str(aux)+".jpg"
        img2 = cv2.imread(i2)
        n=0
    n=round(n+0.05,2)
    dst = cv2.addWeighted(img1,1-n,img2,0+n,0)
    cv2.imshow("dst",dst)
    if cv2.waitKey(100) & 0xFF == ord('m'):
        print("m has been pressed")
        break

cv2.destroyAllWindows()