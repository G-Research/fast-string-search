use std::time::Instant;

fn main() {
    let mut words = vec![];
    for i in 0..1_000_000 {
        words.push(format!("{} hello world how are you", i));
    }
    println!("{} {}", words[0], words[356]);

    let giant_string = words.join("");

    let now = Instant::now();
    let giant_upper = giant_string.to_ascii_uppercase();
    println!("Giant string upper(): {}", now.elapsed().as_millis());
}
