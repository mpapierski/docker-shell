use std::io;

use super::dispatch::Dispatch;
use std::path::Path;

#[derive(Debug, PartialEq, Eq)]
pub struct List<'a>(&'a Path);

impl<'a> Dispatch for List<'a> {
    type Error = io::Error;
    fn dispatch(&self) -> Result<(), Self::Error> {
        println!("Hello {}", self.0.display());
        Ok(())
    }
}

impl<'a> From<&'a str> for List<'a> {
    fn from(t: &'a str) -> List<'a> {
        List(Path::new(t))
    }
}
