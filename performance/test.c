#include <bzlib.h>
#include <stdio.h>

int main() {
    printf("BZ2 Version: %s\n", BZ2_bzlibVersion());
    return 0;
}
