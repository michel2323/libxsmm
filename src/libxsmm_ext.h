/******************************************************************************
** Copyright (c) 2016, Intel Corporation                                     **
** All rights reserved.                                                      **
**                                                                           **
** Redistribution and use in source and binary forms, with or without        **
** modification, are permitted provided that the following conditions        **
** are met:                                                                  **
** 1. Redistributions of source code must retain the above copyright         **
**    notice, this list of conditions and the following disclaimer.          **
** 2. Redistributions in binary form must reproduce the above copyright      **
**    notice, this list of conditions and the following disclaimer in the    **
**    documentation and/or other materials provided with the distribution.   **
** 3. Neither the name of the copyright holder nor the names of its          **
**    contributors may be used to endorse or promote products derived        **
**    from this software without specific prior written permission.          **
**                                                                           **
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS       **
** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT         **
** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR     **
** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT      **
** HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,    **
** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED  **
** TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR    **
** PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF    **
** LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING      **
** NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS        **
** SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.              **
******************************************************************************/
/* Hans Pabst (Intel Corp.)
******************************************************************************/
#ifndef LIBXSMM_EXT_H
#define LIBXSMM_EXT_H

#include "libxsmm_main.h"

#if defined(LIBXSMM_OFFLOAD_TARGET)
# pragma offload_attribute(push,target(LIBXSMM_OFFLOAD_TARGET))
#endif
#if defined(_OPENMP)
# include <omp.h>
#endif
#if defined(LIBXSMM_OFFLOAD_TARGET)
# pragma offload_attribute(pop)
#endif

#if defined(_OPENMP)
# if !defined(LIBXSMM_EXT_TASKS) && (200805 <= _OPENMP) /*OpenMP 3.0*/
#   define LIBXSMM_EXT_TASKS
# endif
# define LIBXSMM_EXT_MIN_NTASKS(NT) LIBXSMM_MAX(2/*factor*/ * (omp_get_max_threads() / (NT) - 1), 1)
# define LIBXSMM_EXT_OVERHEAD(NT) (2/*factor*/ * (NT))
# define LIBXSMM_EXT_SINGLE LIBXSMM_PRAGMA(omp single nowait)
# define LIBXSMM_EXT_FOR_PARALLEL LIBXSMM_PRAGMA(omp parallel)
# define LIBXSMM_EXT_FOR_LOOP(COLLAPSE, ...) LIBXSMM_PRAGMA(omp for private(__VA_ARGS__) schedule(dynamic) LIBXSMM_OPENMP_COLLAPSE(COLLAPSE))
# define LIBXSMM_EXT_FOR_KERNEL LIBXSMM_NOOP_ARGS
# define LIBXSMM_EXT_FOR_SYNC LIBXSMM_NOOP
#else
# define LIBXSMM_EXT_MIN_NTASKS(NT) LIBXSMM_MIN_NTASKS(NT)
# define LIBXSMM_EXT_OVERHEAD(NT) LIBXSMM_OVERHEAD(NT)
# define LIBXSMM_EXT_SINGLE LIBXSMM_NOOP
# define LIBXSMM_EXT_FOR_PARALLEL LIBXSMM_NOOP
# define LIBXSMM_EXT_FOR_LOOP(COLLAPSE, ...) LIBXSMM_NOOP_ARGS(COLLAPSE, __VA_ARGS__)
# define LIBXSMM_EXT_FOR_KERNEL LIBXSMM_NOOP_ARGS
# define LIBXSMM_EXT_FOR_SYNC LIBXSMM_NOOP
#endif

#if defined(LIBXSMM_EXT_TASKS)
# define LIBXSMM_EXT_TSK_PARALLEL LIBXSMM_PRAGMA(omp parallel) LIBXSMM_PRAGMA(omp single nowait)
# define LIBXSMM_EXT_TSK_PARALLEL_ONLY LIBXSMM_EXT_TSK_PARALLEL
# define LIBXSMM_EXT_TSK_LOOP(COLLAPSE, ...)
# define LIBXSMM_EXT_TSK_KERNEL_VARS(...) LIBXSMM_PRAGMA(omp task firstprivate(__VA_ARGS__))
# define LIBXSMM_EXT_TSK_KERNEL LIBXSMM_PRAGMA(omp task)
# define LIBXSMM_EXT_TSK_SYNC LIBXSMM_PRAGMA(omp taskwait)
#else
# define LIBXSMM_EXT_TSK_PARALLEL LIBXSMM_EXT_FOR_PARALLEL
# define LIBXSMM_EXT_TSK_PARALLEL_ONLY LIBXSMM_NOOP
# define LIBXSMM_EXT_TSK_LOOP(COLLAPSE, ...) LIBXSMM_EXT_FOR_LOOP(COLLAPSE, __VA_ARGS__)
# define LIBXSMM_EXT_TSK_KERNEL_VARS LIBXSMM_EXT_FOR_KERNEL
# define LIBXSMM_EXT_TSK_KERNEL LIBXSMM_EXT_FOR_KERNEL
# define LIBXSMM_EXT_TSK_SYNC LIBXSMM_EXT_FOR_SYNC
#endif

#endif /*LIBXSMM_EXT_H*/

