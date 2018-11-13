#ifndef HELPERS
#define HELPERS

/* Create String of User Input Size */
char *inputString(FILE* fp, size_t size){
    char *str;
    int ch;
    size_t len = 0;
    str = realloc(NULL, sizeof(char)*size);
    if(!str)return str;
    while(EOF!=(ch=fgetc(fp)) && ch != '\n'){
        str[len++]=ch;
        if(len==size){
            str = realloc(str, sizeof(char)*(size+=16));
            if(!str)return str;
        }
    }
    str[len++]='\0';

    return realloc(str, sizeof(char)*len);
}

/* Ensure User Input is an Accepted Hash Type */
int checkHash(int sockfd, char *hashInput) {
    if (strcmp(hashInput, "sha1") == 0) {
        send(sockfd, hashInput, strlen(hashInput) + 1, 0);
        return 0;
    }
    else if (strcmp(hashInput, "sha256") == 0) {
        send(sockfd, hashInput, strlen(hashInput) + 1, 0);
        return 0;
    }
    else if (strcmp(hashInput, "sha512") == 0) {
        send(sockfd, hashInput, strlen(hashInput) + 1, 0);
        return 0;
    }
    else if (strcmp(hashInput, "md5") == 0) {
        send(sockfd, hashInput, strlen(hashInput) + 1, 0);
        return 0;
    }
    else {
        printf("Not a valid hashing algorithm!\n");
        return 1;
    }
}

/* Ensure User Input is Valid File in Current Directory */
int checkFile (int sockfd, char *fileInput) {
  struct stat buffer;   
  if (stat (fileInput, &buffer) == 0) {
      send(sockfd, fileInput, strlen(fileInput) + 1, 0);
      return 0;
  }
  else {
      printf("Not a valid file!\n");
      return 1;
  }
}

#endif