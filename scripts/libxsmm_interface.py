#!/usr/bin/env python
###############################################################################
## Copyright (c) 2014-2016, Intel Corporation                                ##
## All rights reserved.                                                      ##
##                                                                           ##
## Redistribution and use in source and binary forms, with or without        ##
## modification, are permitted provided that the following conditions        ##
## are met:                                                                  ##
## 1. Redistributions of source code must retain the above copyright         ##
##    notice, this list of conditions and the following disclaimer.          ##
## 2. Redistributions in binary form must reproduce the above copyright      ##
##    notice, this list of conditions and the following disclaimer in the    ##
##    documentation and/or other materials provided with the distribution.   ##
## 3. Neither the name of the copyright holder nor the names of its          ##
##    contributors may be used to endorse or promote products derived        ##
##    from this software without specific prior written permission.          ##
##                                                                           ##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS       ##
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT         ##
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR     ##
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT      ##
## HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,    ##
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED  ##
## TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR    ##
## PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF    ##
## LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING      ##
## NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS        ##
## SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.              ##
###############################################################################
## Hans Pabst (Intel Corp.)
###############################################################################
from string import Template
import libxsmm_utilities
import sys, fnmatch


if __name__ == "__main__":
    argc = len(sys.argv)
    if (1 < argc):
        # required argument(s)
        filename = sys.argv[1]

        # optional argument(s)
        if (2 < argc): precision = int(sys.argv[2])
        else: precision = 0
        if (3 < argc): ilp64 = int(sys.argv[3])
        else: ilp64 = 0
        if (4 < argc): prefetch = int(sys.argv[4])
        else: prefetch = 0
        if (5 < argc): mnklist = sorted(libxsmm_utilities.load_mnklist(sys.argv[5:], 0))
        else: mnklist = list()

        template = Template(open(filename, "r").read())
        version, branch = libxsmm_utilities.version_branch()
        major, minor, update, patch = libxsmm_utilities.version_numbers(version)

        substitute = { \
            "VERSION":  version, \
            "BRANCH":   branch, \
            "MAJOR":    major, \
            "MINOR":    minor, \
            "UPDATE":   update, \
            "PATCH":    patch, \
            "MNK_INTERFACE_LIST": "" \
        }

        if (fnmatch.fnmatch(filename, "*.h*")):
            for mnk in mnklist:
                mnkstr = "_".join(map(str, mnk))
                if (2 != precision):
                    substitute["MNK_INTERFACE_LIST"] += "\n" \
                        "LIBXSMM_API void libxsmm_smm_" + mnkstr + "(const float* a, const float* b, float* c" + \
                          [");", ",\n  const float* pa, const float* pb, const float* pc);"][0!=prefetch]
                if (1 != precision):
                    substitute["MNK_INTERFACE_LIST"] += "\n" \
                        "LIBXSMM_API void libxsmm_dmm_" + mnkstr + "(const double* a, const double* b, double* c" + \
                          [");", ",\n  const double* pa, const double* pb, const double* pc);"][0!=prefetch]
                if (0 == precision):
                    substitute["MNK_INTERFACE_LIST"] += "\n"
            if (mnklist and 0 != precision): substitute["MNK_INTERFACE_LIST"] += "\n"
            print(template.substitute(substitute))
        else:
            substitute["BLASINT_KIND"] = ["C_INT", "C_LONG_LONG"][0!=ilp64]
            if (mnklist):
                substitute["MNK_INTERFACE_LIST"] += "\n"
                for mnk in mnklist:
                    mnkstr = "_".join(map(str, mnk))
                    if (0 == precision):
                        substitute["MNK_INTERFACE_LIST"] += "\n        !DIR$ ATTRIBUTES OFFLOAD:MIC :: libxsmm_smm_" + mnkstr + ", libxsmm_dmm_" + mnkstr
                    elif (2 != precision):
                        substitute["MNK_INTERFACE_LIST"] += "\n        !DIR$ ATTRIBUTES OFFLOAD:MIC :: libxsmm_smm_" + mnkstr
                    elif (1 != precision):
                        substitute["MNK_INTERFACE_LIST"] += "\n        !DIR$ ATTRIBUTES OFFLOAD:MIC :: libxsmm_dmm_" + mnkstr
                substitute["MNK_INTERFACE_LIST"] += "\n        INTERFACE"
                for mnk in mnklist:
                    mnkstr = "_".join(map(str, mnk))
                    if (2 != precision):
                        substitute["MNK_INTERFACE_LIST"] += "\n" \
                            "          PURE SUBROUTINE libxsmm_smm_" + mnkstr + "(a, b, c" + \
                            [") BIND(C)\n", "," + "&".rjust(26 - len(mnkstr)) + "\n     &    pa, pb, pc) BIND(C)\n"][0!=prefetch] + \
                            "            IMPORT :: C_FLOAT\n" \
                            "            REAL(C_FLOAT), INTENT(IN) :: a(*), b(*)\n" \
                            "            REAL(C_FLOAT), INTENT(INOUT) :: c(*)\n" + \
                            ["", "            REAL(C_FLOAT), INTENT(IN) :: pa(*), pb(*), pc(*)\n"][0!=prefetch] + \
                            "          END SUBROUTINE"
                    if (1 != precision):
                        substitute["MNK_INTERFACE_LIST"] += "\n" \
                            "          PURE SUBROUTINE libxsmm_dmm_" + mnkstr + "(a, b, c" + \
                            [") BIND(C)\n", "," + "&".rjust(26 - len(mnkstr)) + "\n     &    pa, pb, pc) BIND(C)\n"][0!=prefetch] + \
                            "            IMPORT :: C_DOUBLE\n" \
                            "            REAL(C_DOUBLE), INTENT(IN) :: a(*), b(*)\n" \
                            "            REAL(C_DOUBLE), INTENT(INOUT) :: c(*)\n" + \
                            ["", "            REAL(C_DOUBLE), INTENT(IN) :: pa(*), pb(*), pc(*)\n"][0!=prefetch] + \
                            "          END SUBROUTINE"
                substitute["MNK_INTERFACE_LIST"] += "\n        END INTERFACE"
            print(template.safe_substitute(substitute))
    else:
        sys.tracebacklimit = 0
        raise ValueError(sys.argv[0] + ": wrong number of arguments!")
