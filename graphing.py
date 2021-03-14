import subprocess
import codecs
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')
from main import *
from seq_algo import *


def run_sequential(file1, file2, repeat):
    times = []
    for i in range(repeat):
        time = run_for_timing(file1, file2)
        times.append(time)

        result = subprocess.run(
            ["python3", "seq_algo.py", file1, file2], stdout=subprocess.PIPE
        )
        print(result.stdout)
        time = str(result.stdout[11:26])
        normal_str = codecs.decode(time, "unicode_escape")
        times.append(float(normal_str[2: len(normal_str) - 1]))
    return times


def run_parallel(file1, file2, repeat):
    times = []
    for i in range(repeat):
        result = subprocess.run(
            ["python3", "main.py", file1, file2], stdout=subprocess.PIPE
        )
        print(result.stdout)
        time = str(result.stdout[11:26])
        normal_str = codecs.decode(time, "unicode_escape")
        times.append(float(normal_str[2: len(normal_str) - 1]))
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
    method = ["Sequential", "Parallel"]
    # sequential = run_sequential('covid.txt', 'sars.txt', 2)
    # parallel = run_parallel('covid.txt', 'sars.txt', 2)
    data = run_both_regular("covid19.txt", "sars.txt", 2)
    sequential = data[0]
    parallel = data[1]
    times = [sum(sequential) / len(sequential), sum(parallel) / len(parallel)]
    plt.bar(method, times)
    plt.title("Runtime for parallel vs sequential with a 5000 long DNA sequence")
    plt.xlabel("Method")
    plt.ylabel("average time(seconds)")
    plt.savefig("Seq vs parallel regular.png", dpi=200)


def plot_sequential_vs_parallel_bar_custom():
    method = ["Sequential", "Parallel"]
    # sequential = run_sequential('covid.txt', 'sars.txt', 2)
    # parallel = run_parallel('covid.txt', 'sars.txt', 2)
    data = run_both_custom("covid19.txt", "sars.txt", 2)
    sequential = data[0]
    parallel = data[1]
    times = [sum(sequential) / len(sequential), sum(parallel) / len(parallel)]
    plt.bar(method, times)
    plt.title(
        "Runtime for parallel vs sequential with a 5000 long DNA sequence custom algorithm"
    )
    plt.xlabel("Method")
    plt.ylabel("average time(seconds)")
    plt.savefig("Seq vs parallel custom.png", dpi=200)


def plot_sequential_vs_parallel_line():
    files = [
        "500.txt",
        "500_2.txt",
        "1000.txt",
        "1000_2.txt",
        "5000.txt",
        "5000_2.txt",
        "10000.txt",
        "10000_2.txt",
        "20k.txt",
        "20k_2.txt",
        # "50k.txt",
        # "50k_2.txt"
    ]
    sizes = [500, 1000, 5000, 10000, 20000]
    times_seq = []
    times_parallel = []
    i = 0
    while i < len(files):
        data = run_both_regular(files[i], files[i + 1], 1)
        seq = data[0]
        par = data[1]
        times_seq.extend(seq)
        times_parallel.extend(par)
        i += 2
    #
    # plt.plot(sizes, times_seq, label="Sequential")
    # plt.plot(sizes, times_parallel, label="Parallel")

    plt.xlabel("DNA Sequence length")

    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.title("Runtime for sequential and parallel algorithms with varying sizes")
    plt.savefig("Line graph seq vs parallel.png", dpi=200)


def plot_sequential_vs_parallel_line_custom():
    files = [
        "500.txt",
        "500_2.txt",
        "1000.txt",
        "1000_2.txt",
        "5000.txt",
        "5000_2.txt",
        "10000.txt",
        "10000_2.txt",
        "20k.txt",
        "20k_2.txt",
        # "50k.txt",
        # "50k_2.txt"
    ]
    sizes = [500, 1000, 5000, 10000, 20000]
    times_seq = []
    times_parallel = []
    i = 0
    while i < len(files):
        data = run_both_custom(files[i], files[i + 1], 1)
        seq = data[0]
        par = data[1]
        times_seq.extend(seq)
        times_parallel.extend(par)
        i += 2
    #
    # plt.plot(sizes, times_seq, label="Sequential")
    # plt.plot(sizes, times_parallel, label="Parallel")

    plt.xlabel("DNA Sequence length")

    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.title("Runtime for sequential and parallel algorithms with varying sizes")
    plt.savefig("Line graph seq vs parallel custom algo.png", dpi=200)


def plot_seq_vs_par_both():
    files = ['500.txt', '500_2.txt', '1000.txt', '1000_2.txt', '5000.txt', '5000_2.txt', '10000.txt', '10000_2.txt',
             '20k.txt', '20k_2.txt']
    sizes = [500, 1000, 5000, 10000, 20000]
    times_seq = []
    times_parallel = []
    times_seq_custom = []
    times_par_custom = []
    i = 0
    while i < len(files):
        data = run_both_custom(files[i], files[i + 1], 1)
        seq = data[0]
        par = data[1]
        times_seq_custom.extend(seq)
        times_par_custom.extend(par)

        data = run_both_regular(files[i], files[i + 1], 1)
        seq = data[0]
        par = data[1]
        times_seq.extend(seq)
        times_parallel.extend(par)
        i += 2

    with open("Output.txt", "w") as text_file:
        text_file.write("\nsequential\n")
        text_file.write(str(times_seq))
        text_file.write("\nparallel\n")
        text_file.write(str(times_parallel))
        text_file.write("\nsequential custom\n")
        text_file.write(str(times_seq_custom))
        text_file.write("\nparallel custom\n")
        text_file.write(str(times_par_custom))

    # plt.plot(sizes, times_seq, label="Sequential")
    # plt.plot(sizes, times_parallel, label="Parallel")
    # plt.plot(sizes, times_seq_custom, label="Sequential custom algorithm")
    # plt.plot(sizes, times_par_custom, label="Parallel custom algorithm")

    plt.xlabel("DNA Sequence length")

    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.title("Runtime for sequential and parallel algorithms with varying sizes")
    plt.savefig("Line graph seq vs parallel custom algo.png", dpi=200)

    plt.close()

    # plt.plot(sizes, times_par_custom, label="Parallel custom algorithm")
    # plt.plot(sizes, times_parallel, label="Parallel")
    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.title("Runtime for parallel algorithms with varying sizes")
    plt.savefig("Line graph just parallel.png", dpi=200)

    plt.close()

    # plt.plot(sizes, times_seq, label="Sequential algorithm")
    # plt.plot(sizes, times_seq_custom, label="Custom Sequential algorithm")
    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.title("Runtime for sequential algorithms with varying sizes")
    plt.savefig("Line graph just sequential.png", dpi=200)


def plot_covid():
    par_time, seq_time = regular_alg(covid, sars)
    par_time_custom, seq_time_custom = custom_alg(covid, sars)
    plt.bar(["parallel", "sequential", "parallel custom", "sequential custom"],
            [par_time, seq_time, par_time_custom, seq_time_custom])
    plt.xlabel("Algorithms")
    plt.ylabel("Time (seconds)")
    plt.savefig("bar_all.png", dpi=200)
    plt.close()


if __name__ == "__main__":
    # plot_sequential_vs_parallel_bar_custom()
    # plot_sequential_vs_parallel_bar()
    # plot_sequential_vs_parallel_line()
    # plot_sequential_vs_parallel_line_custom()
    # plot_seq_vs_par_both()
    plot_covid()
