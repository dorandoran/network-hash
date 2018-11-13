#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/errno.h>
#include <stdlib.h>
#include <sys/stat.h>

#include "helpers.h"

#define PORT_NUMBER 2345
#define SERVER_ADDRESS "127.0.0.1"

int main () {
    int server_socket, connection_status, file_size;
    struct sockaddr_in serverAddress;
    char *hashType, *fileName;
    char send_buffer[4000];
    char response[1000];
    FILE * file_to_send;

    serverAddress.sin_family = AF_INET;
    serverAddress.sin_port = htons(PORT_NUMBER);
    serverAddress.sin_addr.s_addr = inet_addr(SERVER_ADDRESS);

    while(1) {
        /* Connect to Server */
        server_socket = socket(AF_INET, SOCK_STREAM, 0);
        if (server_socket < 0) {
            perror("Error Opening Socket\n\n");
        }

        connection_status = connect(server_socket, (struct sockaddr *) &serverAddress, sizeof(serverAddress));
        if(connection_status < 0) {
            perror("Socket Error\n\n");
        }
        printf("Connected to Server\n\n");

        /** Get Hash and File User Input
            Check if Valid and Send **/
        int invalid = 1;
        while(invalid) {
            printf("INFO: Enter q or Q to quit!\n");
            printf("Enter hash type: ");
            hashType = inputString(stdin, 10);
            if (strcmp(hashType, "q") == 0 || strcmp(hashType, "Q") == 0) {
                return 0;
            }
            invalid = checkHash(server_socket, hashType);
        }
        free(hashType);
        
        invalid = 1;
        while(invalid) {
            printf("Enter file name: ");
            fileName = inputString(stdin, 10);
            if (strcmp(fileName, "q") == 0 || strcmp(fileName, "Q") == 0){
                return 0;
            }
            invalid = checkFile(server_socket, fileName);
        }
        free(fileName);

        /* Open File, Get Size, Convert to String */
        file_to_send = fopen(fileName, "rb");
        fseek(file_to_send, 0, SEEK_END);
        file_size = ftell(file_to_send);
        fseek(file_to_send, 0, SEEK_SET);

        char *str_file_size;
        asprintf(&str_file_size, "%i", file_size);

        /* Send File Size and File */
        send(server_socket, str_file_size, strlen(str_file_size) + 1, 0);
        free(str_file_size);

        while(!feof(file_to_send)) {
            fread(send_buffer, 1, sizeof(send_buffer) - 1, file_to_send);
        }
        send(server_socket, send_buffer, sizeof(send_buffer), 0);

        recv(server_socket, response, sizeof(response), 0);
        printf("\n");
        printf("%s\n\n", response);
    }

    return 0;
}