#include <stdio.h> 
#include <string.h> 
#include <fcntl.h> 
#include <sys/stat.h> 
#include <sys/types.h> 
#include <unistd.h> 

int main()
{
	int fd;
	char * myfifo = "/home/pi/Desktop/ece5725project/cv_fifo";

	   	fd = open(myfifo, O_WRONLY);
	   	write(fd, "r", 1);
	   	close(fd);
	
	return 0;
}
