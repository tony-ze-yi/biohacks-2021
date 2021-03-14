import subprocess
import codecs
import matplotlib.pyplot as plt
from main import *
from seq_algo import *



def run_sequential(file1, file2, repeat):
    times = []
    for i in range(repeat):
        time = run_for_timing(file1, file2)
        times.append(time)

        result = subprocess.run(['python3', 'seq_algo.py', file1, file2], stdout=subprocess.PIPE)
        print(result.stdout)
        time = str(result.stdout[11:26])
        normal_str = codecs.decode(time, 'unicode_escape')
        times.append(float(normal_str[2:len(normal_str) - 1]))
    return times

def run_parallel(file1, file2, repeat):
    times = []
    for i in range(repeat):
        result = subprocess.run(['python3', 'main.py', file1, file2], stdout=subprocess.PIPE)
        print(result.stdout)
        time = str(result.stdout[11:26])
        normal_str = codecs.decode(time, 'unicode_escape')
        times.append(float(normal_str[2:len(normal_str) - 1]))
    return times


def run_both_regular(file1, file2, repeat):
    times_seq = []
    times_par = []
    with open(file1, "r") as file:
        string1 = file.read().replace("\n", "")

    with open(file2, "r") as file:
        string2 = file.read().replace("\n", "")

    str_arr1 = np.array(list(string1))
    str_arr2 = np.array(list(string2))
    for i in range(repeat):
        res = regular_alg(str_arr1, str_arr2)
        seq = res[1]
        par = res[0]
        times_seq.append(seq)
        times_par.append(par)

    return times_seq, times_par


def run_both_custom(file1, file2, repeat):
    times_seq = []
    times_par = []
    with open(file1, "r") as file:
        string1 = file.read().replace("\n", "")

    with open(file2, "r") as file:
        string2 = file.read().replace("\n", "")

    str_arr1 = np.array(list(string1))
    str_arr2 = np.array(list(string2))
    for i in range(repeat):
        res = custom_alg(str_arr1, str_arr2)
        seq = res[1]
        par = res[0]
        times_seq.append(seq)
        times_par.append(par)

    return times_seq, times_par


def get_nums():
    return [1, 2, 3, 4, 4, 3, 2, 1]

def plot_sequential_vs_parallel_bar():
    method = ['Sequential', 'Parallel']
    # sequential = run_sequential('covid.txt', 'sars.txt', 2)
    # parallel = run_parallel('covid.txt', 'sars.txt', 2)
    data = run_both_regular('covid19.txt', 'sars.txt', 2)
    sequential = data[0]
    parallel = data[1]
    times = [sum(sequential) / len(sequential), sum(parallel) / len(parallel)]
    plt.bar(method, times)
    plt.title("Runtime for parallel vs sequential with a 5000 long DNA sequence")
    plt.xlabel("Method")
    plt.ylabel('average time(seconds)')
    plt.savefig("Seq vs parallel regular.png", dpi=200)

def plot_sequential_vs_parallel_bar_custom():
    method = ['Sequential', 'Parallel']
    # sequential = run_sequential('covid.txt', 'sars.txt', 2)
    # parallel = run_parallel('covid.txt', 'sars.txt', 2)
    data = run_both_custom('covid19.txt', 'sars.txt', 2)
    sequential = data[0]
    parallel = data[1]
    times = [sum(sequential) / len(sequential), sum(parallel) / len(parallel)]
    plt.bar(method, times)
    plt.title("Runtime for parallel vs sequential with a 5000 long DNA sequence custom algorithm")
    plt.xlabel("Method")
    plt.ylabel('average time(seconds)')
    plt.savefig("Seq vs parallel custom.png", dpi=200)

def plot_sequential_vs_parallel_line():
    files = ['500.txt', '500_2.txt', '1000.txt', '1000_2.txt', '5000.txt', '5000_2.txt', '10000.txt', '10000_2.txt',
             '20k.txt', '20k_2.txt', '50k.txt', '50k_2.txt', '100k.txt', '100k_2.txt']
    sizes = [500, 1000, 5000, 10000, 20000, 50000, 100000]
    times_seq = []
    times_parallel = []
    i = 0
    while i < len(files):
        data = run_both_regular(files[i], files[i+1], 1)
        seq = data[0]
        par = data[1]
        times_seq.extend(seq)
        times_parallel.extend(par)
        i += 2

    plt.plot(sizes, times_seq, label="Sequential")
    plt.plot(sizes, times_parallel, label="Parallel")

    plt.xlabel("DNA Sequence length")

    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.title("Runtime for sequential and parallel algorithms with varying sizes")
    plt.savefig("Line graph seq vs parallel.png", dpi=200)

def plot_sequential_vs_parallel_line_custom():
    files = ['500.txt', '500_2.txt', '1000.txt', '1000_2.txt', '5000.txt', '5000_2.txt', '10000.txt', '10000_2.txt',
             '20k.txt', '20k_2.txt', '50k.txt', '50k_2.txt', '100k.txt', '100k_2.txt']
    sizes = [500, 1000, 5000, 10000, 20000, 50000, 100000]
    times_seq = []
    times_parallel = []
    i = 0
    while i < len(files):
        data = run_both_custom(files[i], files[i+1], 1)
        seq = data[0]
        par = data[1]
        times_seq.extend(seq)
        times_parallel.extend(par)
        i += 2

    plt.plot(sizes, times_seq, label="Sequential")
    plt.plot(sizes, times_parallel, label="Parallel")

    plt.xlabel("DNA Sequence length")

    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.title("Runtime for sequential and parallel algorithms with varying sizes")
    plt.savefig("Line graph seq vs parallel custom algo.png", dpi=200)


if __name__ == '__main__':
    plot_sequential_vs_parallel_bar_custom()
    plot_sequential_vs_parallel_bar()
    plot_sequential_vs_parallel_line()
    plot_sequential_vs_parallel_line_custom()
