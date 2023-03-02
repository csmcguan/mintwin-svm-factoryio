from sklearn.svm import OneClassSVM
import csv
import joblib
import subprocess
import sys
import time

def predict(log):
    head, tail = 0, 50
    WIN_SIZE = tail - head
    identified = False

    with open("./util/monitor-pred.csv", "w") as w:
        w = csv.writer(w)
        w.writerow(["prediction", "time"])

    start = time.time()
    while True:
        with open(log, "r") as r, open("./util/monitor-pred.csv", "a+") as w:
            svm = joblib.load("./util/svm.dmp")
            data = list(csv.reader(r))
            w = csv.writer(w)

            if int(tail) > len(data):
                w.writerow([1, str(time.time() - start)])
                continue

            win = data[head:tail]
            pred = svm.predict(win)
            count = 0
            for i in range(len(pred)):
                if pred[i] == -1:
                    count += 1
            if count / WIN_SIZE >= 0.6:
                if not identified:
                    identified = True
                    id_time = time.time()
                    print("Attack identified at time: " + str(id_time - start))
                    sys.stdout.flush()
                    
                    with open("./time.csv", "a+") as fp:
                        rel_time = id_time - start - 30
                        writer = csv.writer(fp)
                        writer.writerow([rel_time])

                w.writerow([0, str(time.time() - start)])
            else:
                w.writerow([1, str(time.time() - start)])
            head += 1
            tail += 1
        time.sleep(0.1)

if __name__ == "__main__":
    predict(sys.argv[1])
