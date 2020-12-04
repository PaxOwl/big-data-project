FC = gfortran
FFLAGS = -Wall
LDFLAGS = 

SRCS = $(wildcard *.f90)
OBJS = $(SRCS:.f90=.o)
EXEC = $(SRCS:.f90=)

all: $(EXEC)

%.o: %.f90
	$(FC) $(FFLAGS) -c $<

%: %.o
	$(FC) $(LDFLAGS) -o $@ $<

clean:
	rm -f $(OBJS) $(EXEC)
