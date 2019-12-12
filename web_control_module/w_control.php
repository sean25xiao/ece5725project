<?php
#echo "W has been pressed!";
$out = fopen("/home/pi/Desktop/ece5725project/web_control_fifo", "w");
fwrite($out, "w");
fclose($out);
#shell_exec("sudo echo -n $'w' > /home/pi/Desktop/ece5725project/web_control_fifo");
#echo "W has been sent!";
?>
