
export GEM5_DIR=/home/011/a/ax/axb200166/Desktop/Akash/CompArch/gem5
export BENCHMARK=/home/011/a/ax/axb200166/m5out/benchmarks/458.sjeng/src/benchmark
export ARGUMENT=/home/011/a/ax/axb200166/m5out/benchmarks/458.sjeng/data/test.txt
time $GEM5_DIR/build/X86/gem5.opt -d ~/m5out $GEM5_DIR/configs/example/se.py -c $BENCHMARK -o $ARGUMENT -I 500000000 --cpu-type=timing --caches --l2cache --l1d_size=128kB --l1i_size=128kB --l2_size=1MB --l1d_assoc=2 --l1i_assoc=2 --l2_assoc=4 --cacheline_size=64

#'20 reference.dat 0 1 ./data/100_100_130_cf_a.of'
