use std::path::Path;

#[derive(Debug, PartialEq, Eq)]
pub struct List<'a>(&'a Path);

impl<'a> From<&'a str> for List<'a> {
    fn from(t: &'a str) -> List<'a> {
        // let s :String = t.into();
        List(Path::new(t))
    }
}

// impl<'a> Into<Box<Path>> for List<'a> {
//     fn into(self) -> Box<Path> {
//         self.0
//     }
// }
