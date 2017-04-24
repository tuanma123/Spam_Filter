import naive_bayes
correct_output_map = []
with open("true_labels.txt") as f:
    correct_map = f.readlines()

for line in correct_map:
    correct_output_map.append(line.split(" ")[1].replace("\n", ""))


def stats(k):
    output = [0, 0, 0, 0, 0]
    my_output_map = naive_bayes.output_map("data/test", k)
    for x in range(0, len(my_output_map.keys())):
        file = str(x+1) + ".txt"
        my_label =my_output_map[file]
        correct_label = correct_output_map[x]
        if correct_label == "spam":
            if my_label == "spam":
                output[1] += 1
            else:
                output[2] += 1
        else:
            if my_label == "ham":
                output[0] += 1
            else:
                output[3] += 1
    output[4] = (output[0] + output[1]) / len(my_output_map.keys())
    return output


def optimize():
    csv = open("k values.csv", "w")
    best = stats(1)
    csv.write("K Value, Correct Ham, Correct Spam, Incorrect Ham, Incorrect Spam, Percentage Accuracy")
    for x in range(1, 5001):
        k = x * 0.05
        trial = stats(k)
        data = str(k) + "," + str(trial[0]) + "," + str(trial[1]) + "," + str(trial[2]) + "," + str(trial[3]) + "," \
               + str(trial[4])
        csv.write(data)
        print(data)

        if trial[4] > best[4]:
            best = trial
    csv.close()
    print(best)
optimize()