from sklearn.svm import OneClassSVM
import csv
import joblib
import sys

def main():
    svm = OneClassSVM(kernel="rbf", gamma="scale", nu=0.05)
    with open("./data-capture/log/training-data.csv", "r") as fp:
        data = list(csv.reader(fp))
        svm.fit(data)
        joblib.dump(svm, "./util/svm.dmp")

if __name__ == "__main__":
    main()
