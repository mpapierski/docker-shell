pub mod commands;
use std::convert::TryInto;
use std::env;
use std::error::Error;

use commands::{Command, Dispatch};

fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<String> = env::args().skip(1).collect();
    // TODO: Use args straight and own strings
    let args: Vec<&str> = args.iter().map(String::as_str).collect();

    let cmd: Command = args[..].try_into().unwrap();
    cmd.dispatch()?;
    Ok(())
}
