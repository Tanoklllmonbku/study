#include "HelloWorld.h"
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

int sum(int x, int y){
    return x + y;
}

void print(int x){
    printf("%d", x);
}

int main(){

    char result[2];
    int z;
    int x;
    int y;

    scanf("%d", &x);
    scanf("%d", &y);

    z = sum(x, y);
    print(result);
    print(z);
    Sleep(3000);
    return 0;
}