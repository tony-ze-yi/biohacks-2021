import subprocess
import codecs
import matplotlib.pyplot as plt


def run_sequential():
    times = []
    for i in range(10):
        result = subprocess.run(['python3', 'seq-algo.py', 'a.txt', 'b.txt'], stdout=subprocess.PIPE)
        print(result.stdout)
        time = str(result.stdout[11:26])
        normal_str = codecs.decode(time, 'unicode_escape')
        times.append(float(normal_str[2:len(normal_str) - 1]))
    return times

def run_parallel():
    times = []
    for i in range(10):
        result = subprocess.run(['python3', 'main.py', 'a.txt', 'b.txt'], stdout=subprocess.PIPE)
        print(result.stdout)
        time = str(result.stdout[11:26])
        normal_str = codecs.decode(time, 'unicode_escape')
        times.append(float(normal_str[2:len(normal_str) - 1]))
    return times

def plot_sequential_vs_parallel():
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    method = ['Sequential', 'Parallel']
    sequential = run_sequential()
    parallel = run_parallel()
    times = [sum(sequential) / len(sequential), sum(parallel) / len(parallel)]
    ax.bar(method, times)
    plt.show()
    plt.savefig("Seq vs parallel.png", dpi=200)



if __name__ == '__main__':
    run_parallel()