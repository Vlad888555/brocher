<?php



class DB {
    public $link;
    
    public function __construct(){
        $this->link = new mysqli("localhost", "root", "", "test1");
    }

    public function get_user(){
        $con = $this->link->query("SELECT * FROM `users`");
        if($con && $con->num_rows){
            return $con->fetch_assoc();
        }
    }
    
    public function reg($name, $password){
        $this->link->query("INSERT INTO `users` (`id`, `name`, `password`) VALUES (NULL, '$name', '$password')");   
    }
}