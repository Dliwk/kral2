#define PY_SSIZE_T_CLEAN
#include <python3.8/Python.h>

static PyObject * _kral2_is_collide(PyObject *self, PyObject *args) {
    PyObject * obj1;
    PyObject * obj2;
    if (!PyArg_ParseTuple(args, "OO", &obj1, &obj2)) {
        return NULL;
    }
    PyObject * pos1 = PyObject_GetAttrString(obj1, "pos");
    PyObject * pos2 = PyObject_GetAttrString(obj2, "pos");
    double w1 = PyFloat_AsDouble(PyObject_GetAttrString(obj1, "width"));
    double h1 = PyFloat_AsDouble(PyObject_GetAttrString(obj1, "height"));
    double x1 = PyFloat_AsDouble(PyObject_GetAttrString(pos1, "x")) - w1 / 2;
    double y1 = PyFloat_AsDouble(PyObject_GetAttrString(pos1, "y")) - h1 / 2;

    double w2 = PyFloat_AsDouble(PyObject_GetAttrString(obj2, "width"));
    double h2 = PyFloat_AsDouble(PyObject_GetAttrString(obj2, "height"));
    double x2 = PyFloat_AsDouble(PyObject_GetAttrString(pos2, "x")) - w2 / 2;
    double y2 = PyFloat_AsDouble(PyObject_GetAttrString(pos2, "y")) - h2 / 2;

    if (x1 < x2 + w1 and x1 + w2 > x2 and y1 < y2 + h1 and y1 + h2 > y2) {
        Py_RETURN_TRUE;
    } else {
        Py_RETURN_FALSE;
    }
}

static PyMethodDef _kral2Methods[] = {
    {"is_collide", _kral2_is_collide, METH_VARARGS,
     "check objects collide"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


static struct PyModuleDef _kral2Module = {
    PyModuleDef_HEAD_INIT,
    "_kral2",                  /* name of module */
    "_kral2 internal module",  /* module documentation, may be NULL */
    -1,                        /* size of per-interpreter state of the module,
                                  or -1 if the module keeps state in global variables. */
    _kral2Methods
};

PyMODINIT_FUNC PyInit__kral2(void) {
    return PyModule_Create(&_kral2Module);
}
