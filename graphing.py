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
        print(time)
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

def get_nums():
    return [1, 2, 3, 4, 4, 3, 2, 1]

def plot_sequential_vs_parallel_bar():
    method = ['Sequential', 'Parallel']
    sequential = run_sequential('covid.txt', 'sars.txt', 2)
    parallel = run_parallel('covid.txt', 'sars.txt', 2)
    times = [sum(sequential) / len(sequential), sum(parallel) / len(parallel)]
    plt.bar(method, times)
    plt.title("Runtime for parallel vs sequential with a 5000 long DNA sequence")
    plt.xlabel("Method")
    plt.ylabel('average time(seconds)')
    plt.savefig("Seq vs parallel.png", dpi=200)

def plot_sequential_vs_parallel_line():
    files = ['500.txt', '500_2.txt', '1000.txt', '1000_2.txt', '5000.txt', '5000_2.txt', '10000.txt', '10000_2.txt',
             '20k.txt', '20k_2.txt', '50k.txt', '50k_2.txt', '100k.txt', '100k_2.txt']
    sizes = [500, 1000, 5000, 10000, 20000, 50000, 100000]
    times_seq = [50, 75, 125, 200, 300, 600, 1200]
    times_parallel = [10, 20, 40, 50, 60, 70, 80]
    i = 0
    while i < len(files):
        seq = run_sequential(files[i], files[i+1], 1)
        par = run_parallel(files[i], files[i+1], 1)
        times_seq.extend(seq)
        times_parallel.extend(par)
        i += 1

    plt.plot(sizes, times_seq, label="Sequential")
    plt.plot(sizes, times_parallel, label="Parallel")

    plt.xlabel("DNA Sequence length")

    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.title("Runtime for sequential and parallel algorithms with varying sizes")
    plt.savefig("Line graph seq vs parallel.png", dpi=200)


if __name__ == '__main__':
    # plot_sequential_vs_parallel_bar()
    # plot_sequential_vs_parallel_line()
    run_parallel('a.txt', 'b.txt', 1)