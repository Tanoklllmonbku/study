#include <stdio.h>
#include <locale.h>
#include <math.h>

// void main() {
//     double a, b, c, determinant, root1, root2, realPart, imaginaryPart;
//     printf("??????? a, b, c: ");
//     scanf("%lf %lf %lf", &a, &b, &c);
    
//     determinant = b*b-4*a*c;
    
//     if (determinant>0) {
//         root1 = (-b + sqrt(determinant))/(2*a);
//         root2 = (-b - sqrt(determinant))/(2*a);
//         printf("root1 = %.2lf, root2 = %.2lf\n", root1, root2);
//     }
//     else if (determinant == 0) {
//         root1 = root2 = -b/(2*a);
        
//         printf("root1 = root2 = %.2lf\n", root1);
//     }
//     else {
//         realPart = -b/(2*a);
//         imaginaryPart = sqrt(-determinant)/(2*a);
//         printf("root1 = %.2lf+%.2lfi and root2 = %.2f-%.2fi\n", realPart, imaginaryPart, realPart, imaginaryPart);
//     }
// }

// void main() {
//     int year;
//     printf("Insert year: ");
//     scanf("%d", &year);
//     if (year%4 == 0) {
//         if (year%100 == 0) {
//             if (year%400 == 0) 
//                 printf("%d - ??????????\n", year);
//             else
//                 printf("%d - ????????????\n", year);
//         }
//         else
//             printf("%d - ??????????\n", year);
//     }
//     else
//         printf("%d - ????????????\n", year);

// }

// void main() {
//     double num;
//     printf("Insert number... ");
//     scanf("%lf", &num);

//     if (num <= 0.0) {
//         if (num == 0.0)
//             printf("?? ????? 0");
//         else
//             printf("????? - ?????????????");
//     }
//     else
//         printf("????? - ?????????????");
// }

// void main() { 
//     int n, i, sum = 0;
    
//     do {
//         printf("??????? ????? ????????????? ?????: \n");
//         scanf("%d", &n);
//     }
//     while (n <= 0);
    
//     for (i=1; i <= n; ++i) {
//         sum += i;
//     }
//     printf("????? = %d", sum);
// }

// void main() {
//     char c;
//     int ASCIICODE;
//     do {
//         printf("Insert any alphabet char: \n");
//         scanf(" %c", &c);
//     }
//     while (!((c>='a' && c<='z') || (c>='A' && c<='Z')));
    
//     ASCIICODE = c;
//     printf("ASCII-code: %d", ASCIICODE);
// }

// void main() {
//     int n, i;
//     unsigned long long factorial = 1;
//     printf("Insert any number: ");
//     scanf("%d", &n);

//     if (n < 0)
//         printf("The number is above than 0");
//     else {
//         for (i=1; i<=n; ++i) {
//             factorial *= i;
//         }
//         printf("Factorial = %d", factorial);
//     }
// }

// void main() {
//     int i, j;
//     int counter1, counter2;
    
//     printf("Insert i and j: \n");
//     scanf("%d %d", &i, &j);

//     for (counter1 = 1; counter1 <= i; counter1++) {
//         for (counter2 = 1; counter2 <= j; counter2++)
//             printf("|%d * %d = %d", counter1, counter2, counter1*counter2);
//         printf("|\n");
//     }
// }

// void main() {
//     int n1, n2;

//     printf("Insert two numbers: \n");
//     scanf("%d %d", &n1, &n2);

//     n1 = (n1 > 0) ? n1 : -n1;
//     n2 = (n2 > 0) ? n2 : -n2;

//     while (n1!=n2) 
//     {
//         if (n1 > n2)
//             n1 -= n2;
//         else
//             n2 -= n1;
//     }
//     printf("??? = %d", n1);

// }

// void main() {
//     int n1, n2, minMultiple;
    
//     printf("Insert two numbers: \n");
//     scanf("%d %d", &n1, &n2);

//     minMultiple = (n1>n2) ? n1 : n2;

//     while(1) {
//         if ( minMultiple%n1==0 && minMultiple%n2==0) {
//             printf("??? = %d.\n", minMultiple);
//             break;
//         }
//         ++minMultiple;
//     }
    
// }

// void main() {
//     long long n;
//     // int count = 0;
//     int count;

//     printf("??????? ????? ?????: ");
//     scanf("%lld", &n);

//     // while (n != 0) {
//     //     n /= 10;
//     //     ++count;
//     // }

//     for (count=0; n != 0; count++)
//         n /= 10;
//     printf("?????????? ????: %d\n", count);
// }

// void main() {
//     int num, reversedNumber = 0, remainder;

//     printf("??????? ?????: ");
//     scanf("%d", &num);

//     while (num != 0) {
//         remainder = num%10;
//         reversedNumber = reversedNumber*10 + remainder;
//         num /= 10;
//     }

//     printf("???????? ?????: %d\n", reversedNumber);
// }

// void main() {
//     int base, exp, BASETEMP, EXPTEMP;

//     long long res = 1;

//     printf("??????? ????? ? ???????: ");
//     scanf("%d %d", &base, &exp);
//     BASETEMP = base;
//     EXPTEMP = exp;
//     while (exp!=0) {
//         res *= base;
//         --exp;
//     }
//     printf("%d ? ??????? %d = %d", BASETEMP, EXPTEMP, res);
    
// }

// void main() {
//     int n, i, flag = 0;
//     do {
//         printf("??????? ????? ????????????? ?????: ");
//         scanf(" %d", &n);
//     }
//     while (n < 0);

//     for(i=2; i<=n/2; ++i) {
//         if (n%i==0) {
//             flag = 1;
//             break;
//         }
//     }

//     if (flag==0)
//         printf("%d - ???????\n", n);
//     else
//         printf("%d - ?? ???????? ???????\n", n);
    
// }

// void main() {
//     int temp, low, high, i, flag;
//     do {
//         printf("??????? ????? ????????????? ?????: ");
//         scanf(" %d %d", &low, &high);
//     }
//     while (low < 0 || high < 0);

//     if (low > high) {
//         temp = low;
//         low = high;
//         high = temp;
//     }

//     while (low < high) {
//         flag = 0;
//         for(i=2; i<=low/2; ++i) {
//             if (low%i==0) {
//                 flag = 1;
//                 break;
//             }
//         }

//         if (flag==0)
//             printf("%d - ???????\n", low);
//         ++low;
//     }
//     printf("\n");
// }

// void main() {
//     int i, j, rows;
    
//     printf("??????? ???-?? ?????: ");
//     scanf("%d", &rows);
    
//     for(i=1; i<=rows; ++i) {
//         for(j=1; j<=i; ++j) {
//             printf("* ");
//         }
//         printf("\n");
//     }
// }
//
// void main() {
//     char operator;
//     double firstNum, secondNum;
//
//     printf("??????? ????????: ");
//     scanf("%c", &operator);
//
//     printf("??????? ??? ????????: ");
//     scanf("%lf %lf", &firstNum, &secondNum);
//
//     switch (operator)
//     {
//     case '+':
//         printf("%.1lf + %.1lf = %.1lf", firstNum, secondNum, firstNum+secondNum);
//         break;
//     case '-':
//         printf("%.1lf - %.1lf = %.1lf", firstNum, secondNum, firstNum-secondNum);
//         break;
//     case '*':
//         printf("%.1lf * %.1lf = %.1lf", firstNum, secondNum, firstNum*secondNum);
//         break;
//     case '/':
//         printf("%.1lf / %.1lf = %.1lf", firstNum, secondNum, firstNum/secondNum);
//         break;
//     default:
//         printf("??????! ???????? ????????");
//     }
//     printf("\n");
// }
//
// int checkPrimeNumber(int n);
// int checkArmstrongNumber(int number);
//
// int main(void)
// {
//
//     int n;
//
//     printf("Введите положительное целое число: ");
//     scanf("%d", &n);
//     int flag = checkPrimeNumber(n);
//     if (flag == 1)
//         printf("%d - простое.\n", n);
//     else
//         printf("%d - не является простым.\n", n);
//
//     flag = checkArmstrongNumber(n);
//     if (flag == 1)
//         printf("%d - число Армстронга.\n", n);
//     else
//         printf("%d - не число Армстронга.\n", n);
//
//     return 0;
// }
//
// int checkPrimeNumber(int n)
// {
//     int i, flag = 1;
//     for (i = 2; i <= n/2; i++)
//     {
//         if (n % i == 0)
//         {
//             flag = 0;
//             break;
//         }
//     }
//     return flag;
// }
//
// int checkArmstrongNumber(int number)
// {
//     int remainder, result = 0, n = 0, flag;
//
//     int originalNumber = number;
//
//     while (originalNumber != 0)
//     {
//         remainder = originalNumber /= 10;
//         ++n;
//     }
//
//     originalNumber = number;
//
//     while (originalNumber != 0)
//     {
//         remainder = originalNumber % 10;
//         result += pow(remainder, n);
//         originalNumber /= 10;
//     }
//     if (result == number)
//         flag = 1;
//     else
//         flag = 0;
//
//     return flag;
// }

// int addNumbers(int n);
//
// int main()
// {
//     int num;
//     printf("Enter a number: ");
//     scanf("%d", &num);
//     printf("The sum is: %d\n", addNumbers(num));
//     return 0;
// }
//
// int addNumbers(int n)
// {
//     if (n != 0)
//         return n + addNumbers(n - 1);
//     // else
//     //     return n;
// }

// long int fact(int n);
//
// int main()
// {
//     int n;
//     printf("Enter a number: ");
//     scanf("%d", &n);
//     printf("The factorial of %d is %ld\n", n, fact(n));
//     return 0;
// }
//
// long int fact(int n)
// {
//     if (n > 0)
//         return n*fact(n-1);
//     else
//         return 1;
// }
//
// int hcf(int a, int b);
//
// int main(void)
// {
//     int a, b;
//     printf("Enter two numbers: ");
//     scanf("%d%d", &a, &b);
//     printf("HCF = %d\n", hcf(a, b));
//     return 0;
// }
//
// int hcf(int a, int b)
// {
//     if (b != 0)
//         return hcf(b, a % b);
//     else
//         return a;
// }
//
// int convertBinToDecimal(long long n);
// long long convertDecimalToBin(int n);
//
// int main(void) {
//     long long bin;
//     int dec;
//
//     // Перевод из двоичного в десятичный
//     printf("Введите двоичное число: ");
//     scanf("%lld", &bin);
//     int decimal_result = convertBinToDecimal(bin);
//     if (decimal_result != -1)
//         printf("%lld (bin) = %d (dec)\n", bin, decimal_result);
//
//     // Перевод из десятичного в двоичный
//     printf("Введите десятичное число: ");
//     scanf("%d", &dec);
//     long long binary_result = convertDecimalToBin(dec);
//     if (binary_result != -1)
//         printf("%d (dec) = %lld (bin)\n", dec, binary_result);
//
//     return 0;
// }
//
// int convertBinToDecimal(long long n) {
//     int decimal = 0, i = 0, remainder;
//
//     while (n != 0) {
//         remainder = n % 10;
//         n /= 10;
//         decimal += remainder * (int)pow(2, i);  // Безопасное преобразование
//         ++i;
//     }
//     return decimal;
// }
//
// long long convertDecimalToBin(int n)
// {
//     long long binary = 0;
//     int i = 1, remainder, step = 1;
//     while (n != 0)
//     {
//         remainder = n % 2;
//         printf("Step %d: %d/2, остаток = %d, частное = %d\n", step++, n, remainder, n/2);
//         n /= 2;
//         binary += remainder * i;
//         i *= 10;
//     }
//     return binary;
// }
//
// int main(void)
// {
//     int n, i;
//     float num[100], sum = 0.0, avg;
//     printf("Enter the number of elements: ");
//     scanf("%d", &n);
//
//     while (n > 100 || n <= 0)
//     {
//         printf("from 1 to 100\n");
//         printf("Again");
//         scanf("%d", &n);
//     }
//     for (i=0; i<n; i++)
//         {
//             printf("Enter the number: ");
//             scanf("%f", &num[i]);
//             sum += num[i];
//         }
//         avg = sum/n;
//         printf("Average = %.2f\n", avg);
//
//         return 0;
// }
