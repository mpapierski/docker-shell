use std::path::Path;
use std::path::PathBuf;
use std::{fs, io};

use super::dispatch::Dispatch;

#[derive(Debug, PartialEq, Eq)]
pub struct List<'a>(&'a Path);

#[derive(Debug, Serialize)]
struct Output {
    path: PathBuf,
    is_dir: bool,
    is_file: bool,
    size: u64,
}

impl<'a> Dispatch for List<'a> {
    type Error = io::Error;
    fn dispatch(&self) -> Result<(), Self::Error> {
        let mut outputs = Vec::new();
        for entry in fs::read_dir(self.0)? {
            let entry = entry?;
            let metadata = entry.metadata()?;
            let output = Output {
                path: entry.path(),
                is_dir: metadata.is_dir(),
                is_file: metadata.is_file(),
                size: metadata.len(),
            };
            outputs.push(output);
        }
        println!("{}", serde_json::to_string(&outputs)?);
        Ok(())
    }
}

impl<'a> From<&'a str> for List<'a> {
    fn from(t: &'a str) -> List<'a> {
        List(Path::new(t))
    }
}
