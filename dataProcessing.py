# -*- coding: utf-8 -*-
# @Time    : 1/27/21 8:54 PM
# @Author  : Kay
# @Email   : kahy.shen@gmail.com
# @File    : dataProcessing.py
# @Desc    :
import jsonlines
import csv
import json
import copy
import random


def read_data(filename):
    data = []
    with jsonlines.open(filename) as f:
        for line in f.iter():
            data.append(line)
    # print(len(data))
    return data


def read_label(filename):
    labels = []
    with open(filename, "r") as file:
        data = file.readlines()
        for line in data:
            # print(line.split("\n")[0])
            labels.append(line.split("\n")[0])
    # print(len(labels))
    return labels


def read(filename1, filename2):
    questions = read_data(filename1)
    labels = read_label(filename2)
    return questions, labels


def NoQuestion(dataset):
    data = []
    for line in dataset:

        # line['goal'] = ""  # PIQA
        # line['obs1'] = ""
        # line['obs2'] = ""  # aNLI
        # line['context'] = ""
        # line['question'] = ""  # socialiqa
        line['ctx_a'] = ""
        line['ctx_b'] = ""
        line['ctx'] = ""  # Hellaswag
        data.append(line)
    return data


def jaccardIndex(l1, l2):
    return len(set(l1).intersection(set(l2))) / len(set(l1).union(set(l2)))


def WrongQuestion(dataset):
    # dataset1 = copy.deepcopy(dataset)
    # randomPairedIdx = {}
    # while dataset1:
    #     q1 = dataset1[0]
    #     dataset1.remove(q1)
    #     q2 = random.choice(dataset1)
    #     dataset1.remove(q2)
    #     randomPairedIdx[dataset.index(q1)] = dataset.index(q2)
    #     randomPairedIdx[dataset.index(q2)] = dataset.index(q1)
    #
    # # print(len(randomPairedIdx))
    # dataset1 = []
    # for line in dataset:
    #     tmp = copy.deepcopy(line)
    #     pairidx = randomPairedIdx[dataset.index(tmp)]
    #     # tmp['goal'] = dataset[randomPairedIdx[dataset.index(tmp)]]['goal']  # PIQA
    #     # tmp['obs1'] = dataset[pairidx]['obs1']
    #     # tmp['obs2'] = dataset[pairidx]['obs2']  # aNLI
    #     # tmp['context'] = dataset[pairidx]['context']
    #     # tmp['question'] = dataset[pairidx]['question']  # socialiqa
    #     tmp['ctx_a'] = dataset[pairidx]['ctx_a']
    #     tmp['ctx_b'] = dataset[pairidx]['ctx_b']
    #     tmp['ctx'] = dataset[pairidx]['ctx']  # hellaswag
    #     dataset1.append(tmp)

    dataset2 = copy.deepcopy(dataset)
    for line in dataset2:
        # line['sol1'] = line['sol1'].split(' ')
        # line['sol2'] = line['sol2'].split(' ')  # PIQA
        line['hyp1'] = line['hyp1'].split(' ')
        line['hyp2'] = line['hyp2'].split(' ')  # aNLI
        # line['answerA'] = line['answerA'].split(' ')
        # line['answerB'] = line['answerB'].split(' ')
        # line['answerC'] = line['answerC'].split(' ')  # socialiqa
        # for i in range(len(line['ending_options'])):
        #     line['ending_options'][i] = line['ending_options'][i].split(' ')

    candidatePairIdx = {}
    for line1 in dataset2:
        candidatePairIdx[dataset2.index(line1)] = []
        for line2 in dataset2:
            if line1 != line2:
                # if jaccardIndex(line1['ending_options'][0], line2['ending_options'][0]) == 0 and\
                #         jaccardIndex(line1['ending_options'][1], line2['ending_options'][1]) == 0 and \
                #         jaccardIndex(line1['ending_options'][2], line2['ending_options'][2]) == 0 and \
                #         jaccardIndex(line1['ending_options'][3], line2['ending_options'][3]) == 0:
                if jaccardIndex(line1['hyp1'], line2['hyp1']) == 0 and \
                        jaccardIndex(line1['hyp2'], line2['hyp2']) == 0:
                    candidatePairIdx[dataset2.index(line1)].append(dataset2.index(line2))
    candidatePair = {}
    for idx in candidatePairIdx:
        pidx = random.choice(candidatePairIdx[idx])
        candidatePair[idx] = pidx
        candidatePair[pidx] = idx
    # candidatePairIdx = {idx: random.choice(candidatePairIdx[idx]) for idx in candidatePairIdx}
    dataset2 = []
    for line in dataset:
        tmp = copy.deepcopy(line)
        pairidx = candidatePair[dataset.index(tmp)]
        # tmp['goal'] = dataset[pairidx]['goal']  # PIQA
        tmp['obs1'] = dataset[pairidx]['obs1']
        tmp['obs2'] = dataset[pairidx]['obs2']  # aNLI
        # tmp['context'] = dataset[pairidx]['context']
        # tmp['question'] = dataset[pairidx]['question']  # socialiqa
        # tmp['ctx_a'] = dataset[pairidx]['ctx_a']
        # tmp['ctx_b'] = dataset[pairidx]['ctx_b']
        # tmp['ctx'] = dataset[pairidx]['ctx']  # hellaswag
        dataset2.append(tmp)

    return dataset2, candidatePair

def NoRAnswer(dataset, label):
    # labelDict = {1: 'answerA', 2: 'answerB', 3: 'answerC'}
    dataset1 = copy.deepcopy(dataset)
    randomPairedIdx = {}
    while dataset1:
        q1 = dataset1[0]
        dataset1.remove(q1)
        q2 = random.choice(dataset1)
        dataset1.remove(q2)
        randomPairedIdx[dataset.index(q1)] = dataset.index(q2)
        randomPairedIdx[dataset.index(q2)] = dataset.index(q1)

    dataset1 = []
    for i in range(len(dataset)):
        tmp = copy.deepcopy(dataset[i])
        pairidx = randomPairedIdx[dataset.index(tmp)]
        targetQ = dataset[pairidx]
        # print(targetQ)
        # tmp[labelDict[int(label[i])]] = random.choice([targetQ['answerA'], targetQ['answerB'], targetQ['answerC']])
        # tmp['ending_options'][int(label[i])] = random.choice(targetQ['ending_options'])
        tmp['sol{}'.format(int(label[i]) + 1)] = random.choice([targetQ['sol1'], targetQ['sol2']])
        dataset1.append(tmp)

    # dataset2 = copy.deepcopy(dataset)
    # for line in dataset2:
    #     # line['sol1'] = line['sol1'].split(' ')
    #     # line['sol2'] = line['sol2'].split(' ')  # PIQA
    #     # line['hyp1'] = line['hyp1'].split(' ')
    #     # line['hyp2'] = line['hyp2'].split(' ')  # aNLI
    #     line['answerA'] = line['answerA'].split(' ')
    #     line['answerB'] = line['answerB'].split(' ')
    #     line['answerC'] = line['answerC'].split(' ')  # socialiqa
    # candidatePairIdx = {}
    # for line1 in dataset2:
    #     candidatePairIdx[dataset2.index(line1)] = []
    #     for line2 in dataset2:
    #         if line1 != line2:
    #             if jaccardIndex(line1['answerA'], line2['answerA']) == 0 \
    #                     and jaccardIndex(line1['answerB'], line2['answerB']) == 0 \
    #                     and jaccardIndex(line1['answerC'], line2['answerC']) == 0:
    #                 candidatePairIdx[dataset2.index(line1)].append(dataset2.index(line2))
    # candidatePair = {}
    # for idx in candidatePairIdx:
    #     pairIdx = random.choice(candidatePairIdx[idx])
    #     candidatePair[idx] = pairIdx
    #     candidatePair[pairIdx] = idx
    # dataset2 = []
    # for i in range(len(dataset)):
    #     # print(label[i])
    #     tmp = copy.deepcopy(dataset[i])
    #     pairidx = candidatePair[dataset.index(tmp)]
    #     targetQ = dataset[pairidx]
    #     # print(targetQ)
    #     print(labelDict[int(label[i])])
    #     tmp[labelDict[int(label[i])]] = random.choice([targetQ['answerA'], targetQ['answerB'], targetQ['answerC']])
    #
    #     dataset2.append(tmp)

    return dataset1


def output(dataset, label, datasetName, labelName):
    with open("{}".format(datasetName), "w") as f:
        for line in dataset:
            json.dump(line, f)
            f.write("\n")
    with open("{}".format(labelName), "w") as f:
        f.write("\n".join(label))


if __name__ == '__main__':
    questions, labels = read('./hellaswag/dev.jsonl',
         './hellaswag/dev-labels.lst')

    # questions = NoRAnswer(questions, labels)
    # output(questions, labels, 'data/PIQA/NoRightARandomdev.jsonl', 'data/PIQA/NoRightARandomdev-labels.lst')

    # questions, pairedIdx = WrongQuestion(questions)
    # output(questions, labels, 'data/aNLI/WrongQNoOverlapdev.jsonl', 'data/aNLI/WrongQNoOverlapdev-labels.lst')

    # NoQQuestion = NoQuestion(questions)
    # output(NoQQuestion, labels, 'data/Hellaswag/NoQdev.jsonl', 'data/Hellaswag/NoQdev-labels.lst')

