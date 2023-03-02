from sklearn.svm import OneClassSVM
import joblib
import csv
import sys

def init_win(data, size):
    return data[0:size - 1]

def predict(file):
    WIN_SIZE = 150

    with open(file, "r") as fp:
        data = list(csv.reader(fp))
        win = []
        svm = joblib.load("./util/svm.dmp")

        win = init_win(data, WIN_SIZE)

        index = WIN_SIZE
        while index < len(data):
            win.append(data[index])

            if len(win) == WIN_SIZE:
                count = 0
                pred = svm.predict(win)
                for i in range(WIN_SIZE):
                    if pred[i] == -1:
                        count += 1
                if count / WIN_SIZE >= 0.6:
                    return True

            index += 1
            if len(win) >= WIN_SIZE:
                win.pop(0)

        return False

if __name__ == "__main__":
    predict(sys.argv[1])
