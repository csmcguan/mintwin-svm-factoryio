from sklearn.svm import OneClassSVM
from util.predict import predict
import sys

def main():
    print("[*] Classifier Accuracy for Attacks:")
    count = 0
    for i in range(7):
        log = "./data-capture/log/attack" + str(i) + ".csv"
        pred = predict(log)
        if pred:
            count += 1
        print("  " + log + ": " + str(pred))

    print("  Identified " + str(count) + "/7 attacks")

    print("[*] Classifier Accuracy for Benign Data:")
    count = 0
    for i in range(50):
        log = "./data-capture/log/benign" + str(i) + ".csv"
        pred = predict(log)
        if pred:
            count += 1
        print("  " + log + ": " + str(pred))

    print("  Misclassified " + str(count) + "/50 benign data")
if __name__ == "__main__":
    main()
