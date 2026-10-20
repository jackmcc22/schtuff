use std::cmp::Ordering;

use std::io;

use rand::prelude::*;

fn main() {
    println!("Guess the number!");

    let secret_number = rand::rng().random_range(1..=100);

    //println!("The secret number is: {secret_number}");
    loop {
        println!("please input your guess. ");

        let mut guess = String::new();


        io::stdin()
        .read_line(&mut guess)
        .expect("failed to read line");

        let guess: u32 = match guess.trim().parse() {
            Ok(num) => num,
            Err(_) => continue,
        };

        println!("you guesed: {guess}");
    
        match guess.cmp(&secret_number) {
            Ordering::Less => println!("to small!"),
            Ordering::Greater => println!("to big!"),
            Ordering::Equal => {
                println!("You win!");
                break;
            }

        }
    }

}
