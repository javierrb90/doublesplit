import argparse, os

parser = argparse.ArgumentParser(description='Process some integers.')


parser.add_argument('-i',default=os.getcwd(),dest="input")

parser.add_argument('-o',dest="output")

# El threshold para la conversion BW
parser.add_argument('-t', default=150, dest="threshold")

# El ancho en pixels del margen central
parser.add_argument('-w', default=25, dest="sepwidth")

# El numero de paginas que queremos samplear
parser.add_argument('-s', dest="sample")

args = parser.parse_args()


config={}

if args.output is None:
    if os.path.isdir(args.input):
        config["output"] = os.path.join(args.input,"output")
    else: 
        input_path = os.path.dirname(os.path.abspath(args.input))
        config["output"] = os.path.join(input_path,"output")
else:
    config["output"] = args.output


if os.path.isdir(args.input):
    targets = []
    for file in os.listdir(args.input):
        if file.endswith(".zip") or file.endswith(".cbz"):
           targets.append(os.path.join(args.input,file))
else:
    targets = [args.input]

if args.sample is not None:
    config['sample'] = int(args.sample)
else:
    config['sample'] = None

config['threshold'] = int(args.threshold)
config['sepwidth'] = int(args.sepwidth)
