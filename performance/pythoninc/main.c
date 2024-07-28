#include <Python.h>
#include <stdio.h>
#include <stdlib.h>

void create_patch(const char *oldfile, const char *newfile, const char *patchfile) {
    PyObject *pName, *pModule, *pFunc;
    PyObject *pArgs, *pValue;

    // Initialize the Python Interpreter
    Py_Initialize();

    // Set the Python script name (the name of the module)
    pName = PyUnicode_DecodeFSDefault("bsdiff4_interface");

    // Import the bsdiff4_interface module
    pModule = PyImport_Import(pName);
    Py_DECREF(pName);

    if (pModule != NULL) {
        // Get the create_patch function from the module
        pFunc = PyObject_GetAttrString(pModule, "create_patch");

        // Check if the function is callable
        if (pFunc && PyCallable_Check(pFunc)) {
            // Prepare the arguments for the function
            pArgs = PyTuple_Pack(3, 
                                 PyUnicode_FromString(oldfile), 
                                 PyUnicode_FromString(newfile), 
                                 PyUnicode_FromString(patchfile));

            // Call the Python function
            pValue = PyObject_CallObject(pFunc, pArgs);
            Py_DECREF(pArgs);

            if (pValue != NULL) {
                printf("%s\n", PyUnicode_AsUTF8(pValue));
                Py_DECREF(pValue);
            } else {
                Py_DECREF(pFunc);
                Py_DECREF(pModule);
                PyErr_Print();
                fprintf(stderr, "Call to create_patch failed\n");
            }
        } else {
            if (PyErr_Occurred())
                PyErr_Print();
            fprintf(stderr, "Cannot find function \"create_patch\"\n");
        }
        Py_XDECREF(pFunc);
        Py_DECREF(pModule);
    } else {
        PyErr_Print();
        fprintf(stderr, "Failed to load \"bsdiff4_interface\" module\n");
    }

    // Finalize the Python Interpreter
    Py_Finalize();
}

void apply_patch(const char *oldfile, const char *patchfile, const char *newfile) {
    PyObject *pName, *pModule, *pFunc;
    PyObject *pArgs, *pValue;

    // Initialize the Python Interpreter
    Py_Initialize();

    // Set the Python script name (the name of the module)
    pName = PyUnicode_DecodeFSDefault("bsdiff4_interface");

    // Import the bsdiff4_interface module
    pModule = PyImport_Import(pName);
    Py_DECREF(pName);

    if (pModule != NULL) {
        // Get the apply_patch function from the module
        pFunc = PyObject_GetAttrString(pModule, "apply_patch");

        // Check if the function is callable
        if (pFunc && PyCallable_Check(pFunc)) {
            // Prepare the arguments for the function
            pArgs = PyTuple_Pack(3, 
                                 PyUnicode_FromString(oldfile), 
                                 PyUnicode_FromString(patchfile), 
                                 PyUnicode_FromString(newfile));

            // Call the Python function
            pValue = PyObject_CallObject(pFunc, pArgs);
            Py_DECREF(pArgs);

            if (pValue != NULL) {
                printf("%s\n", PyUnicode_AsUTF8(pValue));
                Py_DECREF(pValue);
            } else {
                Py_DECREF(pFunc);
                Py_DECREF(pModule);
                PyErr_Print();
                fprintf(stderr, "Call to apply_patch failed\n");
            }
        } else {
            if (PyErr_Occurred())
                PyErr_Print();
            fprintf(stderr, "Cannot find function \"apply_patch\"\n");
        }
        Py_XDECREF(pFunc);
        Py_DECREF(pModule);
    } else {
        PyErr_Print();
        fprintf(stderr, "Failed to load \"bsdiff4_interface\" module\n");
    }

    // Finalize the Python Interpreter
    Py_Finalize();
}

int main(int argc, char *argv[]) {
    if (argc != 5) {
        fprintf(stderr, "Usage: %s <oldfile> <newfile> <patchfile> <newnewfile>\n", argv[0]);
        return 1;
    }

    const char *oldfile = argv[1];
    const char *newfile = argv[2];
    const char *patchfile = argv[3];
    const char *newnewfile = argv[4];

    create_patch(oldfile, newfile, patchfile);
    apply_patch(oldfile, patchfile, newnewfile);

    return 0;
}
