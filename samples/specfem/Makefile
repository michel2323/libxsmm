# Export all variables to sub-make processes.
#.EXPORT_ALL_VARIABLES: #export

# Automatically disable parallel builds
# depending on the version of GNU Make.
# MAKE_PARALLEL=0: disable explicitly
# MAKE_PARALLEL=1: enable explicitly
ifeq (0,$(MAKE_PARALLEL))
.NOTPARALLEL:
else ifeq (,$(MAKE_PARALLEL))
ifneq (3.82,$(firstword $(sort $(MAKE_VERSION) 3.82)))
.NOTPARALLEL:
endif
endif

ROOTDIR = $(abspath $(dir $(firstword $(MAKEFILE_LIST))))
DEPDIR = ../..
SRCDIR = $(ROOTDIR)
INCDIR = .
BLDDIR = build
OUTDIR = .

CXXFLAGS = $(NULL)
CFLAGS = $(NULL)
DFLAGS = $(NULL)
IFLAGS = -I$(INCDIR) -I$(DEPDIR)/include

BLAS = 1
OMP = 1
SYM = 1

# include common Makefile artifacts
include $(DEPDIR)/Makefile.inc

OUTNAME := $(shell basename $(ROOTDIR))
HEADERS := $(shell ls -1 $(INCDIR)/*.h   2> /dev/null | tr "\n" " ") \
           $(shell ls -1 $(INCDIR)/*.hpp 2> /dev/null | tr "\n" " ") \
           $(shell ls -1 $(INCDIR)/*.hxx 2> /dev/null | tr "\n" " ") \
           $(shell ls -1 $(INCDIR)/*.hh  2> /dev/null | tr "\n" " ") \
           $(shell ls -1 $(SRCDIR)/*.h   2> /dev/null | tr "\n" " ") \
           $(shell ls -1 $(SRCDIR)/*.hpp 2> /dev/null | tr "\n" " ") \
           $(shell ls -1 $(SRCDIR)/*.hxx 2> /dev/null | tr "\n" " ") \
           $(shell ls -1 $(SRCDIR)/*.hh  2> /dev/null | tr "\n" " ")
CPPSRCS := $(shell ls -1 $(SRCDIR)/*.cpp 2> /dev/null | tr "\n" " ")
CXXSRCS := $(shell ls -1 $(SRCDIR)/*.cxx 2> /dev/null | tr "\n" " ")
CCXSRCS := $(shell ls -1 $(SRCDIR)/*.cc  2> /dev/null | tr "\n" " ")
CSOURCS := $(shell ls -1 $(SRCDIR)/*.c   2> /dev/null | tr "\n" " ")
FXXSRCS := $(shell ls -1 $(SRCDIR)/*.f   2> /dev/null | tr "\n" " ")
F77SRCS := $(shell ls -1 $(SRCDIR)/*.F   2> /dev/null | tr "\n" " ")
F90SRCS := $(shell ls -1 $(SRCDIR)/*.f90 2> /dev/null | tr "\n" " ") \
           $(shell ls -1 $(SRCDIR)/*.F90 2> /dev/null | tr "\n" " ")

CPPOBJS := $(patsubst %,$(BLDDIR)/%,$(notdir $(CPPSRCS:.cpp=-cpp.o)))
CXXOBJS := $(patsubst %,$(BLDDIR)/%,$(notdir $(CXXSRCS:.cxx=-cxx.o)))
CCXOBJS := $(patsubst %,$(BLDDIR)/%,$(notdir $(CCXSRCS:.cc=-cc.o)))
COBJCTS := $(patsubst %,$(BLDDIR)/%,$(notdir $(CSOURCS:.c=-c.o)))
FXXOBJS := $(patsubst %,$(BLDDIR)/%,$(notdir $(FXXSRCS:.f=-f.o)))
F77OBJS := $(patsubst %,$(BLDDIR)/%,$(notdir $(F77SRCS:.F=-f77.o)))
F90OBJS := $(patsubst %,$(BLDDIR)/%,$(notdir $(F90SRCS:.f90=-f90.o)))
F90OBJS := $(patsubst %,$(BLDDIR)/%,$(notdir $(F90SRCS:.F90=-f90.o)))

SOURCES := $(CPPSRCS) $(CXXSRCS) $(CCXSRCS) $(CSOURCS)
OBJECTS := $(CPPOBJS) $(CXXOBJS) $(CCXOBJS) $(COBJCTS)
FTNSRCS := $(FXXSRCS) $(F77SRCS) $(F90SRCS)
MODULES := $(addsuffix .mod,$(basename $(FTNSRCS))) $(addsuffix .modmic,$(basename $(FTNSRCS)))
FTNOBJS := $(FXXOBJS) $(F77OBJS) $(F90OBJS)
XFILES := $(OUTDIR)/$(OUTNAME)

# specfem example specific
MODULES += my_libxsmm.mod constants.mod specfem_par.mod my_libxsmm.modmic constants.modmic specfem_par.modmic
DFLAGS += -DFORCE_VECTORIZATION

# OpenMP directives support
ifneq (0,$(OMP))
DFLAGS += -DUSE_OPENMP
endif

# fixes library paths: substitutes path name from ../mkl/lib/intel64/.. to ../mkl/lib/mic/..
ifneq (0,$(KNC))
ifneq (0,$(MPSS))
lib_intel := mkl/lib/intel64
lib_mic := mkl/lib/mic
LDFLAGS_MIC = $(subst $(lib_intel),$(lib_mic),$(LDFLAGS))
endif
endif

##
## targets
##

.PHONY: all
all: $(XFILES)

.PHONY: compile
compile: $(OBJECTS) $(FTNOBJS)

$(OUTDIR)/specfem: $(OUTDIR)/.make $(FTNOBJS) $(LIBNAME).$(LIBEXT)
ifneq (0,$(KNC))
ifneq (0,$(MPSS))
	@echo ""
	@echo "building MIC/KNC version"
	@echo ""
	$(FC) -o $@ -mmic $(FTNOBJS) $(call abslib,$(LIBNAME)f.$(LIBEXT)) $(call abslib,$(LIBNAME).$(LIBEXT)) $(FCMTFLAGS) $(SLDFLAGS) $(LDFLAGS_MIC) $(FLDFLAGS) $(ELDFLAGS)
endif
endif
ifeq (0,$(KNC))
ifeq (0,$(MPSS))
	@echo ""
	@echo "building host version"
	@echo ""
	$(FC) -o $@ $(FTNOBJS) $(call abslib,$(LIBNAME)f.$(LIBEXT)) $(call abslib,$(LIBNAME).$(LIBEXT)) $(FCMTFLAGS) $(SLDFLAGS) $(LDFLAGS) $(FLDFLAGS) $(ELDFLAGS)
endif
endif

.PHONY: clean-minimal
clean-minimal:
	@rm -f $(OBJECTS) $(FTNOBJS) $(MODULES)
	@rm -f fit.log *.dat
	@rm -f *__genmod.*

.PHONY: clean
clean: clean-minimal
ifneq ($(abspath $(BLDDIR)),$(ROOTDIR))
ifneq ($(abspath $(BLDDIR)),$(abspath .))
	@rm -rf $(BLDDIR)
endif
endif

.PHONY: realclean
realclean: clean
ifneq ($(abspath $(OUTDIR)),$(ROOTDIR))
ifneq ($(abspath $(OUTDIR)),$(abspath .))
	@rm -rf $(OUTDIR)
else
	@rm -f $(XFILES)
endif
else
	@rm -f $(XFILES)
endif
	@rm -f $(MODULES) $(ROOTDIR)/specfem-perf.sh
	@rm -f *.gcno *.gcda *.gcov
	@rm -f $(OUTDIR)/libxsmm.$(DLIBEXT)
	@rm -f $(OUTDIR)/*.bin
	@rm -f .make .state



##
## dependencies
##
$(BLDDIR)/compute_forces_Dev-f90.o: $(BLDDIR)/specfem-f90.o
$(BLDDIR)/compute_forces_noDev-f90.o: $(BLDDIR)/specfem-f90.o
$(BLDDIR)/compute_forces_xsmm_dispatch-f90.o: $(BLDDIR)/specfem-f90.o
$(BLDDIR)/compute_forces_xsmm_prefetch-f90.o: $(BLDDIR)/specfem-f90.o
$(BLDDIR)/compute_forces_xsmm_static-f90.o: $(BLDDIR)/specfem-f90.o


##
## rules
##
ifneq (0,$(KNC))
ifneq (0,$(MPSS))
$(BLDDIR)/%-f90.o: $(SRCDIR)/%.f90 .state $(BLDDIR)/.make $(ROOTDIR)/Makefile $(DEPDIR)/Makefile.inc
	$(FC) $(FCMTFLAGS) $(FCFLAGS) $(DFLAGS) $(IFLAGS) -mmic -c $< -o $@

$(BLDDIR)/%-f90.o: $(SRCDIR)/%.F90 .state $(BLDDIR)/.make $(ROOTDIR)/Makefile $(DEPDIR)/Makefile.inc
	$(FC) $(FCMTFLAGS) $(FCFLAGS) $(DFLAGS) $(IFLAGS) -mmic -c $< -o $@
endif
endif
ifeq (0,$(KNC))
ifeq (0,$(MPSS))
$(BLDDIR)/%-f90.o: $(SRCDIR)/%.f90 .state $(BLDDIR)/.make $(ROOTDIR)/Makefile $(DEPDIR)/Makefile.inc
	$(FC) $(FCMTFLAGS) $(FCFLAGS) $(DFLAGS) $(IFLAGS) $(FTARGET) -c $< -o $@

$(BLDDIR)/%-f90.o: $(SRCDIR)/%.F90 .state $(BLDDIR)/.make $(ROOTDIR)/Makefile $(DEPDIR)/Makefile.inc
	$(FC) $(FCMTFLAGS) $(FCFLAGS) $(DFLAGS) $(IFLAGS) $(FTARGET) -c $< -o $@
endif
endif
