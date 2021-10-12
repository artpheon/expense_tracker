#include <Python.h>

static PyObject* spam_system(PyObject* self, PyObject* args) {
    const char* cmd;
    int stat;

    if (!PyArg_ParseTuple(args, "s", &cmd))
        return NULL;
    stat = system(cmd);
    return(Py_BuildValue("i", stat));
}
