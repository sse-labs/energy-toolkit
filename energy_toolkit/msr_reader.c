/**
 * \file msr_reader.c
 * Authors: Maximilian Krebs
 * \brief 
 * \version 0.1
 * \date 2025-10-21
 * 
 * Copyright 2025 SSE
 * 
 */

#include <Python.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdint.h>
#include <sys/mman.h>
#include <stdio.h>
#include <sys/stat.h>

/**
 * \brief Read the given msr register file and read at the given offset
 * 
 * \param registerpath Path of the msr file in linux
 * \param offset Offset defining the register that should be read
 * \return uint64_t Returns read msr value
 */
static uint64_t read_msr(const char *registerpath, uint32_t offset) {
    // Open the file once
    int fd = open(registerpath, O_RDONLY);

    // Check validity of file descriptor
    if (fd < 0) {
        PyErr_SetString(PyExc_OSError, "Failed to open MSR file");
        return 0;
    }

    // Init the value and seek the register offset
    uint64_t value = 0;
    if (lseek(fd, offset, SEEK_SET) == (off_t)-1) {
        close(fd);
        PyErr_SetString(PyExc_OSError, "Failed to seek in MSR file");
        return 0;
    }

    // Read the register value
    if (read(fd, &value, sizeof(value)) != sizeof(value)) {
        close(fd);
        PyErr_SetString(PyExc_OSError, "Failed to read MSR file");
        return 0;
    }

    close(fd);
    return value;
}

/**
 * \brief Read the given energy and unit register under the defined path and convert them to joule
 * 
 * \param energyreg Register offset of the energy value
 * \param unitreg Register offset of the unit
 * \param registerpath Path of the msr register file
 * \return double Energy in Joule
 */
static double get_register_values(uint32_t energyreg, uint32_t unitreg, const char *registerpath) {
  uint64_t energy = read_msr(registerpath, energyreg);
  uint64_t unit = read_msr(registerpath, unitreg);

  uint32_t cleaned_unit = (unit >> 8) & 0x1F;
  double energy_value = energy * pow(0.5, cleaned_unit);

  return energy_value;
}

/**
 * \brief Python method to read energy registers of the given msr register file on an INTEL CPU
 * 
 * \param self Python object
 * \param args Python arguments
 * \return PyObject* Python double object with the read energy
 */
static PyObject* py_read_intel_msr(PyObject* self, PyObject* args) {
    const char *registerpath;
    uint32_t energyreg = 0x639;
    uint32_t unitreg = 0x606;

    if (!PyArg_ParseTuple(args, "s", &registerpath)) {
        return NULL;
    }

    double read_val = get_register_values(energyreg, unitreg, registerpath);
    return Py_BuildValue("d", read_val);
}

/**
 * \brief Python method to read energy registers of the given msr register file on an AMD CPU
 * 
 * \param self Python object
 * \param args Python arguments
 * \return PyObject* Python double object with the read energy
 */
static PyObject* py_read_amd_msr(PyObject* self, PyObject* args) {
    const char *registerpath;
    uint32_t energyreg = 0xC001029A;
    uint32_t unitreg = 0xC0010299;

    if (!PyArg_ParseTuple(args, "s", &registerpath)) {
        return NULL;
    }

    double read_val = get_register_values(energyreg, unitreg, registerpath);
    return Py_BuildValue("d", read_val);
}

static PyMethodDef MsrMethods[] = {
    {"read_amd_msr", py_read_amd_msr, METH_VARARGS, "Read AMD MSR values"},
    {"read_intel_msr", py_read_intel_msr, METH_VARARGS, "Read AMD MSR values"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef msrmodule = {
    PyModuleDef_HEAD_INIT,
    "msr_reader",   // name of module
    NULL,           // module documentation
    -1,             // size of per-interpreter state of the module,
                    // or -1 if the module keeps state in global variables.
    MsrMethods
};

PyMODINIT_FUNC PyInit_msr_reader(void) {
    return PyModule_Create(&msrmodule);
}
