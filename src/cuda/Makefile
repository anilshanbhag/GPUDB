
OS_SIZE = $(shell uname -m | sed -e "s/i.86/32/" -e "s/x86_64/64/")

CUDA_PATH       ?= /usr/local/cuda
CUDA_INC_PATH   ?= $(CUDA_PATH)/include
CUDA_BIN_PATH   ?= $(CUDA_PATH)/bin

ifeq ($(OS_SIZE),32)
    CUDA_LIB_PATH  ?= $(CUDA_PATH)/lib
else
    CUDA_LIB_PATH  ?= $(CUDA_PATH)/lib64
endif

NVCC            ?= $(CUDA_BIN_PATH)/nvcc

GENCODE_SM20    := -gencode arch=compute_20,code=sm_20
GENCODE_SM30    := -gencode arch=compute_30,code=sm_30 -gencode arch=compute_35,code=sm_35
GENCODE_SM50    := -gencode arch=compute_50,code=sm_50
GENCODE_FLAGS   := $(GENCODE_SM50)

ifeq ($(OS_SIZE),32)
    LDFLAGS   := -lcudart -lrt
else
    LDFLAGS   := -lcudart -lrt
endif

%.o: %.cu $(DEPS)
	$(NVCC) -c -g $(GENCODE_FLAGS) $<

gpudb: tableScan.o inviJoin.o hashJoin.o cuckoo.o materialize.o groupby.o orderBy.o driver.o
	 $(NVCC) -pg tableScan.o inviJoin.o hashJoin.o cuckoo.o materialize.o groupby.o orderBy.o driver.o $(LDFLAGS) -o GPUDATABASE

all: gpudb

clean:
	rm -rf *.o GPUDATABASE
