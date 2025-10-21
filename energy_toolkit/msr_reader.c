#include <Python.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdint.h>
#include <sys/mman.h>
#include <stdio.h>
#include <sys/stat.h>

static uint64_t read_msr(const char *registerpath, uint32_t offset) {
    int fd = open(registerpath, O_RDONLY);
    if (fd < 0) {
        PyErr_SetString(PyExc_OSError, "Failed to open MSR file");
        return 0;
    }

    uint64_t value = 0;
    if (lseek(fd, offset, SEEK_SET) == (off_t)-1) {
        close(fd);
        PyErr_SetString(PyExc_OSError, "Failed to seek in MSR file");
        return 0;
    }

    if (read(fd, &value, sizeof(value)) != sizeof(value)) {
        close(fd);
        PyErr_SetString(PyExc_OSError, "Failed to read MSR file");
        return 0;
    }

    close(fd);
    return value;
}

static double get_register_values(uint32_t energyreg, uint32_t unitreg, const char *registerpath) {
  uint64_t energy = read_msr(registerpath, energyreg);
  uint64_t unit = read_msr(registerpath, unitreg);

  uint32_t cleaned_unit = (unit >> 8) & 0x1F;
  double energy_value = energy * pow(0.5, cleaned_unit);

  return energy_value;
}



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
    NULL,           // module documentation, may be NULL
    -1,             // size of per-interpreter state of the module,
                    // or -1 if the module keeps state in global variables.
    MsrMethods
};

PyMODINIT_FUNC PyInit_msr_reader(void) {
    return PyModule_Create(&msrmodule);
}